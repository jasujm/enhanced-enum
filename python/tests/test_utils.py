import unittest

from enumecg.utils import NameFormatter, CppTypeDeducer


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
        self.assertEqual(
            formatter.join(["joinable", "thing"], pluralize=True), "joinable_things"
        )
        self.assertEqual(formatter.join([], pluralize=True), "")

    def test_names_with_different_cases_should_raise_error(self):
        self.assertRaises(ValueError, NameFormatter, "lower", "UPPER")

    def test_type_deducer_with_empty_type_list_should_raise_error(self):
        self.assertRaises(ValueError, CppTypeDeducer)

    def test_type_deducer_string(self):
        deducer = CppTypeDeducer("string", "another string")
        self.assertEqual(deducer.type_name, "std::string_view")
        self.assertEqual(deducer.get_initializer("string"), '"string"')

    def test_type_deducer_bytes(self):
        deducer = CppTypeDeducer(b"bytes", b"more bytes", "...and a string")
        self.assertEqual(deducer.type_name, "std::string_view")
        self.assertEqual(deducer.get_initializer(b"bytes"), '"bytes"')

    def test_type_deducer_int(self):
        deducer = CppTypeDeducer(1, 2, 3)
        self.assertEqual(deducer.type_name, "long")
        self.assertEqual(deducer.get_initializer(1), "1")

    def test_type_deducer_float(self):
        deducer = CppTypeDeducer(3.14, 2.71)
        self.assertEqual(deducer.type_name, "double")
        float_initializer = deducer.get_initializer(3.14)
        self.assertIsInstance(float_initializer, str)
        self.assertAlmostEqual(float(float_initializer), 3.14)

    def test_type_deducer_bool(self):
        deducer = CppTypeDeducer(True, False)
        self.assertEqual(deducer.type_name, "bool")
        self.assertEqual(deducer.get_initializer(True), "true")
        self.assertEqual(deducer.get_initializer(False), "false")

    def test_type_deducer_tuple_simple(self):
        deducer = CppTypeDeducer(("string", 1, 2.3), ("another", 4, 5.6))
        self.assertEqual(
            deducer.type_name, "std::tuple<std::string_view, long, double>"
        )
        self.assertSequenceEqual(
            deducer.get_initializer(["string", 1, True]), ['"string"', "1", "true"],
        )

    def test_type_deducer_tuple_complex(self):
        deducer = CppTypeDeducer(
            (),  # Empty sequence should not affect type deduction
            (
                [],  # This is consistent with any tuple
                [1, 2],  # Deduce that the second type is tuple<int, int>
                False,
            ),
            (
                ["an", "array"],  # Deduce that the first type ys tuple<str, str>
                [3],  # This is consistent with tuple<int, int>
                True,
            ),
        )
        self.assertEqual(
            deducer.type_name,
            "std::tuple<std::tuple<std::string_view, std::string_view>, std::tuple<long, long>, bool>",
        )

    def test_type_deducer_with_unrecognized_type_should_raise_error(self):
        self.assertRaises(ValueError, CppTypeDeducer, object())
        self.assertRaises(ValueError, CppTypeDeducer.get_initializer, object())

    def test_type_deducer_with_incompatible_types_should_raise_error(self):
        self.assertRaises(ValueError, CppTypeDeducer, "str", 1, 3.14)
