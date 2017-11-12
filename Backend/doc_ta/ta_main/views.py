# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import request, response
from django.template import loader
import models as ta_models
from django.shortcuts import render
import datetime
import asp_code_generator
import os
import json
from django.views.decorators.csrf import csrf_exempt
# from rest_framework.decorators import APIView, permission_classes
# from rest_framework.permissions import AllowAny


def read_from_asp_result(result_src):
    f = open(result_src)
    data = f.read()
    f.close()
    return data


def run_clingo(input_src, output_src):
    command_string = "./asp/clingo --outf=2 <" + input_src + ">" + output_src
    os.system(command_string)


# get index page
def get_index(request):
    template = loader.get_template("index.html")
    context = {}
    return response.HttpResponse(template.render(context,request))


# checks if constraints with current table selection succeeds

@csrf_exempt
def generate_table(request):
    codegen = asp_code_generator.CodeGeneratorBuilder()
    # codegen.with_hard_constraints(hard_constraints)
    # codegen.with_soft_constraints(soft_constraints)
    generator = codegen.build()
    try:
        generator.generate_code('default_001.in')
    except asp_code_generator.CodeGeneratorException:
        response.HttpResponseServerError()
    run_clingo('./default_001.in','./default_001.out')
    result = generator.parse_result('default_001.out')

    return response.HttpResponse(content=result)

@csrf_exempt
def check_constraints(request):
    # grid_objects = request["data"]["grid_objects"]
    timetable = json.loads(request.body)["timetable"]
    # hard_constraints = request.data["constraints"]
    # soft_constraints = request.data[""]
    if not timetable:
        return response.HttpResponseBadRequest('No grid objects data given')

    # create models from json
    grid_objects = []
    for obj in timetable:
        model = ta_models.LectureClass()
        model.init_from_json(obj)
        grid_objects.append(model)

    # build pattern
    codegen = asp_code_generator.CodeGeneratorBuilder()
    codegen.with_result_facts(grid_objects)
    # codegen.with_hard_constraints(hard_constraints)
    # codegen.with_soft_constraints(soft_constraints)
    generator = codegen.build()
    # check if code generator generates without exceptions
    try:
        generator.generate_code('default_001.in')
    except asp_code_generator.CodeGeneratorException:
        response.HttpResponseServerError()
    # runs clingo
    run_clingo('./default_001.in','./default_001.out')
    code_result = generator.get_result_status('default_001.out')
    return response.HttpResponse(content=code_result)


@csrf_exempt
def save_timetable(request):
    # return response.HttpResponse(content=json.loads(request.body)['timetable'],content_type="application/json")
    timetable = json.loads(request.body)["timetable"]
    # delete any previous saved data
    previous_save = ta_models.SavedTable.objects.filter(name="test_timetable").first()
    if not (previous_save is None):
        ta_models.LectureClass.objects.filter(save_it_belongs_to=previous_save).delete()
        previous_save.delete()

    save_id = ta_models.SavedTable()
    save_id.name = "test_timetable"  # TODO: pass a name of timetable
    save_id.save()
    for obj in timetable:
        model = ta_models.LectureClass()
        model.init_from_json(obj)
        model.save_it_belongs_to = save_id
        model.save()

    return response.HttpResponse(status=200)


import tests.database_inits as DB
@csrf_exempt
def init_timeslots_DoC(request):
    DB.generate_all()
    return response.HttpResponse()


