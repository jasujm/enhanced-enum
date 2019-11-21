import unittest

from enumecg.utils import split_name


class UtilsTest(unittest.TestCase):
    def test_split_name_lower_snake_case(self):
        parts, joiner = split_name("snake_case")
        self.assertSequenceEqual(parts, ["snake", "case"])
        self.assertEqual(joiner(parts + ["rules"]), "snake_case_rules")
        self.assertEqual(joiner([]), "")

    def test_split_name_lower_snake_case_with_numbers(self):
        parts, _ = split_name("sn4ke_cas3")
        self.assertSequenceEqual(parts, ["sn4ke", "cas3"])

    def test_split_name_upper_snake_case(self):
        parts, joiner = split_name("SNAKE_CASE")
        self.assertSequenceEqual(parts, ["snake", "case"])
        self.assertEqual(joiner(parts + ["rules"]), "SNAKE_CASE_RULES")
        self.assertEqual(joiner([]), "")

    def test_split_name_upper_snake_case_with_numbers(self):
        parts, _ = split_name("SN4KE_CAS3")
        self.assertSequenceEqual(parts, ["sn4ke", "cas3"])

    def test_split_name_upper_camel_case(self):
        parts, joiner = split_name("CamelCase")
        self.assertSequenceEqual(parts, ["camel", "case"])
        self.assertEqual(joiner(parts + ["rules"]), "CamelCaseRules")
        self.assertEqual(joiner([]), "")

    def test_split_name_upper_camel_case_with_numbers(self):
        parts, _ = split_name("C4melCas3")
        self.assertSequenceEqual(parts, ["c4mel", "cas3"])

    def test_split_name_lower_camel_case(self):
        parts, joiner = split_name("mixedCase")
        self.assertSequenceEqual(parts, ["mixed", "case"])
        self.assertEqual(joiner(parts + ["rules"]), "mixedCaseRules")
        self.assertEqual(joiner([]), "")

    def test_split_name_upper_camel_case_with_numbers(self):
        parts, _ = split_name("C4melCas3")
        self.assertSequenceEqual(parts, ["c4mel", "cas3"])

    def test_split_name_with_single_lowercase_word_should_be_snake_case(self):
        _, joiner = split_name("word")
        self.assertSequenceEqual(joiner(["snake", "case"]), "snake_case")

    def test_split_name_with_single_uppercase_word_should_be_snake_case(self):
        _, joiner = split_name("WORD")
        self.assertSequenceEqual(joiner(["snake", "case"]), "SNAKE_CASE")

    def test_split_name_with_single_capitalized_word_should_be_camel_case(self):
        _, joiner = split_name("Word")
        self.assertSequenceEqual(joiner(["camel", "case"]), "CamelCase")

    def test_name_with_unrecognized_case_should_raise_error(self):
        self.assertRaises(ValueError, split_name, "odd word")
