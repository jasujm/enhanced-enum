"""
EnumECG command line interface
..............................

Contains the command line interface to EnumECG. The entry point is
:func:`cli()`.
"""

import traceback

import click
import yaml

from . import generate
from .generators import DocumentationStyle
from .definitions import PrimaryType


def _get_enum_values(enum_type):
    return [e.value for e in enum_type.__members__.values()]


def _report_error_and_fail(message):
    click.secho(message, err=True, fg="red")
    traceback.print_exc()
    raise click.Abort()


@click.command()
@click.option(
    "--documentation",
    type=click.Choice(_get_enum_values(DocumentationStyle)),
    help="Documentation style",
)
@click.option(
    "--primary-type",
    type=click.Choice(_get_enum_values(PrimaryType)),
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
    try:
        enum = yaml.safe_load(file)
    except Exception:  # pylint: disable=broad-except
        _report_error_and_fail(f"Failed to load {file.name}")

    try:
        output = generate(
            enum,
            documentation=documentation,
            primary_type=primary_type,
            value_type=value_type,
        )
    except Exception:  # pylint: disable=broad-except
        _report_error_and_fail(f"Failed to generate code from {file.name}")

    click.echo(output)
