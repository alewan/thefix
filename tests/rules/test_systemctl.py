from thefix.rules.systemctl import match, get_new_command
from thefix.types import Command


def test_match():
    assert match(Command('systemctl nginx start', 'Unknown operation \'nginx\'.'))
    assert match(Command('sudo systemctl nginx start', 'Unknown operation \'nginx\'.'))
    assert not match(Command('systemctl start nginx', ''))
    assert not match(Command('systemctl start nginx', ''))
    assert not match(Command('sudo systemctl nginx', 'Unknown operation \'nginx\'.'))
    assert not match(Command('systemctl nginx', 'Unknown operation \'nginx\'.'))
    assert not match(Command('systemctl start foo', 'Failed to start foo.service: Unit foo.service failed to load: No such file or directory.'))


def test_get_new_command():
    assert get_new_command(Command('systemctl nginx start', '')) == "systemctl start nginx"
    assert get_new_command(Command('sudo systemctl nginx start', '')) == "sudo systemctl start nginx"
