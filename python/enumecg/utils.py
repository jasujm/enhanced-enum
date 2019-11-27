"""
Utilities
.........

Utilities to perform miscellaneous tasks that the library needs to
perform. While they are mainly targeted for internal use, they are may
also be useful outside the scope of the :mod:`enumecg` package.
"""

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


_SPLIT_NAME_TESTS = [
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

    The following case styles are recognized:

    - Snake case with all lowercase letters: ``lower_snake_case``

    - Snake case with all uppercase letters: ``UPPER_SNAKE_CASE``

    - Camel case with every word capitalized: ``CamelCase``

    - Camel case with the first word starting with a lowercase letter:
      ``mixedCase``. A single lower case word is recognized as snake_case
      instead of mixedCase.

    Only ASCII alphanumeric characters are supported, because the function
    targets code generation. Numbers may appear in any other position except at
    the start of a subword.
    """

    _inflect = inflect.engine()

    def __init__(self, *names: str):
        """
        Parameters:
          name: The name to analyze

        Raises:
          :exc:`ValueError`: If at least one of the ``names`` doesn't
            follow a known case style, or if the sample contains names
            that follow different case style.
        """
        for pattern, joiner in _SPLIT_NAME_TESTS:
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
    def parts(self):
        """List of the name parts used to create the formatter"""
        return self._parts

    def join(self, parts: typing.Iterable[str], *, pluralize=False):
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
