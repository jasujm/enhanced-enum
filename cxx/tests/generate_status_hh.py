#!/usr/bin/env python

import sys

import jinja2

from tests.common import STATUS_DEFINITION_DICT, NESTED_ENUM_DEFINITION_DICT
from enumecg import generate


_STATUS_HH_TEMPLATE = jinja2.Template(
    """
#include <enhanced_enum/enhanced_enum.hh>

#include <string_view>

namespace testapp {

{{ status_definitions }}

}

namespace nested {

{{ nested_enum_definitions }}

}
"""
)


def main(filename):
    status_definitions = generate(STATUS_DEFINITION_DICT)
    nested_enum_definitions = generate(
        NESTED_ENUM_DEFINITION_DICT, primary_type="enhanced"
    )
    status_hh = _STATUS_HH_TEMPLATE.render(
        status_definitions=status_definitions,
        nested_enum_definitions=nested_enum_definitions,
    )
    with open(filename, "w") as out:
        print(status_hh, file=out)


if __name__ == "__main__":
    main(sys.argv[1])
