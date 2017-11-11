# THIS FILES HOLDS FUNCTIONS TO INITIALIZE THE DATABASE
# WITH EXAMPLE DATA FOR YEARS 1,2,3,4

from django import test
from ta_main import asp_manipulators
from ta_main import models as ta_models
from ta_main import asp_code_generator
from ta_main import views

def init_t1m3sl0ts_DoC():
    for i in range(9,18):
        for day in ta_models.days_choices:
            if ta_models.Timeslot.objects.filter(day=day[0], hour=i).first() is None:
                # return response.HttpResponse(content="does not have item")
                model = ta_models.Timeslot()
                model.hour = i
                model.day = day[0]
                model.save()

def init_firstYearSubjects(): # NOTE: DONT TOUCH cancer naming style :D
    subject = ta_models.Subject()
    subject.title = "Hardware"
    subject.title_asp = "hardware"
    subject.hours = 3
    subject.code = 112
    subject.population_estimate = 182
    subject.save()

    subject = ta_models.Subject()
    subject.title = "Logic"
    subject.title_asp = "logic"
    subject.hours = 3
    subject.code = 140
    subject.population_estimate = 182
    subject.save()

    subject = ta_models.Subject()
    subject.title = "Programming I"
    subject.title_asp = "programmingi"
    subject.hours = 5
    subject.code = 120
    subject.population_estimate = 182
    subject.save()

    subject = ta_models.Subject()
    subject.title = "Math Methods"
    subject.title_asp = "mm"
    subject.hours = 4
    subject.code = 145
    subject.population_estimate = 145
    subject.save()

    subject = ta_models.Subject()
    subject.title = "Descrete"
    subject.title_asp = "ds"
    subject.hours = 3
    subject.code = 142
    subject.population_estimate = 145
    subject.save()


def in1t_r00ms():
    room = ta_models.Room()
    room.room_name = "311"
    room.room_size = "150"
    room.save()
    room = ta_models.Room()
    room.room_name = "308"
    room.room_size = "182"
    room.save()
    room = ta_models.Room()
    room.room_name = "145"
    room.room_size = "100"
    room.save()
    room = ta_models.Room()
    room.room_name = "144"
    room.room_size = "90"
    room.save()


def GenerateFirstYearsDB():
    in1t_r00ms()
    init_t1m3sl0ts_DoC()
    init_firstYearSubjects()


def InitThirdYearMandatoryCourses():
    subject = ta_models.Subject()
    subject.title = "3rd Year Group project"
    subject.title_asp = "3rdyeargroupproject"
    subject.hours = 1
    subject.code = 362
    subject.selection_level = "M"
    subject.population_estimate = 182
    subject.save()


def InitThirdYearSelectableCoursesAutumn():
    subject = ta_models.Subject()
    subject.title = "Adv Databases"
    subject.title_asp = "advdatabases"
    subject.hours = 3
    subject.code = 572
    subject.selection_level = "S"
    subject.population_estimate = 100
    subject.save()

    subject = ta_models.Subject()
    subject.title = "Operations Research"
    subject.title_asp = "operationsresearch"
    subject.hours = 3
    subject.code = 343
    subject.selection_level = "S"
    subject.population_estimate = 100
    subject.save()

    subject = ta_models.Subject()
    subject.title = "Operations Research"
    subject.title_asp = "operationsresearch"
    subject.hours = 3
    subject.code = 362
    subject.selection_level = "S"
    subject.population_estimate = 100
    subject.save()

    subject = ta_models.Subject()
    subject.title = "Computer Vision"
    subject.title_asp = "computervision"
    subject.hours = 3
    subject.code = 316
    subject.selection_level = "S"
    subject.population_estimate = 100
    subject.save()

    subject = ta_models.Subject()
    subject.title = "Robotics"
    subject.title_asp = "robotics"
    subject.hours = 3
    subject.code = 333
    subject.selection_level = "S"
    subject.population_estimate = 100
    subject.save()

    subject = ta_models.Subject()
    subject.title = "Coding Theory"
    subject.title_asp = "codingtheory"
    subject.hours = 3
    subject.code = 349
    subject.selection_level = "S"
    subject.population_estimate = 100
    subject.save()

    subject = ta_models.Subject()
    subject.title = "Type Systems"
    subject.title_asp = "typesystems"
    subject.hours = 3
    subject.code = 382
    subject.selection_level = "S"
    subject.population_estimate = 100
    subject.save()

    subject = ta_models.Subject()
    subject.title = "Sim and Modelling"
    subject.title_asp = "simandmodelling"
    subject.hours = 3
    subject.code = 337
    subject.selection_level = "S"
    subject.population_estimate = 100
    subject.save()


def InitThirdYearSelectableCoursesSpring():
    subject = ta_models.Subject()
    subject.title = "Verification"
    subject.title_asp = "verification"
    subject.hours = 3
    subject.code = 303
    subject.selection_level = "S"
    subject.population_estimate = 100
    subject.save()

    subject = ta_models.Subject()
    subject.title = "LogicBased Learning"
    subject.title_asp = "logicbasedlearning"
    subject.hours = 3
    subject.code = 304
    subject.selection_level = "S"
    subject.population_estimate = 100
    subject.save()

    subject = ta_models.Subject()
    subject.title = "Graphics"
    subject.title_asp = "graphics"
    subject.hours = 3
    subject.code = 317
    subject.selection_level = "S"
    subject.population_estimate = 100
    subject.save()

    subject = ta_models.Subject()
    subject.title = "Custom computing"
    subject.title_asp = "customcomputing"
    subject.hours = 3
    subject.code = 318
    subject.selection_level = "S"
    subject.population_estimate = 100
    subject.save()

    subject = ta_models.Subject()
    subject.title = "CS in Schools"
    subject.title_asp = "csinschools"
    subject.hours = 3
    subject.code = 322
    subject.selection_level = "S"
    subject.population_estimate = 100
    subject.save()

    subject = ta_models.Subject()
    subject.title = "Web Security"
    subject.title_asp = "websecurity"
    subject.hours = 3
    subject.code = 331
    subject.selection_level = "S"
    subject.population_estimate = 100
    subject.save()

    subject = ta_models.Subject()
    subject.title = "AdvancedComputerArchitecture"
    subject.title_asp = "advancedcomputerarchitecture"
    subject.hours = 3
    subject.code = 332
    subject.selection_level = "S"
    subject.population_estimate = 100
    subject.save()

    subject = ta_models.Subject()
    subject.title = "PervasiveComputing"
    subject.title_asp = "pervasivecomputing"
    subject.hours = 3
    subject.code = 338
    subject.selection_level = "S"
    subject.population_estimate = 100
    subject.save()

    subject = ta_models.Subject()
    subject.title = "DistributedAlgorithms"
    subject.title_asp = "distributedalgorithms"
    subject.hours = 3
    subject.code = 347
    subject.selection_level = "S"
    subject.population_estimate = 100
    subject.save()

    subject = ta_models.Subject()
    subject.title = "MachineLearning"
    subject.title_asp = "machinelearning"
    subject.hours = 3
    subject.code = 395
    subject.selection_level = "S"
    subject.population_estimate = 100
    subject.save()


def Generate3rdYearCourses():
    InitThirdYearMandatoryCourses()
    InitThirdYearSelectableCoursesAutumn()
    InitThirdYearSelectableCoursesSpring()
