import pytest

from enumecg.utils import NameFormatter, CppTypeDeducer
from enumecg.exceptions import Error


def test_name_formatter_lower_snake_case():
    formatter = NameFormatter("snake_case", "sn4ke_cas3", "test_123")
    assert formatter.parts[0] == ["snake", "case"]
    assert formatter.parts[1] == ["sn4ke", "cas3"]
    assert formatter.parts[2] == ["test", "123"]
    assert formatter.join(["snake", "case", "rules", "123"]) == "snake_case_rules_123"
    assert formatter.join([]) == ""


def test_name_formatter_upper_snake_case():
    formatter = NameFormatter("SNAKE_CASE", "SN4KE_CAS3", "TEST_123")
    assert formatter.parts[0] == ["snake", "case"]
    assert formatter.parts[1] == ["sn4ke", "cas3"]
    assert formatter.parts[2] == ["test", "123"]
    assert formatter.join(["snake", "case", "rules", "123"]) == "SNAKE_CASE_RULES_123"
    assert formatter.join([]) == ""


def test_name_formatter_upper_camel_case():
    formatter = NameFormatter("CamelCase", "C4melCas3")
    assert formatter.parts[0] == ["camel", "case"]
    assert formatter.parts[1] == ["c4mel", "cas3"]
    assert formatter.join(["camel", "case", "rules"]) == "CamelCaseRules"
    assert formatter.join([]) == ""


def test_name_formatter_lower_camel_case():
    formatter = NameFormatter("camelCase", "c4melCas3")
    assert formatter.parts[0] == ["camel", "case"]
    assert formatter.parts[1] == ["c4mel", "cas3"]
    assert formatter.join(["camel", "case", "rules"]) == "camelCaseRules"
    assert formatter.join([]) == ""


def test_name_formatter_with_single_lowercase_word_should_be_snake_case():
    formatter = NameFormatter("word")
    assert formatter.join(["snake", "case"]) == "snake_case"


def test_name_formatter_with_single_uppercase_word_should_be_snake_case():
    formatter = NameFormatter("WORD")
    assert formatter.join(["snake", "case"]) == "SNAKE_CASE"


def test_name_formatter_with_single_capitalized_word_should_be_camel_case():
    formatter = NameFormatter("Word")
    assert formatter.join(["camel", "case"]) == "CamelCase"


def test_name_with_unrecognized_case_should_raise_error():
    with pytest.raises(Error):
        NameFormatter("odd word")


def test_name_formatter_pluralize():
    formatter = NameFormatter("word")
    assert formatter.join(["joinable", "thing"], pluralize=True) == "joinable_things"
    assert formatter.join([], pluralize=True) == ""


def test_names_with_different_cases_should_raise_error():
    with pytest.raises(Error):
        NameFormatter("lower", "UPPER")


def test_type_deducer_with_empty_type_list_should_raise_error():
    with pytest.raises(Error):
        CppTypeDeducer()


def test_type_deducer_string():
    deducer = CppTypeDeducer("string", "another string")
    assert deducer.type_name == "std::string_view"
    assert deducer.get_initializer("string") == '"string"'


def test_type_deducer_bytes():
    deducer = CppTypeDeducer(b"bytes", b"more bytes", "...and a string")
    assert deducer.type_name == "std::string_view"
    assert deducer.get_initializer(b"bytes") == '"bytes"'


def test_type_deducer_int():
    deducer = CppTypeDeducer(1, 2, 3)
    assert deducer.type_name == "long"
    assert deducer.get_initializer(1) == "1"


def test_type_deducer_float():
    deducer = CppTypeDeducer(3.14, 2.71)
    assert deducer.type_name == "double"
    float_initializer = deducer.get_initializer(3.14)
    assert type(float_initializer) is str
    assert float(float_initializer) == 3.14


def test_type_deducer_bool():
    deducer = CppTypeDeducer(True, False)
    assert deducer.type_name == "bool"
    assert deducer.get_initializer(True) == "true"
    assert deducer.get_initializer(False) == "false"


def test_type_deducer_tuple_simple():
    deducer = CppTypeDeducer(("string", 1, 2.3), ("another", 4, 5.6))
    assert deducer.type_name == "std::tuple<std::string_view, long, double>"
    assert deducer.get_initializer(["string", 1, True]) == ['"string"', "1", "true"]


def test_type_deducer_tuple_complex():
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
    assert (
        deducer.type_name
        == "std::tuple<std::tuple<std::string_view, std::string_view>, std::tuple<long, long>, bool>"
    )


def test_type_deducer_with_explicit_typename():
    deducer = CppTypeDeducer(type_name="MyType")
    assert deducer.type_name == "MyType"


def test_type_deducer_with_unrecognized_type_should_raise_error():
    with pytest.raises(Error):
        CppTypeDeducer(object())


def test_get_initializer_with_unrecognized_type_should_raise_error():
    with pytest.raises(Error):
        CppTypeDeducer.get_initializer(object())


def test_type_deducer_with_incompatible_types_should_raise_error():
    with pytest.raises(Error):
        CppTypeDeducer("str", 1, 3.14)
