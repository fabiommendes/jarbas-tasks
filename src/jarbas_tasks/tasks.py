import os

import invoke as inv
import pkg_resources

# Dependency injection via mocks
_execvp = os.execvp


def default_tasks():
    """
    Return a mapping from task name to task object for all default tasks.

    By default, it includes the 'run' and 'bash' tasks on the list.
    """
    tasks = {'run': run, 'bash': bash}
    for entry_point in pkg_resources.iter_entry_points('jarbas_task'):
        tasks[entry_point.name] = entry_point.load()
    return tasks


#
# Default task implementations
#
@inv.task
def run(ctx):
    """
    Run a bash shell.
    """
    print('Warning: No default "run" task is defined. '
          'Falling back to a bash shell.')
    bash(ctx)


@inv.task
def bash(ctx):
    """
    Opens a bash shell.
    """
    if os.environ.get('RUNNING_ON_DOCKER', False):
        prefix = 'docker-'
    else:
        prefix = ''

    file_name = prefix + 'bashrc'
    rcfile = os.path.join(os.path.dirname(__file__), 'data', file_name)
    _execvp('bash', ['bash', '--rcfile', rcfile])
