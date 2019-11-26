import unittest

from enumecg.utils import NameFormatter


class UtilsTest(unittest.TestCase):
    def test_name_formatter_lower_snake_case(self):
        formatter = NameFormatter("snake_case", "sn4ke_cas3")
        self.assertSequenceEqual(formatter.parts[0], ["snake", "case"])
        self.assertSequenceEqual(formatter.parts[1], ["sn4ke", "cas3"])
        self.assertEqual(formatter.join(["snake", "case", "rules"]), "snake_case_rules")
        self.assertEqual(formatter.join([]), "")

    def test_name_formatter_upper_snake_case(self):
        formatter = NameFormatter("SNAKE_CASE", "SN4KE_CAS3")
        self.assertSequenceEqual(formatter.parts[0], ["snake", "case"])
        self.assertSequenceEqual(formatter.parts[1], ["sn4ke", "cas3"])
        self.assertEqual(formatter.join(["snake", "case", "rules"]), "SNAKE_CASE_RULES")
        self.assertEqual(formatter.join([]), "")

    def test_name_formatter_upper_camel_case(self):
        formatter = NameFormatter("CamelCase", "C4melCas3")
        self.assertSequenceEqual(formatter.parts[0], ["camel", "case"])
        self.assertSequenceEqual(formatter.parts[1], ["c4mel", "cas3"])
        self.assertEqual(formatter.join(["camel", "case", "rules"]), "CamelCaseRules")
        self.assertEqual(formatter.join([]), "")

    def test_name_formatter_lower_camel_case(self):
        formatter = NameFormatter("camelCase", "c4melCas3")
        self.assertSequenceEqual(formatter.parts[0], ["camel", "case"])
        self.assertSequenceEqual(formatter.parts[1], ["c4mel", "cas3"])
        self.assertEqual(formatter.join(["camel", "case", "rules"]), "camelCaseRules")
        self.assertEqual(formatter.join([]), "")

    def test_name_formatter_with_single_lowercase_word_should_be_snake_case(self):
        formatter = NameFormatter("word")
        self.assertEqual(formatter.join(["snake", "case"]), "snake_case")

    def test_name_formatter_with_single_uppercase_word_should_be_snake_case(self):
        formatter = NameFormatter("WORD")
        self.assertEqual(formatter.join(["snake", "case"]), "SNAKE_CASE")

    def test_name_formatter_with_single_capitalized_word_should_be_camel_case(self):
        formatter = NameFormatter("Word")
        self.assertEqual(formatter.join(["camel", "case"]), "CamelCase")

    def test_name_with_unrecognized_case_should_raise_error(self):
        self.assertRaises(ValueError, NameFormatter, "odd word")

    def test_name_formatter_pluralize(self):
        formatter = NameFormatter("word")
        self.assertEqual(formatter.join(["joinable", "thing"], pluralize=True), "joinable_things")
        self.assertEqual(formatter.join([], pluralize=True), "")

    def test_names_with_different_cases_should_raise_error(self):
        self.assertRaises(ValueError, NameFormatter, "lower", "UPPER")
