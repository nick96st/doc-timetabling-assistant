# THIS FILES HOLDS FUNCTIONS TO INITIALIZE THE DATABASE
# WITH EXAMPLE DATA FOR YEARS 1,2,3,4

from ta_main import models as ta_models


# SUBJECT CREATION
def create_subject(title, title_asp, hours, code, selection_level, pop, term, course):
    subject = ta_models.Subject()
    subject.title = title
    subject.title_asp = title_asp
    subject.hours = hours
    subject.code = code
    subject.selection_level = selection_level
    subject.population_estimate = pop
    subject.save()
    create_term_relation(subject, term)
    create_course_relation(subject, course)


# CREATE TERMS RELATIONS
def create_term_relation(subject, term):
    term_obj = ta_models.ClassTerm()
    term_obj.subject = subject
    term_obj.term = term
    term_obj.save()


def create_term(name, weeks):
    term = ta_models.Term()
    term.name = name
    term.number_of_weeks = weeks
    term.save()


def init_term_objects():
    create_term("Term 1", 11)
    create_term("Term 2", 11)
    create_term("Term 3", 11)


# CREATES COURSE RELATIONS
def create_course_relation(subject, course):
    term_obj = ta_models.SubjectsCourses()
    term_obj.subject = subject
    term_obj.courseyear = course
    term_obj.save()


def create_course(name):
    course_obj = ta_models.CourseYear()
    course_obj.name = name
    course_obj.save()


def init_course_objects():
    create_course("ComputingY1")
    create_course("ComputingY3")


# INITIALIZE BASES AS ROOMS AND SLOTS
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


# TIMESLOT INIT
def init_t1m3sl0ts_DoC():
    for i in range(9, 18):
        for day in ta_models.days_choices:
            if ta_models.Timeslot.objects.filter(day=day[0], hour=i).first() is None:
                # return response.HttpResponse(content="does not have item")
                model = ta_models.Timeslot()
                model.hour = i
                model.day = day[0]
                model.save()


def init_base():
    in1t_r00ms()
    init_t1m3sl0ts_DoC()
    init_term_objects()
    init_course_objects()


# INITIALIZING FIRST YEAR
def GenerateFirstYearsDB():
    init_firstYearSubjectsAutumn()
    init_firstYearSubjectsSpring()


def init_firstYearSubjectsAutumn():  # NOTE: DONT TOUCH cancer naming style :D
    term_1 = ta_models.Term.objects.filter(name="Term 1").first()
    course_1 = ta_models.CourseYear.objects.filter(name="ComputingY1").first()

    create_subject("Hardware", "hardware", 3, 112, "M", 182, term_1, course_1)
    create_subject("Logic", "logic", 3, 140, "M", 182, term_1, course_1)
    create_subject("Programming I", "programmingi", 5, 120, "M", 182, term_1, course_1)
    create_subject("Math Methods", "mm", 4, 145, "M", 145, term_1, course_1)
    create_subject("Descrete", "ds", 3, 142, "M", 145, term_1, course_1)


def init_firstYearSubjectsSpring():  # NOTE: DONT TOUCH cancer naming style :D
    term_2 = ta_models.Term.objects.filter(name="Term 2").first()
    course_1 = ta_models.CourseYear.objects.filter(name="ComputingY1").first()

    create_subject("Architecture", "architecture", 3, 113, "M", 182, term_2, course_1)
    create_subject("ProgrammingII", "programmingii", 3, 1202, "M", 182, term_2, course_1)
    create_subject("Databases I", "databasesi", 3, 130, "M", 182, term_2, course_1)
    create_subject("Reasoning For Programs", "reasoningforprograms", 3, 141, "M", 145, term_2, course_1)
    create_subject("Graphs And Algo", "graphsandalgo", 3, 150, "M", 145, term_2, course_1)


def Generate3rdYearCourses():
    InitThirdYearMandatoryCourses()
    InitThirdYearSelectableCoursesAutumn()
    InitThirdYearSelectableCoursesSpring()


def InitThirdYearMandatoryCourses():
    term_1 = ta_models.Term.objects.filter(name="Term 1").first()
    course_3 = ta_models.CourseYear.objects.filter(name="ComputingY3").first()

    create_subject("Third Year Group project", "thirdyeargroupproject", 1, 362, "M", 182, term_1, course_3)


def InitThirdYearSelectableCoursesAutumn():
    term_1 = ta_models.Term.objects.filter(name="Term 1").first()
    course_3 = ta_models.CourseYear.objects.filter(name="ComputingY3").first()

    create_subject("Adv Databases", "advdatabases", 3, 572, "S", 100, term_1, course_3)
    create_subject("Operations Research", "operationsresearch", 3, 343, "S", 100, term_1, course_3)
    create_subject("Computer Vision", "computervision", 3, 316, "S", 100, term_1, course_3)
    create_subject("Robotics", "robotics", 3, 333, "S", 100, term_1, course_3)
    create_subject("Coding Theory", "codingtheory", 3, 349, "S", 100, term_1, course_3)
    create_subject("Type Systems", "typesystems", 3, 382, "S", 100, term_1, course_3)
    create_subject("Sim and Modelling", "simandmodelling", 3, 337, "S", 100, term_1, course_3)


def InitThirdYearSelectableCoursesSpring():
    term_2 = ta_models.Term.objects.filter(name="Term 2").first()
    course_3 = ta_models.CourseYear.objects.filter(name="ComputingY3").first()

    create_subject("Verification", "verification", 3, 303, "S", 100, term_2, course_3)
    create_subject("LogicBased Learning", "logicbasedlearning", 3, 304, "S", 100, term_2, course_3)
    create_subject("Graphics", "graphics", 3, 317, "S", 100, term_2, course_3)
    create_subject("Custom computing", "customcomputing", 3, 318, "S", 100, term_2, course_3)
    create_subject("CS in Schools", "csinschools", 3, 322, "S", 100, term_2, course_3)
    create_subject("Web Security", "websecurity", 3, 331, "S", 100, term_2, course_3)
    create_subject("AdvancedComputerArchitecture", "advancedcomputerarchitecture", 3, 332, "S", 100, term_2, course_3)
    create_subject("PervasiveComputing", "pervasivecomputing", 3, 338, "S", 100, term_2, course_3)
    create_subject("DistributedAlgorithms", "distributedalgorithms", 3, 347, "S", 100, term_2, course_3)
    create_subject("MachineLearning", "machinelearning", 3, 395, "S", 100, term_2, course_3)


# FUNCTION TO GENERATE ALL
def generate_all():
    init_base()                 # Rooms, slots, terms and courses
    GenerateFirstYearsDB()      # First year subjects
    Generate3rdYearCourses()    # Third year subjects
