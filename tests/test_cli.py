import click.testing
import pytest

from jt import cli

@pytest.fixture
def runner():
    return click.testing.CliRunner()

def test_no_args(runner):
    """calling jt with no args gets a 'not implemented"""
    result = runner.invoke(cli.main)
    assert result.exit_code == 0

