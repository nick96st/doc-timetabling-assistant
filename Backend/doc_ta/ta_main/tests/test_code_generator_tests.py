from django import test
from ta_main import asp_manipulators
from ta_main import models as ta_models
from ta_main import asp_code_generator
from ta_main import views
import database_inits as DatabaseInits
import json
# UNIT TESTS FOR CODE GENERATOR

bad_request = 400
success_code = 200

class TestCodeGeneratorCases(test.TestCase):

    def setUp(self):
        DatabaseInits.init_base()
        DatabaseInits.GenerateFirstYearsDB()

    def code_gen_build(self):
        codegen = asp_code_generator.CodeGeneratorBuilder()
        return codegen.build()

    def test_selects_only_proper_term_subjects(self):
        generator = asp_code_generator.CodeGeneratorBuilder()
        generator.for_term("Term 1")
        generator = generator.build()
        # Note currently only first year term 1 should be init
        expected = ["hardware","logic", "programmingi","mathmethods","descrete"]
        generator.select_subjects_from_term()
        result = generator.generate_default_object_definitions()

        for subject in expected:
            self.assertEquals(subject in result, True,msg=result)

    def test_generates_timeslots(self):
        pass


# TESTS FOR  RestAPI TO ISSUE PROPER CODE GENERATIONS
class TestCodeGeneratorIntegrationCases(test.TestCase):
    def setUp(self):
        self.client = test.Client()
        DatabaseInits.init_base()
        DatabaseInits.GenerateFirstYearsDB()

    def test_generates_table(self):

        response = self.client.get(path='/timetable/generate',
                                   data={"term":"Term 1"},
                                   content_type="application/json",
                                   )

        self.assertEquals(response.status_code, success_code)
        # TODO:
        # self.assertEquals(response.content, expected)
        pass

    def test_generates_no_term_selected_400(self):
        response = self.client.get(path='/timetable/generate',
                                   )

        self.assertEquals(response.status_code, bad_request)
        pass

    def test_saves_generated(self):
        pass

    def test_check_table(self):
        test_timetable = [{"time":12, "day":"Monday", "room": "308", "name":"Hardware"}]
        response = self.client.post(path='/timetable/check',
                                   data=json.dumps({"term":"Term 1", "timetable":test_timetable}),
                                   content_type="application/json"
                                   )

        self.assertEquals(response.status_code, success_code, msg= response.content)
        pass

    def test_check_table_no_request_param_timetable(self):
        response = self.client.post(path='/timetable/check',
                                   data={"term":"Term 1"},
                                   )

        self.assertEquals(response.status_code, bad_request)
        pass

    def test_check_table_no_request_param_term(self):
        response = self.client.post(path='/timetable/check',
                                   data={"timetable":[]},
                                   )
        self.assertEquals(response.status_code, bad_request,msg= response.content)
        pass


