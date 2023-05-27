#!/usr/bin/env python3
import os
from setuptools import setup

BASEDIR = os.path.abspath(os.path.dirname(__file__))


def required(requirements_file):
    """ Read requirements file and remove comments and empty lines. """
    with open(os.path.join(BASEDIR, requirements_file), 'r') as f:
        requirements = f.read().splitlines()
        if 'MYCROFT_LOOSE_REQUIREMENTS' in os.environ:
            print('USING LOOSE REQUIREMENTS!')
            requirements = [r.replace('==', '>=').replace('~=', '>=') for r in requirements]
        return [pkg for pkg in requirements
                if pkg.strip() and not pkg.startswith("#")]


with open("README.md", "r") as f:
    long_description = f.read()


with open("./version.py", "r", encoding="utf-8") as v:
    for line in v.readlines():
        if line.startswith("__version__"):
            if '"' in line:
                version = line.split('"')[1]
            else:
                version = line.split("'")[1]


PLUGIN_ENTRY_POINT = 'neon_solver_wordnet_plugin=neon_solver_wordnet_plugin:WordnetSolver'
PERSONA_ENTRY_POINT = 'wordnet=neon_solver_wordnet_plugin:WORDNET_PERSONA'


setup(
    name='neon_solver_wordnet_plugin',
    version=version,
    description='A question solver plugin for ovos/neon/mycroft',
    url='https://github.com/NeonGeckoCom/neon_solver_wordnet_plugin',
    author='Neongecko',
    author_email='developers@neon.ai',
    license='bsd3',
    packages=['neon_solver_wordnet_plugin'],
    zip_safe=True,
    keywords='mycroft plugin utterance fallback query',
    entry_points={'neon.plugin.solver': PLUGIN_ENTRY_POINT,
                  "opm.plugin.persona": PERSONA_ENTRY_POINT},
    install_requires=required("requirements/requirements.txt"),
    long_description=long_description,
    long_description_content_type='text/markdown'
)
