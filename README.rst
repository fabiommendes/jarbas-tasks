.. image:: https://travis-ci.org/fabiommendes/jarbas-tasks.svg?branch=master
   :target: https://travis-ci.org/fabiommendes/jarbas-tasks

.. image:: https://coveralls.io/repos/github/fabiommendes/jarbas-tasks/badge.svg?branch=master
   :target: https://coveralls.io/github/fabiommendes/jarbas-tasks?branch=master

.. image:: https://api.codeclimate.com/v1/badges/bc4f2a1234462c9de61f/maintainability
   :target: https://codeclimate.com/github/fabiommendes/jarbas-tasks/maintainability
   :alt: Maintainability


============
Jarbas tasks
============

This is a very small module that defines a mechanism to inject `invoke<https://pyinvoke.org)`_
tasks to Jarbas enabled projects. The jarbas-tasks cli is designed to be used as an
entry point of a Docker container and is used as such in most Jarbas based
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
points:

.. code-block:: python

   # setup.py
   setup(
      ...,
      entry_points={
         'jarbas-tasks': [
             'mytask1 = mytask:task1',  # Maps command name to task object
             'mytask2 = mytask:task2',
         ]
      },
   }

The handler should be a regular Invoke task declared anywhere in the module:

.. code-block:: python

   # mytask.py

   from invoke import task

   @task
   def task1(ctx):
      print('Hello from task1')

   @task
   def task2(ctx):
      print('Hello from task2')
