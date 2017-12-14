import io
import os
import sys
from contextlib import contextmanager

import pytest
from mock import patch, Mock

import jarbas_tasks
from jarbas_tasks import main

basepath = os.path.dirname(os.path.dirname(__file__))


@contextmanager
def capture_print():
    stdout = sys.stdout
    out = sys.stdout = io.StringIO()
    try:
        yield lambda: out.getvalue()
    finally:
        sys.stdout = stdout


@contextmanager
def capture_exit():
    ex = None

    def result():
        nonlocal ex

        data = out()
        if ex is not None:
            data += '\n%s' % ex
        return data

    try:
        with capture_print() as out:
            yield result
    except SystemExit as ex_:
        ex = ex_


def with_dir(newdir):
    """
    Common implementation to with_tasks and without_tasks
    """

    curr_dir = os.getcwd()
    try:
        yield os.chdir(os.path.join(basepath, newdir))
    finally:
        os.chdir(curr_dir)


@pytest.yield_fixture
def with_tasks():
    yield from with_dir('project_with_tasks')


@pytest.yield_fixture
def without_tasks():
    yield from with_dir('project_without_tasks')


@pytest.fixture(params=[False, True])
def toggle_docker(request):
    return request.param


@pytest.fixture(params=['run', 'bash'])
def task_name(request):
    return request.param


def test_project_defines_author_and_version():
    assert hasattr(jarbas_tasks, '__author__')
    assert hasattr(jarbas_tasks, '__version__')


def test_recognize_tasks(without_tasks):
    with capture_exit() as output:
        main.main(['jarbas-tasks'])

    assert output() == """
Usage: jarbas-tasks COMMAND

  Execute a jarbas standard command or a task from tasks.py

Commands:
  bash   Start a bash shell
  tasks  List all available tasks
  run    Execute the "run" task or start a bash shell

jarbas-tasks reads all tasks in the tasks.py file and make
them available as sub-commands.
"""


def test_run_bash(without_tasks, toggle_docker, task_name):
    mock = Mock()
    if toggle_docker:
        os.environ['RUNNING_ON_DOCKER'] = 'true'
    else:
        os.environ.pop('RUNNING_ON_DOCKER', None)

    with capture_exit() as output:
        with patch('jarbas_tasks.tasks._execvp', mock):
            main.main(['jarbas-tasks', task_name])
    assert mock.called

    (cmd, args), kwargs = mock.call_args
    assert cmd == 'bash'
    assert args[0:2] == ['bash', '--rcfile']

    if toggle_docker:
        assert args[2].endswith(os.path.sep + 'docker-bashrc')
    else:
        assert args[2].endswith(os.path.sep + 'bashrc')
