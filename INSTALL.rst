=========================
Installation instructions
=========================

Jarbas Tasks can be installed using pip::

    $ python3 -m pip install jarbas-tasks --user

If you prefer to install it system-wide, skip the ``--user`` flag and execute
the command as superuser or using ``sudo``.


Troubleshoot
------------

Windows users may find that the above command only works if typed from Python's
installation directory.

Some Linux distributions (e.g. Ubuntu) install Python without installing pip.
Please install it using the package manager or download the get-pip.py script
at https://bootstrap.pypa.io/get-pip.py and execute it as
``python3 get-pip.py --user``.


Development
-----------

If you want to contribute to jarbas-tasks, first clone the git repository with
the command

::

    $ git clone https://github.com/fabiommendes/jarbas-task

After cloning, install the dependencies with::

    $ python setup.py develop
