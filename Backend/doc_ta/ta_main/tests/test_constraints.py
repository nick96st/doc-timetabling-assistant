from django import test
from ta_main import asp_manipulators
from ta_main import models as ta_models
from ta_main import asp_code_generator
from ta_main.tests import database_inits as DatabaseInits


def generate_lectureclass_json(name, room, day, hour):
    return {"time": hour, "name": name, "room": str(room), "day": day}


unsatisfiable = "UNSATISFIABLE"
satisfiable = "SATISFIABLE"


def invoke_codegen_sequence_with_facts(grid_objects,term="Term 1"):
    codegen = asp_code_generator.CodeGeneratorBuilder()
    codegen.for_term(term).perform("GENERATE")
    codegen.with_result_facts(grid_objects)
    # codegen.with_hard_constraints(hard_constraints)
    # codegen.with_soft_constraints(soft_constraints)
    generator = codegen.build()
    generator.should_generate = True
    generator.generate_code('test_001.in')
    generator.run_clingo('./test_001.in', './test_001.out')
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
        # creates a single subject in the empty Term 3 to easy test
        term_3 = ta_models.Term.objects.filter(name="Term 3").first()
        course_1 = ta_models.CourseYear.objects.filter(name="ComputingY1").first()
        DatabaseInits.create_subject("Test subject","testsubject", 2,1337,"M",100, term_3, course_1)

        facts_less = [ta_models.LectureClass().init_from_json(
            generate_lectureclass_json("Test subject", "308", "Monday", 10)),]
        result = invoke_codegen_sequence_with_facts(facts_less,term="Term 3")
        self.assertEquals(result, unsatisfiable, msg="DOESNT CATCH IF LESS")
        facts_enough = [ta_models.LectureClass().init_from_json(
            generate_lectureclass_json("Test subject", "308", "Monday", 10)),
            ta_models.LectureClass().init_from_json(
                generate_lectureclass_json("Test subject", "308", "Monday", 11)),]
        result = invoke_codegen_sequence_with_facts(facts_enough,term="Term 3")
        self.assertEquals(result, satisfiable, msg="THINKS ENOUGH HOURS ARE UNSATISFIABLE")
        facts_more = [ta_models.LectureClass().init_from_json(
            generate_lectureclass_json("Test subject", "308", "Monday", 10)),
            ta_models.LectureClass().init_from_json(
                generate_lectureclass_json("Test subject", "308", "Monday", 11)),
            ta_models.LectureClass().init_from_json(
                generate_lectureclass_json("Test subject", "308", "Tuesday", 10)),]
        result = invoke_codegen_sequence_with_facts(facts_more,term="Term 3")
        self.assertEquals(result, unsatisfiable,msg= "DOESNT CATCH IF MORE THAN EXACT NEEDED")

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
        clash.subject1 = ta_models.Subject.objects.get(title="Hardware")
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

    def test_lecturer_cant_teach_2_different_subjects_at_same_time(self):
        #create lecturer object
        lecturer = ta_models.Lecturer()
        lecturer.first_name = "Tony"
        lecturer.surname = "Field"
        lecturer.save()

        #assign lecturer to subjects
        teaches1 = ta_models.Teaches()
        teaches1.lecturer = lecturer
        teaches1.subject = ta_models.Subject.objects.get(title="Hardware")
        teaches1.save()

        teaches2 = ta_models.Teaches()
        teaches2.lecturer = lecturer
        teaches2.subject = ta_models.Subject.objects.get(title="Logic")
        teaches2.save()

        #allow subject to clash
        clash1 = ta_models.Clash()
        clash1.subject1 = ta_models.Subject.objects.get(title="Hardware")
        clash1.subject2 = ta_models.Subject.objects.get(title="Logic")
        clash1.save()

        clash2 = ta_models.Clash()
        clash2.subject1 = ta_models.Subject.objects.get(title="Logic")
        clash2.subject2 = ta_models.Subject.objects.get(title="Hardware")
        clash2.save()

        #should unsatisfiable due to lecturer_clash constraint
        facts = [ta_models.LectureClass().init_from_json( \
            generate_lectureclass_json("Hardware", "311", "Wednesday", 11)),
            ta_models.LectureClass().init_from_json( \
            generate_lectureclass_json("Logic", "308", "Wednesday", 11)),
            ]

        code_result = invoke_codegen_sequence_with_facts(facts)
        self.assertEquals(code_result, unsatisfiable)

    def test_max_four_hour_a_day_lecturer(self):
        #create lecturer object
        lecturer = ta_models.Lecturer()
        lecturer.first_name = "Tony"
        lecturer.surname = "Field"
        lecturer.save()

        #assign lecturer to subjects
        teaches1 = ta_models.Teaches()
        teaches1.lecturer = lecturer
        teaches1.subject = ta_models.Subject.objects.get(title="Hardware")
        teaches1.save()

        teaches2 = ta_models.Teaches()
        teaches2.lecturer = lecturer
        teaches2.subject = ta_models.Subject.objects.get(title="Logic")
        teaches2.save()

        teaches3 = ta_models.Teaches()
        teaches3.lecturer = lecturer
        teaches3.subject = ta_models.Subject.objects.get(title="Math Methods")
        teaches3.save()

        facts = [ta_models.LectureClass().init_from_json( \
                generate_lectureclass_json("Hardware", "311", "Wednesday", 9)),
            ta_models.LectureClass().init_from_json( \
                generate_lectureclass_json("Hardware", "311", "Wednesday", 10)),
            ta_models.LectureClass().init_from_json( \
                generate_lectureclass_json("Logic", "308", "Wednesday", 12)),
            ta_models.LectureClass().init_from_json( \
                generate_lectureclass_json("Logic", "308", "Wednesday", 13)),
            ta_models.LectureClass().init_from_json( \
                    generate_lectureclass_json("Math Methods", "311", "Wednesday", 15)),
            ]

        code_result = invoke_codegen_sequence_with_facts(facts)
        self.assertEquals(code_result, unsatisfiable)

    def test_no_9_to_5(self):
        facts = [ta_models.LectureClass().init_from_json( \
                generate_lectureclass_json("Hardware", "311", "Wednesday", 9)),
            ta_models.LectureClass().init_from_json( \
                generate_lectureclass_json("Hardware", "311", "Wednesday", 10)),
            ta_models.LectureClass().init_from_json( \
                generate_lectureclass_json("Logic", "308", "Wednesday", 16)),
            ta_models.LectureClass().init_from_json( \
                generate_lectureclass_json("Logic", "308", "Wednesday", 17)),
            ]

        code_result = invoke_codegen_sequence_with_facts(facts)
        self.assertEquals(code_result, unsatisfiable)

    def test_lecture_no_three_consecutive_hour(self):
        #create lecturer object
        lecturer = ta_models.Lecturer()
        lecturer.first_name = "Tony"
        lecturer.surname = "Field"
        lecturer.save()

        #assign lecturer to subjects
        teaches1 = ta_models.Teaches()
        teaches1.lecturer = lecturer
        teaches1.subject = ta_models.Subject.objects.get(title="Hardware")
        teaches1.save()

        teaches2 = ta_models.Teaches()
        teaches2.lecturer = lecturer
        teaches2.subject = ta_models.Subject.objects.get(title="Logic")
        teaches2.save()

        facts = [ta_models.LectureClass().init_from_json( \
                generate_lectureclass_json("Hardware", "311", "Wednesday", 9)),
            ta_models.LectureClass().init_from_json( \
                generate_lectureclass_json("Hardware", "311", "Wednesday", 10)),
            ta_models.LectureClass().init_from_json( \
                generate_lectureclass_json("Logic", "308", "Wednesday", 11)),
            ]

        code_result = invoke_codegen_sequence_with_facts(facts)
        self.assertEquals(code_result, unsatisfiable)
    
