# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import request, response
from django.template import loader
from django.shortcuts import render
import datetime
import asp_manipulators
import os


def read_from_asp_result(result_src):
    f = open(result_src)
    data = f.read()
    f.close()
    return data


def run_clingo(input_src, output_src):
    command_string = "./asp/clingo --outf=2 <" + input_src + ">" + output_src
    os.system(command_string)


def test_view(request):
    input_src = "./asp/src/timetable_2.in"
    output_src = "result.out"
    run_clingo(input_src, output_src)
    data = read_from_asp_result(output_src)
    return response.HttpResponse(content=data, status=200)


def get_index(request):
    template = loader.get_template("index.html")
    context = {}
    return response.HttpResponse(template.render(context,request))


# checks if constraints with current table selection succeeds
def check_constraints(request):

    # grid_objects = request["data"]["grid_objects"]
    grid_objects = [{"id":"lecture","params": ["Ian","Logic"]},
                    {"id":"lecture","params": ["Mark","Reasoning"]}]
    # hard_constraints = request.data["constraints"]
    # soft_constraints = request.data[""]
    if not grid_objects:
        return response.HttpResponseBadRequest('No grid objects field')

    # build pattern
    codegen = asp_manipulators.CodeGeneratorBuilder()
    codegen.with_result_facts(grid_objects)
    # codegen.with_hard_constraints(hard_constraints)
    # codegen.with_soft_constraints(soft_constraints)
    codegen.build().generate_code('default_001.in')
    code_result = read_from_asp_result('default_001.in')
    return response.HttpResponse(content=code_result)



