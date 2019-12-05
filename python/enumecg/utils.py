"""
Utilities
.........

Utilities to perform miscellaneous tasks that the library needs to
perform. While they are mainly targeted for internal use, they are may
also be useful outside the scope of the :mod:`enumecg` package.
"""

import collections.abc as cabc
import itertools
import numbers
import typing

import inflect
import regex


def _capitalize_word(word):
    return word[0].upper() + word[1:]


def _join_lower_snake_case(parts):
    return "_".join(parts)


def _join_upper_snake_case(parts):
    return "_".join(part.upper() for part in parts)


def _join_upper_camel_case(parts):
    return "".join(_capitalize_word(part) for part in parts)


def _join_lower_camel_case(parts):
    try:
        first, *rest = parts
    except ValueError:
        return ""
    else:
        return first + "".join(_capitalize_word(part) for part in rest)


def _all_are_instances(values, type):
    return values and all(isinstance(v, type) for v in values)


class NameFormatter:
    """Format names in the same case style as sample names

    This class is used to split a sample of names (variables, classes
    etc.) into subwords, and creating new names with the same case
    style. An example demonstrates this the best:

    .. testsetup::

        from enumecg.utils import NameFormatter

    .. doctest::

        >>> formatter = NameFormatter("first_name", "second_name")
        >>> formatter.parts
        [['first', 'name'], ['second', 'name']]
        >>> formatter.join(["name", "in", "snake", "case"])
        'name_in_snake_case'
        >>> formatter.join(["snake", "case"], pluralize=True)
        'snake_cases'

    This class implements the identifier formatting described in
    :ref:`enumecg-identifiers`.
    """

    _split_name_regexes_and_joiners = [
        (
            regex.compile(r"(?P<parts>[a-z][a-z0-9]*)(_(?P<parts>[a-z][a-z0-9]*))*"),
            _join_lower_snake_case,
        ),
        (
            regex.compile(r"(?P<parts>[A-Z][A-Z0-9]*)(_(?P<parts>[A-Z][A-Z0-9]*))*"),
            _join_upper_snake_case,
        ),
        (regex.compile(r"(?P<parts>[A-Z][a-z0-9]*)+"), _join_upper_camel_case),
        (
            regex.compile(r"(?P<parts>[a-z][a-z0-9]*)(?P<parts>[A-Z][a-z0-9]*)+"),
            _join_lower_camel_case,
        ),
    ]

    _inflect = inflect.engine()

    def __init__(self, *names: str):
        """
        Parameters:
          names: The names to analyze

        Raises:
          :exc:`ValueError`: If at least one of the ``names`` doesn't
            follow a known case style, or if the sample contains names
            that follow different case style.
        """
        for pattern, joiner in self._split_name_regexes_and_joiners:
            matches = [pattern.fullmatch(name) for name in names]
            if all(matches):
                self._parts = [
                    [part.lower() for part in match.captures("parts")]
                    for match in matches
                ]
                self._joiner = joiner
                break
        else:
            raise ValueError(f"Could not find common case for {names!r}")

    @property
    def parts(self) -> typing.Sequence[str]:
        """List of the name parts used to create the formatter"""
        return self._parts

    def join(self, parts: typing.Iterable[str], *, pluralize=False) -> str:
        """Create new name from ``parts``

        Parameters:
          parts: Parts (words) of the name
          pluralize: If ``True``, assume the argument is a singular
            noun, and return it pluralized.

        Return:
          The new name as string, with the individual parts joined
          together using the case style inferred during the construction
        """
        try:
            *head, last = parts
        except ValueError:
            return ""
        else:
            if pluralize:
                last = self._inflect.plural_noun(last)
            return self._joiner(head + [last])


class CppTypeDeducer:
    """Deduce C++ types and initializers from Python values

    This class examines collections of Python values, and deduces a
    C++ type that is compatible with them. It implements the algorithm
    described in :ref:`enumecg-enumerator-values`.
    """

    _type_pairs = [
        ((str, bytes), "std::string_view"),
        (bool, "bool"),
        (numbers.Integral, "long"),
        (numbers.Real, "double"),
    ]

    def __init__(self, *values, type_name=None):
        """
        If the explicit ``type_name`` parameter is given, it is preferred and
        the ``values`` are not examined.

        Parameters:
          values: The values used to deduce the type
          type_name: The type name

        Raises:
          :exc:`ValueError`: If no C++ type compatible with
            ``values`` can be deduced.

        """
        self._type_name = type_name or self._get_compatible_type(values)

    @property
    def type_name(self) -> str:
        """The deduced C++ type"""
        return self._type_name

    @classmethod
    def get_initializer(cls, value) -> str:
        """Return C++ initializer for ``value``

        Parameters:
            A value consisting of string, numbers, booleans and nested
            requences thereof.

        Return:
            An expression that can be used in a C++ initializer list to
            initialize a type compatible with ``value`` at compile time
        """
        if isinstance(value, (str, bytes)):
            if isinstance(value, bytes):
                value = value.decode()
            return f'"{repr(value)[1:-1]}"'
        elif isinstance(value, bool):
            return "true" if value else "false"
        elif isinstance(value, numbers.Real):
            return repr(value)
        elif isinstance(value, cabc.Sequence):
            return [cls.get_initializer(v) for v in value]
        raise ValueError(f"Could not generate initializer for {value!r}")

    @classmethod
    def _get_compatible_type(cls, values):
        values = list(values)
        for (py_type, cpp_type_name) in cls._type_pairs:
            if _all_are_instances(values, py_type):
                return cpp_type_name
        if _all_are_instances(values, cabc.Sequence):
            sentinel = object()
            common_types = []
            for value_zip in itertools.zip_longest(*values, fillvalue=sentinel):
                common_type = cls._get_compatible_type(
                    v for v in value_zip if v is not sentinel
                )
                common_types.append(common_type)
            return f"std::tuple<{', '.join(common_types)}>"
        raise ValueError(f"Could not deduce compatible type for {values!r}")
