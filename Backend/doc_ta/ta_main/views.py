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


# get index page
def get_index(request):
    template = loader.get_template("index.html")
    context = {}
    return response.HttpResponse(template.render(context,request))


@csrf_exempt
def generate_table(request):
    term_name = request.GET.get("term",None)
    # term_name = json.loads(request.body)["term"]
    if not term_name:
        return response.HttpResponseBadRequest("No term field")
    codegen = asp_code_generator.CodeGeneratorBuilder()
    codegen.for_term(term_name).perform("GENERATE")
    # codegen.with_hard_constraints(hard_constraints)
    # codegen.with_soft_constraints(soft_constraints)
    generator = codegen.build()
    try:
        generator.generate_code()
    except asp_code_generator.CodeGeneratorException:
        response.HttpResponseServerError()
    generator.run_clingo()
    success, result = generator.parse_result()
    output = {"status":"","solutions":[]}
    # if there are solutions, gets them
    if success:
        output["solutions"] = result
        output["status"] = generator.get_result_status()
    # TODO: fix frontend to handle empty arrays adn remove this
    output["solutions"].append([{"time":12, "day":"Monday", "room": "308", "name":"Architecture"},
                            {"time": 13, "day": "Monday", "room": "308", "name": "Architecture"}])
    return response.HttpResponse(content=json.dumps(output), content_type="application/json")


@csrf_exempt
def check_constraints(request):
    # grid_objects = request["data"]["grid_objects"]

    try:
        timetable = json.loads(request.body)['timetable']
        if not timetable:
            return response.HttpResponseBadRequest("No timetable specified")
    except ValueError:
        return response.HttpResponseBadRequest("No timetable specified")
    try:
        term_name = json.loads(request.body)["term"]
        if not term_name:
            return response.HttpResponseBadRequest("No term specified")
    except KeyError:
        return response.HttpResponseBadRequest("No term specified")
    # hard_constraints = request.data["constraints"]
    # soft_constraints = request.data[""]
    # create models from json
    grid_objects = []
    for obj in timetable:
        model = ta_models.LectureClass()
        model.init_from_json(obj)
        grid_objects.append(model)
    # build pattern
    codegen = asp_code_generator.CodeGeneratorBuilder()
    codegen.for_term(term_name).perform("CHECK")
    codegen.with_result_facts(grid_objects)
    # codegen.with_hard_constraints(hard_constraints)
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
        return response.HttpResponse(content=json.dumps(violations),content_type="application/json")
    # if not success then something has gone wrong since it asp result should be SATISFIABLE(no hard constraints)
    else:
        return response.HttpResponseServerError("ASP result is not satisfiable")

@csrf_exempt
def update_save(request):
    try:
        timetable = json.loads(request.body)["timetable"]
    except KeyError:
        response.HttpResponseBadRequest("No timetable parameter.")
    save_id = 0
    try:
        save_id = json.loads(request.body)["save_id"]
    except KeyError:
        response.HttpResponseBadRequest("No save id parameter.")

    try:
        save_obj = ta_models.SavedTable.objects.get(id=save_id)
        ta_models.LectureClass.objects.filter(save_it_belongs_to=save_obj).delete()
        for obj in timetable:
            model = ta_models.LectureClass()
            model.init_from_json(obj)
            model.save_it_belongs_to = save_obj
            model.save()
        response.HttpResponse(status=200)
    except IndexError:
        response.HttpResponseBadRequest("Save id parameter does not exist.")


@csrf_exempt
def save_timetable(request):
    # return response.HttpResponse(content=json.loads(request.body)['timetable'],content_type="application/json")
    try:
        timetable = json.loads(request.body)["timetable"]
    except KeyError:
        response.HttpResponseBadRequest("No timetable parameter.")
    try:
        save_name = json.loads(request.body)["save_name"]
    except KeyError:
        save_name = "Unnamed"  # default name if no provided

    save_id = ta_models.SavedTable()
    save_id.name = save_name  # TODO: pass a name of timetable
    save_id.save()
    for obj in timetable:
        model = ta_models.LectureClass()
        model.init_from_json(obj)
        model.save_it_belongs_to = save_id
        model.save()

    return response.HttpResponse(status=200)


@csrf_exempt
def get_load_choices(request):

    all_saves = ta_models.SavedTable.objects.all()
    saves = []

    for save in all_saves:
        saves.append({"id":save.id, "name":save.name})

    return response.HttpResponse(content=json.dumps(saves),content_type="application/json")

@csrf_exempt
def load_save(request):
    save_id = request.GET.get("save_id", None)

    if not save_id:
        response.HttpResponseBadRequest("No save identifier given.")

    save_obj = ta_models.SavedTable.objects.get(id=save_id)
    saved_data = ta_models.LectureClass.objects.filter(save_it_belongs_to=save_obj)

    result = []
    for item in saved_data:
        result.append(item.to_json_for_frontend())

    return response.HttpResponse(content=json.dumps(result))

@csrf_exempt
def get_term_choices(request):
    all_terms = ta_models.Term.objects.all()
    term_list = []
    for term in all_terms:
        term_list.append(term.name)

    return response.HttpResponse(content=json.dumps(term_list))


@csrf_exempt
def get_subject_choices(request):
    all_subjects = ta_models.Subject.objects.all()
    subject_list = []
    for subject in all_subjects:
        subject_list.append(subject.title)

    return response.HttpResponse(content=json.dumps(subject_list))


@csrf_exempt
def get_room_choices(request):
    all_rooms = ta_models.Room.objects.all()
    room_list = []
    for room in all_rooms:
        room_list.append(room.room_name)

    return response.HttpResponse(content=json.dumps(room_list))


@csrf_exempt
def get_constraint_choices(request):
    constraints = Constraints.constraint_table_parse_verbose.keys()
    return response.HttpResponse(content=json.dumps(constraints))


import tests.database_inits as DB
@csrf_exempt
def init_timeslots_DoC(request):
    DB.generate_all()
    return response.HttpResponse()


