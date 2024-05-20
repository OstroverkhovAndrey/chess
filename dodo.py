#!/usr/bin/env python3

import glob
from doit.tools import create_folder


def task_erase():
    """Clean all generated files not tracked by GIT."""
    return {
            'actions': ["git reset --hard", "git clean -xdf"],
           }


def task_style():
    """Check style against flake8."""
    return {
            'actions': ['flake8 --config .flake8 server/src client/src'],
            'verbosity': 2,
           }


def task_docstyle():
    """Check docstrings against pydocstyle."""
    return {
            'actions': ['pydocstyle server/src client/src'],
            'verbosity': 2,
           }


def task_html():
    """Make HTML documentationi."""
    return {
            'actions': [(create_folder, ["docs/source/_static"]), 'sphinx-build -M html ./docs/source ./docs/build'],
            'verbosity': 0,
           }


def task_test():
    """Preform tests."""
    yield {'actions': ['coverage run -m unittest -v tests/test_*'],
           'verbosity': 0, 'name': "run"}
    yield {'actions': ['coverage report'], 'verbosity': 2, 'name': "report"}


def task_pot():
    """Re-create .pot ."""
    return {
            'actions': ['pybabel extract . -o client/src/msg.pot'],
            'file_dep': glob.glob('client/src/*.py'),
            'targets': ['client/src/msg.pot'],
           }


def task_po():
    """Update translations."""
    return {
            'actions': ['pybabel update --ignore-pot-creation-date -D msg -i client/src/msg.pot -l ru_RU.UTF-8 -d client/src/po'],
            'file_dep': ['client/src/msg.pot'],
            'targets': ['client/src/po/ru_RU.UTF-8/LC_MESSAGES/msg.po'],
           }


def task_mo():
    """Compile translations."""
    return {
            'actions': [
                       "pybabel compile -D msg -l ru_RU.UTF-8 -d client/src/po -i  client/src/po/ru_RU.UTF-8/LC_MESSAGES/msg.po"
                       ],
            'file_dep': ["client/src/po/ru_RU.UTF-8/LC_MESSAGES/msg.po"],
            'targets': ["client/src/po/ru_RU.UTF-8/LC_MESSAGES/msg.mo"],
           }


def task_check():
    """Perform all checks."""
    return {
            'actions': None,
            'task_dep': ['style', 'docstyle', 'test']
           }


def task_wheel():
    return {
        'actions': ['pyproject-build -n -w'],
        'verbosity': 2,
        'task_dep': ['mo'],
    }



def task_wheel_server():
    return {
        'actions': ['pyproject-build -n -w ./server/'],
        'verbosity': 2,
        'task_dep': ['mo'],
    }


def task_wheel_client():
    return {
        'actions': ['pyproject-build -n -w ./client/'],
        'verbosity': 2,
        'task_dep': ['mo'],
    }


def task_sdist():
    return {
        'actions': ['pyproject-build -n -s'],
        'verbosity': 2,
        'task_dep': ['erase'],
    }
