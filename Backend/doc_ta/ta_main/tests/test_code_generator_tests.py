from django import test
from ta_main import asp_manipulators
from ta_main import models as ta_models
from ta_main import asp_code_generator
from ta_main import views
import database_inits as DatabaseInits

# UNIT TESTS FOR CODE GENERATOR
class TestCodeGeneratorCases(test.TestCase):

    def setUp(self):
        DatabaseInits.init_base()
        DatabaseInits.GenerateFirstYearsDB()

    def code_gen_build(self):
        codegen = asp_code_generator.CodeGeneratorBuilder()
        return codegen.build()

    def test_selects_only_proper_term_subjects(self):
        generator = self.code_gen_build()
        generator.selected_term = "Term 1"

        # Note currently only first year term 1 should be init
        expected = ["hardware","logic", "programmingi","mathmethods","descrete"]
        result = generator.generate_default_object_definitions()

        for subject in expected:
            self.assertEquals(subject in result, True)

    def test_generates_timeslots(self):
        pass


# TESTS FOR  RestAPI TO ISSUE PROPER CODE GENERATIONS
class TestCodeGeneratorIntegrationCases(test.TestCase):
    def setUp(self):
        DatabaseInits.init_base()
        DatabaseInits.GenerateFirstYearsDB()

    def test_generates_table(self):
        pass

    def test_generates_no_term_selected_400(self):
        pass

    def test_saves_generated(self):
        pass

    def test_check_table(self):
        pass

    def test_check_table_no_request_param_timetable(self):
        pass

    def test_check_table_no_request_param_term(self):
        pass


