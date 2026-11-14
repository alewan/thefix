import pytest
from thefix.argument_parser import Parser
from thefix.const import ARGUMENT_PLACEHOLDER


def _args(**override):
    args = {'alias': None, 'command': [], 'yes': False,
            'help': False, 'version': False, 'debug': False,
            'force_command': None, 'repeat': False,
            'enable_experimental_instant_mode': False,
            'shell_logger': None}
    args.update(override)
    return args


@pytest.mark.parametrize('argv, result', [
    (['thefix'], _args()),
    (['thefix', '-a'], _args(alias='fix')),
    (['thefix', '--alias', '--enable-experimental-instant-mode'],
     _args(alias='fix', enable_experimental_instant_mode=True)),
    (['thefix', '-a', 'fix'], _args(alias='fix')),
    (['thefix', 'git', 'branch', ARGUMENT_PLACEHOLDER, '-y'],
     _args(command=['git', 'branch'], yes=True)),
    (['thefix', 'git', 'branch', '-a', ARGUMENT_PLACEHOLDER, '-y'],
     _args(command=['git', 'branch', '-a'], yes=True)),
    (['thefix', ARGUMENT_PLACEHOLDER, '-v'], _args(version=True)),
    (['thefix', ARGUMENT_PLACEHOLDER, '--help'], _args(help=True)),
    (['thefix', 'git', 'branch', '-a', ARGUMENT_PLACEHOLDER, '-y', '-d'],
     _args(command=['git', 'branch', '-a'], yes=True, debug=True)),
    (['thefix', 'git', 'branch', '-a', ARGUMENT_PLACEHOLDER, '-r', '-d'],
     _args(command=['git', 'branch', '-a'], repeat=True, debug=True)),
    (['thefix', '-l', '/tmp/log'], _args(shell_logger='/tmp/log')),
    (['thefix', '--shell-logger', '/tmp/log'],
     _args(shell_logger='/tmp/log'))])
def test_parse(argv, result):
    assert vars(Parser().parse(argv)) == result
