"""
Utilities
---------

The utilities in this module are used to perform miscellaneous tasks that the
library needs to perform. While they are mainly targeted for internal use, they
are may also be useful outside the scope of the :mod:`enumecg` package.
"""

import regex


def _capitalize_word(word):
    return word[0].upper() + word[1:].lower()


def _join_lower_snake_case(parts):
    return "_".join(part.lower() for part in parts)


def _join_upper_snake_case(parts):
    return "_".join(part.upper() for part in parts)


def _join_upper_camel_case(parts):
    return "".join(_capitalize_word(part) for part in parts)


def _join_lower_camel_case(parts):
    return parts[0].lower() + "".join(_capitalize_word(part) for part in parts[1:])


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


def split_name(name: str):
    """Split names into subwords

    This function is used to split a name (variable, class etc.) into subwords,
    and creating new names with the same case style. An example demonstrates
    this the best:

    .. testsetup::

        from enumecg.utils import split_name

    .. doctest::

        >>> parts, joiner = split_name("snake_case")
        >>> parts
        ['snake', 'case']
        >>> joiner(["name", "in", "snake", "case"])
        'name_in_snake_case'

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

    Parameters:
       name: The name to analyze

    Returns:
      .. compound::

         A tuple containing:

         1. A list of subwords in ``name``

         2. A function that can be called with a sequence of strings, returning
            a name with the same case style as the original ``name``

    Raises:
        :exc:`ValueError`: If ``name`` doesn't follow any known case style.
    """
    for pattern, joiner in _SPLIT_NAME_TESTS:
        match = pattern.fullmatch(name)
        if match:
            return [part.lower() for part in match.captures("parts")], joiner
    raise ValueError(f"Could not split {name!r} into subwords")
