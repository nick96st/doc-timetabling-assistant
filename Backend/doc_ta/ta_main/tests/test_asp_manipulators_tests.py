from django import test
from ta_main import asp_manipulators
from ta_main import models as ta_models
from ta_main import asp_code_generator
from ta_main import views
import os


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

class ASPParseTests(test.SimpleTestCase):

    def setUp(self):
        pass

    def test_parses_standard(self):
        term = "course(9,Monday,Maths)"
        expected = {"id": "course", "params": ["9", "Monday", "Maths"]}
        result = asp_manipulators.tokenize_asp_term(term)

        self.assertEquals(expected, result)

    def test_invalid_no_bracket_term(self):
        term = "course123"
        expected = None
        result = asp_manipulators.tokenize_asp_term(term)

        self.assertEquals(expected, result)

    def test_asp_to_string(self):
        term = {"id": "course", "params": ["9", "Monday", "Maths"]}
        expected = "course(9,Monday,Maths)"
        result = asp_manipulators.json_term_to_asp_string(term)

        self.assertEquals(expected, result)

    def test_asp_to_string_catch_attribute_missing_exception(self):
        term = {"params": ["9", "Monday", "Maths"]}
        expected = None
        result = asp_manipulators.json_term_to_asp_string(term)

        self.assertEquals(expected, result)

def generate_lectureclass_json(name,room,day,hour):
    return {"time":hour,"name":name,"room":str(room),"day":day}

unsatisfiable = "UNSATISFIABLE"
satisfiable = "SATISFIABLE"

def invoke_codegen_sequence_with_facts(grid_objects):
    codegen = asp_code_generator.CodeGeneratorBuilder()
    codegen.with_result_facts(grid_objects)
    # codegen.with_hard_constraints(hard_constraints)
    # codegen.with_soft_constraints(soft_constraints)
    generator = codegen.build()
    generator.should_generate = True
    generator.generate_code('test_001.in')
    input_src = "test_001.in"
    output_src = "test_001.out"
    command_string = "./clingo-4.5.4.linux-x86_64/clingo --outf=2 <" + input_src + ">" + output_src
    os.system(command_string)
    # views.run_clingo('./test_001.in','./test_001.out')
    code_result = generator.get_result_status('test_001.out')
    return code_result

class HardConstraintsTest(test.TestCase):
    # Note: to test constraints do(look test test_forbid_3_consequitive_hours):
    # 1) def facts an array of  "[ta_models.LectureClass().init_from_json( \
    #                           generate_lectureclass_json([course_name],[room],[day],[hour])),"
    # 2) the satisfy/not satisfy result is result = invoke_codegen_sequence_with_facts(facts)
    def setUp(self):
        GenerateFirstYearsDB()  # fills the db
        pass

    def test_forbid_3_consequitive_hours(self):
        facts = [ta_models.LectureClass().init_from_json( \
                generate_lectureclass_json("Hardware","311","Monday",10)),
            ta_models.LectureClass().init_from_json( \
                generate_lectureclass_json("Hardware", "311", "Monday", 11)),
            ta_models.LectureClass().init_from_json( \
                generate_lectureclass_json("Hardware", "311", "Monday", 12)),
                ]

        code_result = invoke_codegen_sequence_with_facts(facts)
        self.assertEquals(code_result, unsatisfiable)


    def test_forbid_2_subjects_in_same_room_at_a_given_time(self):
        facts = [ta_models.LectureClass().init_from_json( \
                generate_lectureclass_json("Hardware","311","Monday",10)),
            ta_models.LectureClass().init_from_json( \
                generate_lectureclass_json("Descrete", "311", "Monday", 10)),
                ]

        code_result = invoke_codegen_sequence_with_facts(facts)
        self.assertEquals(code_result, unsatisfiable)

    def test_2_lectures_of_same_subject_must_be_consequitive_if_in_same_day(self):
        facts = [ta_models.LectureClass().init_from_json( \
            generate_lectureclass_json("Hardware", "311", "Monday", 10)),
            ta_models.LectureClass().init_from_json( \
                generate_lectureclass_json("Hardware", "311", "Monday", 12)),
        ]

        code_result = invoke_codegen_sequence_with_facts(facts)
        self.assertEquals(code_result, unsatisfiable)

    def test_2_lectures_of_same_subject_cant_be_in_2_diferent_rooms_at_same_time(self):
        facts = [ta_models.LectureClass().init_from_json( \
            generate_lectureclass_json("Hardware", "311", "Monday", 10)),
            ta_models.LectureClass().init_from_json( \
                generate_lectureclass_json("Hardware", "308", "Monday", 10)),
        ]

        code_result = invoke_codegen_sequence_with_facts(facts)
        self.assertEquals(code_result, unsatisfiable)

    def test_room_capacity_not_smaller_than_subject_requirement(self):
        facts = [ta_models.LectureClass().init_from_json( \
            generate_lectureclass_json("Hardware", "144", "Monday", 10)),
        ]

        code_result = invoke_codegen_sequence_with_facts(facts)
        self.assertEquals(code_result, unsatisfiable)




