#!/usr/bin/env python

import sys

import jinja2

from tests.common import STATUS_DEFINITION
from enumecg import generate


_STATUS_HH_TEMPLATE = jinja2.Template(
    """
#include <enhanced_enum/enhanced_enum.hh>

#include <string_view>

namespace testapp {

{{ status_definitions }}

}
"""
)


def main(filename):
    status_definitions = generate(STATUS_DEFINITION)
    status_hh = _STATUS_HH_TEMPLATE.render(status_definitions=status_definitions)
    with open(filename, "w") as out:
        print(status_hh, file=out)


if __name__ == "__main__":
    main(sys.argv[1])
