import os
import sys
from types import ModuleType

import invoke as inv

from . import __version__
from . import tasks

OPTIONS = """
  bash   Start a bash shell
  tasks  List all available tasks
  run    Execute the "run" task or start a bash shell"""

MESSAGE = """Usage: jarbas-tasks COMMAND

  Execute a jarbas standard command or a task from tasks.py

Commands:%s

jarbas-tasks reads all tasks in the tasks.py file and make
them available as sub-commands.
""" % OPTIONS


def main(argv=None):
    argv = sys.argv if argv is None else argv

    _, *args = argv

    if not args:
        raise SystemExit(MESSAGE)
    elif args[0] == 'bash':
        tasks.bash(inv.Context())
    elif args[0] == 'tasks':
        get_program(True).run(['jarbas_tasks', '-l'])
    elif args[0] == 'run':
        get_program(False).run(['jarbas_tasks'] + args)
    else:
        get_program(False).run(['jarbas_tasks'] + args)


def get_loader_class(override):
    """
    Creates a Loader subclass that can inject the default run and bash
    commands to the list of tasks.

    If override=True, it overrides any user-supplied run/bash commands with the
    default implementation.
    """

    class Loader(inv.FilesystemLoader):
        def load(self, name=None):
            nonlocal override

            try:
                tasks_mod, mod_path = super().load(name)
            except inv.CollectionNotFound:
                tasks_mod = ModuleType('tasks')
                mod_path = os.getcwd()
            existing_tasks = {
                name
                for name in dir(mod_path)
                if isinstance(getattr(mod_path, name), inv.Task)}

            for task_name, task in tasks.default_tasks().items():
                if override or task_name not in existing_tasks:
                    setattr(tasks_mod, task_name, task)
            return tasks_mod, mod_path

    return Loader


def get_program(override):
    return inv.Program(
        version=__version__,
        binary='jarbas_tasks',
        name='Jarbas tasks',
        loader_class=get_loader_class(override),
    )
