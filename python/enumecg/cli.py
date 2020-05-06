"""
EnumECG command line interface
..............................

Contains the command line interface to EnumECG. The entry point is
:func:`cli()`.
"""

import sys

import click
import yaml

from . import generate

@click.command()
@click.argument("file", type=click.File(), default=sys.stdin)
def cli(file):
    """Generate C++ boilerplate for an Enhanced Enum definition

    This executable is a part of the Enhanced Enum library. It is used
    to generate the necessary C++ boilerplate to make an enumeration
    type work with the library.

    FILE is a YAML file containing the definition of the enum type. If
    FILE is - or no FILE is given, the definition is read from the
    standard input.

    For a full discussion of the purpose of the library, and a
    detailed description of the code generation process, see:

        https://enhanced-enum.readthedocs.io/en/latest/

    """
    enum = yaml.safe_load(file)
    click.echo(generate(enum))
