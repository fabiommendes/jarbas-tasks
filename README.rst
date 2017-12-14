============
Jarbas tasks
============

This is a very small module defines a mechanism to inject invoke tasks to
Jarbas enabled projects. The jarbas-tasks cli is designed to be used as an
entry point of a docker container and is used as such in most Jarbas based
images. By default, it accepts the following sub-commands:

Start a bash shell:

    $ jarbas-tasks bash   # starts a bash shell
    $ jarbas-tasks run    # run the default "run" task (a bash shell, by default)
    $ jarbas-tasks tasks  # list all tasks

(jarbas-tasks can also be replaced by ``python3 -m jarbas_tasks``)


If the CWD has a tasks.py, the jarbas-tasks works basically as a replacement for
the "inv" command which adds a default implementation for the "bash", "run" and
"tasks" commands.

Run a task defined in tasks.py:

    $ jarbas-tasks some-task


Creating a task package
=======================

By default, jarbas-tasks inject only the "run" and "bash" tasks to the list of
available tasks. Users can create *task packages* that can inject arbitrary
default tasks to the jarbas-tasks command.

In order to do so, create a Python package that expose the following entry
point:

    setup(
        ...,
        entry_points={
            'jarbas-tasks': [
                'mytask1 = mytask:task1',  # Maps command name to task object
                'mytask2 = mytask:task2',
            ]
        },
    }

The handler should be a regular invoke task declared anywhere in the module.
