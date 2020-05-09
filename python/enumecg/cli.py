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
from .generators import CodeGenerator
from .definitions import PrimaryType


@click.command()
@click.option(
    "--documentation",
    type=click.Choice(CodeGenerator.DOCUMENTATION_CHOICES),
    help="Documentation style",
)
@click.option(
    "--primary-type",
    type=click.Choice([e.value for e in PrimaryType.__members__.values()]),
    help="Primary enumeration type",
)
@click.option("--value-type", help="Enumerator value type")
@click.argument("file", type=click.File(), default="-")
def cli(file, documentation, primary_type, value_type):
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
    click.echo(
        generate(
            enum,
            documentation=documentation,
            primary_type=primary_type,
            value_type=value_type,
        )
    )