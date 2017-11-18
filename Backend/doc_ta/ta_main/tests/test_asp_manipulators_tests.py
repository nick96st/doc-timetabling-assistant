from django import test
from ta_main import asp_manipulators
from ta_main import models as ta_models
from ta_main import asp_code_generator
from ta_main import views
from ta_main.tests import database_inits as DatabaseInits


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


class TestChangeStringToAspSuitable(test.TestCase):
    def setUp(self):
        pass

    def test_removes_spaces(self):
        data = "adv  db"
        expected = "advdb"
        result = asp_manipulators.string_to_asp_suitable(data)

        self.assertEquals(result, expected)

    def test_lowers_letters(self):
        data = "Adv DB"
        expected = "advdb"
        result = asp_manipulators.string_to_asp_suitable(data)

        self.assertEquals(result, expected)


def generate_lectureclass_json(name, room, day, hour):
    return {"time": hour, "name": name, "room": str(room), "day": day}


unsatisfiable = "UNSATISFIABLE"
satisfiable = "SATISFIABLE"


def invoke_codegen_sequence_with_facts(grid_objects):
    codegen = asp_code_generator.CodeGeneratorBuilder()
    codegen.for_term("Term 1")
    codegen.with_result_facts(grid_objects)
    # codegen.with_hard_constraints(hard_constraints)
    # codegen.with_soft_constraints(soft_constraints)
    generator = codegen.build()
    generator.should_generate = True
    generator.generate_code('test_001.in')
    views.run_clingo('./test_001.in', './test_001.out')
    code_result = generator.get_result_status('test_001.out')
    return code_result


class HardConstraintsTest(test.TestCase):
    # Note: to test constraints do(look test test_forbid_3_consequitive_hours):
    # 1) def facts an array of  "[ta_models.LectureClass().init_from_json( \
    #                           generate_lectureclass_json([course_name],[room],[day],[hour])),"
    # 2) the satisfy/not satisfy result is result = invoke_codegen_sequence_with_facts(facts)
    def setUp(self):
        DatabaseInits.init_base()
        DatabaseInits.GenerateFirstYearsDB()  # fills the db
        pass

    def each_class_has_enough_hours_per_week(self):
        pass

    def test_no_3_consequitive_lectures(self):
        facts = [ta_models.LectureClass().init_from_json( \
            generate_lectureclass_json("Hardware", "308", "Monday", 10)),
            ta_models.LectureClass().init_from_json( \
                generate_lectureclass_json("Hardware", "308", "Monday", 11)),
            ta_models.LectureClass().init_from_json( \
                generate_lectureclass_json("Hardware", "308", "Monday", 12)),
        ]

        code_result = invoke_codegen_sequence_with_facts(facts)
        self.assertEquals(code_result, unsatisfiable)

    def test_2_lectures_of_same_subject_must_be_consequitive_if_in_same_day(self):
        facts = [ta_models.LectureClass().init_from_json( \
            generate_lectureclass_json("Hardware", "308", "Monday", 10)),
            ta_models.LectureClass().init_from_json( \
                generate_lectureclass_json("Hardware", "308", "Monday", 12)),
        ]

        code_result = invoke_codegen_sequence_with_facts(facts)
        self.assertEquals(code_result, unsatisfiable)

    def test_room_capacity_requirement(self):
        facts = [ta_models.LectureClass().init_from_json( \
            generate_lectureclass_json("Hardware", "311", "Monday", 10)),
        ]

        code_result = invoke_codegen_sequence_with_facts(facts)
        self.assertEquals(code_result, unsatisfiable)

    def test_force_two_hours_a_day_unless_uneven(self):
        pass

    def test_forbid_2_subjects_in_same_room_at_a_given_time(self):
        facts = [ta_models.LectureClass().init_from_json( \
            generate_lectureclass_json("Hardware", "308", "Monday", 10)),
            ta_models.LectureClass().init_from_json( \
                generate_lectureclass_json("Descrete", "308", "Monday", 10)),
        ]

        code_result = invoke_codegen_sequence_with_facts(facts)
        self.assertEquals(code_result, unsatisfiable)

    def test_allow_clashes_only_if_specified(self):
        clash = ta_models.Clash()
        clash.subject = ta_models.Subject.objects.get(title="Hardware")
        clash.subject2 = ta_models.Subject.objects.get(title="Descrete")
        clash.save()

        facts_with_valid_clash = [ta_models.LectureClass().init_from_json( \
                        generate_lectureclass_json("Hardware", "308", "Monday", 10)),
                        ta_models.LectureClass().init_from_json( \
                            generate_lectureclass_json("Descrete", "311", "Monday", 10)),
                                 ]
        facts_with_invalid_clash = [ta_models.LectureClass().init_from_json( \
                        generate_lectureclass_json("Hardware", "308", "Monday", 10)),
                        ta_models.LectureClass().init_from_json( \
                            generate_lectureclass_json("Math Methods", "311", "Monday", 10)),
                                 ]

        code_valid_result = invoke_codegen_sequence_with_facts(facts_with_valid_clash)
        self.assertEquals(code_valid_result, satisfiable)
        code_invalid_result = invoke_codegen_sequence_with_facts(facts_with_invalid_clash)
        self.assertEquals(code_invalid_result, unsatisfiable)
        pass

    def test_students_no_more_than_6_hours_a_day(self):
        facts = [ta_models.LectureClass().init_from_json( \
            generate_lectureclass_json("Hardware", "308", "Monday", 9)),
            ta_models.LectureClass().init_from_json( \
                generate_lectureclass_json("Hardware", "308", "Monday", 10)),
            ta_models.LectureClass().init_from_json( \
                generate_lectureclass_json("Math Methods", "308", "Monday", 12)),
            ta_models.LectureClass().init_from_json( \
                generate_lectureclass_json("Math Methods", "308", "Monday", 13)),
            ta_models.LectureClass().init_from_json( \
                generate_lectureclass_json("Logic", "308", "Monday", 15)),
            ta_models.LectureClass().init_from_json( \
                generate_lectureclass_json("Logic", "308", "Monday", 16)),
            ta_models.LectureClass().init_from_json( \
                generate_lectureclass_json("Logic", "308", "Monday", 17)),
        ]
        pass

    def test_lectures_of_same_subject_cant_be_in_2_diferent_rooms_at_same_time(self):
        facts = [ta_models.LectureClass().init_from_json( \
            generate_lectureclass_json("Math Methods", "311", "Monday", 10)),
            ta_models.LectureClass().init_from_json( \
                generate_lectureclass_json("Math Methods", "308", "Monday", 10)),
        ]

        code_result = invoke_codegen_sequence_with_facts(facts)
        self.assertEquals(code_result, unsatisfiable)
