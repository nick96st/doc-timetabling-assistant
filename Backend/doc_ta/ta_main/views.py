# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import response
from django.template import loader
import models as ta_models
import asp_code_generator
from asp_constraints import ConstraintHandler as Constraints
import json
from django.views.decorators.csrf import csrf_exempt
# from rest_framework.decorators import APIView, permission_classes
# from rest_framework.permissions import AllowAny
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError


def parse_timetable_into_facts(timetable):
    # create models from json
    grid_objects = []
    # return response.HttpResponse(content=timetable,
    #                              content_type="application/json")
    for obj in timetable:
        model = ta_models.LectureClass()
        model.init_from_json(obj)
        grid_objects.append(model)

    return grid_objects


# get index page
@login_required
def get_index(request):
    template = loader.get_template("index.html")
    context = {}
    return response.HttpResponse(template.render(context,request))

@csrf_exempt
@login_required
def add_constraint(request):
    try:
        constraint_def = json.loads(request.body)['constraint']
    except:
        return response.HttpResponseBadRequest("No query parameter for constraint object.")

    constraint_obj = ta_models.SlotBlocker()
    # input validation
    try:
        constraint_obj.subject = ta_models.Subject.objects.get(title=constraint_def["subject"])
        constraint_obj.day = ta_models.DayDef.objects.get(day_string=constraint_def["day"])
    except IndexError:
        return response.HttpResponseBadRequest('Day or Subject does not exist.')
    # table def

    td = constraint_obj.day.table
    if constraint_def["start"] in range(td.start_hour, td.end_hour):
        constraint_obj.start = constraint_def["start"]
    else:
        return response.HttpResponseBadRequest('Start hour not in range')
    if constraint_def["end"] in range(td.start_hour,td.end_hour) \
       and constraint_def["start"] <= constraint_def["end"]:
        constraint_obj.end = constraint_def["end"]
    else:
        return response.HttpResponseBadRequest('End hour is not suitable')

    constraint_obj.owner = request.user
    constraint_obj.generate_title()
    constraint_obj.save()
    return response.HttpResponse(status=200)


@csrf_exempt
@login_required
def generate_table(request):
    term_name = request.GET.get("term", None)
    # term_name = json.loads(request.body)["term"]
    if not term_name:
        return response.HttpResponseBadRequest("No term field")
    courses_array = request.GET.getlist("courses[]", None)
    timetable_str = request.GET.getlist("timetable[]", None)
    constraints = request.GET.getlist("constraints[]", None)
    timetable = []
    table_def_id = request.GET.get("table_def_id", None)
    for item in timetable_str:
        timetable.append(json.loads(item))
    if not timetable:
        timetable = []
    if not table_def_id:
        return response.HttpResponseBadRequest("Missing table settings.")

    grid_objects = parse_timetable_into_facts(timetable)
    codegen = asp_code_generator.CodeGeneratorBuilder()
    codegen.for_term(term_name).for_courses(courses_array).for_table(table_def_id) \
        .perform("GENERATE").with_result_facts(grid_objects).with_hard_constraints(constraints)
    # codegen.with_hard_constraints(hard_constraints)
    # codegen.with_soft_constraints(soft_constraints)
    generator = codegen.build()
    try:
        generator.generate_code()
    except asp_code_generator.CodeGeneratorException:
        response.HttpResponseServerError()
    generator.run_clingo()
    success, result = generator.parse_result()
    output = {"status": "", "solutions": []}
    # if there are solutions, gets them
    if success:
        output["solutions"] = result
        output["status"] = generator.get_result_status()
    return response.HttpResponse(content=json.dumps(output), content_type="application/json")


@csrf_exempt
@login_required
def check_constraints(request):
    query_params = json.loads(request.body)
    try:
        timetable = query_params['timetable']
    except KeyError:
        timetable = []
    try:
        term_name = query_params["term"]
    except KeyError:
        return response.HttpResponseBadRequest(json.dumps({"no_term": True}))
    try:
        constraints = query_params["constraints"]
    except KeyError:
        constraints = None
    try:
        courses_array = query_params["courses"]
    except KeyError:
        courses_array = None
    try:
        table_def = query_params["table_def_id"]
    except KeyError:
        return response.HttpResponseBadRequest("No table definition.")

    grid_objects = parse_timetable_into_facts(timetable)
    # build pattern
    codegen = asp_code_generator.CodeGeneratorBuilder()
    codegen.for_term(term_name).for_courses(courses_array).for_table(table_def).perform("CHECK")
    codegen.with_result_facts(grid_objects)
    # set constraints if  None - it will use default(ALL)
    codegen.with_hard_constraints(constraints)
    # codegen.with_soft_constraints(soft_constraints)
    generator = codegen.build()
    # check if code generator generates without exceptions
    try:
        generator.generate_code()
    except asp_code_generator.CodeGeneratorException:
        response.HttpResponseServerError("Code generator failed")
    # runs clingo
    generator.run_clingo()
    success, violations = generator.parse_result()
    # if success then send the list of violations
    if success:
        return response.HttpResponse(content=json.dumps(violations), content_type="application/json")
    # if not success then something has gone wrong since it asp result should be SATISFIABLE(no hard constraints)
    else:
        return response.HttpResponseServerError("ASP result is not satisfiable")


@csrf_exempt
@login_required
def update_save(request):
    try:
        timetable = json.loads(request.body)["timetable"]
    except KeyError:
        return response.HttpResponseBadRequest("No timetable parameter.")
    try:
        save_id = json.loads(request.body)["save_id"]
    except KeyError:
        return response.HttpResponseBadRequest("No save id parameter.")

    try:
        save_obj = ta_models.SavedTable.objects.get(id=save_id)
        ta_models.LectureClass.objects.filter(save_it_belongs_to=save_obj).delete()
        for obj in timetable:
            model = ta_models.LectureClass()
            model.init_from_json(obj)
            model.save_it_belongs_to = save_obj
            model.save()
        return response.HttpResponse(status=200)
    except IndexError:
        return response.HttpResponseBadRequest("Save id parameter does not exist.")


def create_timetable_save(save_name,timetable,table_def):
    if table_def == "DEFAULT":
        try:
            item = ta_models.TableSizeDef.objects.get(title="DEFAULT_DOC_TABLE")
        except ObjectDoesNotExist:
            item = ta_models.TableSizeDef()
            table_def, _ = item.create(["Monday","Tuesday","Wednesday","Thursday", "Friday"],
                                       9, 17, "DEFAULT_DOC_TABLE")

    save_id = ta_models.SavedTable()
    save_id.name = save_name
    save_id.table_size = ta_models.TableSizeDef.objects.get(id=table_def)
    save_id.save()
    for obj in timetable:
        model = ta_models.LectureClass()
        model.init_from_json(obj)
        model.save_it_belongs_to = save_id
        model.save()

    return {"save_id": save_id.id}

@csrf_exempt
@login_required
def save_timetable(request):
    # return response.HttpResponse(content=json.loads(request.body)['timetable'],content_type="application/json")
    try:
        timetable = json.loads(request.body)["timetable"]
    except KeyError:
        return response.HttpResponseBadRequest("No timetable parameter.")
    try:
        save_name = json.loads(request.body)["save_name"]
    except KeyError:
        save_name = "Unnamed"  # default name if no provided
    try:
        table_def_id = json.loads(request.body)["table_def_id"]
    except KeyError:
        return response.HttpResponseBadRequest("No table definition")

    result = create_timetable_save(save_name, timetable, table_def_id)

    return response.HttpResponse(status=200,content=json.dumps(result))


@csrf_exempt
@login_required
def get_load_choices(request):

    all_saves = ta_models.SavedTable.objects.all()
    saves = []

    for save in all_saves:
        saves.append({"id":save.id, "name":save.name})

    return response.HttpResponse(content=json.dumps(saves),content_type="application/json")

@csrf_exempt
@login_required
def load_save(request):
    save_id = request.GET.get("save_id", None)

    if not save_id:
        response.HttpResponseBadRequest("No save identifier given.")

    save_obj = ta_models.SavedTable.objects.get(id=save_id)
    saved_data = ta_models.LectureClass.objects.filter(save_it_belongs_to=save_obj)

    result = []
    for item in saved_data:
        result.append(item.to_json_for_frontend())
    table_def_defs = save_obj.table_size.to_json()
    table_def_defs["table"] = result
    table_def_defs["save_id"] = save_id
    # result= {"table": result, "save_id": save_id}
    return response.HttpResponse(content=json.dumps(table_def_defs))


@login_required
def get_term_choices(request):
    all_terms = ta_models.Term.objects.all()
    term_list = []
    for term in all_terms:
        term_list.append(term.name)

    return response.HttpResponse(content=json.dumps(term_list))


@login_required
def get_subject_choices(request):
    all_subjects = ta_models.Subject.objects.all()
    subject_list = []
    for subject in all_subjects:
        subject_list.append(subject.title)

    return response.HttpResponse(content=json.dumps(subject_list))

@login_required
def get_courses_choices(request):
    all_courses = ta_models.CourseYear.objects.all()
    course_list = []
    for course in all_courses:
        course_list.append(course.name)

    return response.HttpResponse(content=json.dumps(course_list))

@login_required
def get_room_choices(request):
    all_rooms = ta_models.Room.objects.all()
    room_list = []
    for room in all_rooms:
        room_list.append(room.room_name)

    return response.HttpResponse(content=json.dumps(room_list))


@login_required
def get_constraint_choices(request):
    constraints = Constraints.get_verbose_nonaxiomatic_constraints()
    for blocker in ta_models.SlotBlocker.objects.filter(owner=request.user).all():
        constraints.append(blocker.title)
    return response.HttpResponse(content=json.dumps(constraints))


@csrf_exempt
@login_required
def create_timeslots_for_table(request):
    try:
        params = json.loads(request.body)
        daydefs = params["days"]
        hours_start = params["hours_start"]
        hours_end = params["hours_end"]
        name = params["name"]
    except KeyError:
        return response.HttpResponseBadRequest("Not a post request ot not have all params")
    daydefs = daydefs.split(",")  # TODO: make this on frontend
    try:
        table_def_id, table_def = ta_models.TableSizeDef.create(daydefs, int(hours_start), int(hours_end), name)
    except IntegrityError:
        return response.HttpResponseBadRequest("NameExists")

    save_id = create_timetable_save(name, [], table_def_id)

    result = {"save_id": save_id["save_id"],
              "table_def_id": table_def_id,
              "table_def": table_def["table_def"],
              }
    return response.HttpResponse(json.dumps(result))

# FOR DEMOING PURPOSES
# import tests.database_inits as DB
#
#
# @csrf_exempt
# @login_required
# def init_timeslots_DoC(request):
#     DB.generate_all()
#     return response.HttpResponse()


