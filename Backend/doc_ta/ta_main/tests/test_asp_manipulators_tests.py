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

