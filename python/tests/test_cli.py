import yaml
import pytest

from click.testing import CliRunner

from enumecg import generate
from enumecg.cli import cli


@pytest.fixture
def cli_runner():
    """Return CliRunner() to invoke enumecg CLI"""
    return CliRunner()


@pytest.fixture
def enum_file(tmpdir, status_definition_dict):
    """Return path to an YAML file containing serialized :const:`conftest.STATUS_DEFINITION_DICT`"""
    p = tmpdir.join("enum.yaml")
    with open(p, "w") as f:
        yaml.dump(status_definition_dict, f)
    return p


def test_cli_should_generate_enum_definition_from_file(
    cli_runner, enum_file, status_definition
):
    result = cli_runner.invoke(cli, [str(enum_file)])
    assert result.output == generate(status_definition) + "\n"


def test_cli_should_have_documentation_option(cli_runner, enum_file, status_definition):
    result = cli_runner.invoke(cli, ["--documentation", "doxygen", str(enum_file)])
    assert result.output == generate(status_definition, documentation="doxygen") + "\n"


@pytest.mark.parametrize("primary_type", ["label", "enhanced"])
def test_cli_should_have_primeray_type_option(
    cli_runner, enum_file, status_definition_dict, primary_type
):
    result = cli_runner.invoke(cli, ["--primary-type", primary_type, str(enum_file)])
    assert (
        result.output
        == generate(status_definition_dict, primary_type=primary_type) + "\n"
    )
