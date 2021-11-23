#!/usr/bin/env python3
from setuptools import setup


PLUGIN_ENTRY_POINT = 'neon_solver_wordnet_plugin=neon_solver_wordnet_plugin:WordnetSolver'
setup(
    name='neon_solver_wordnet_plugin',
    version='0.0.1',
    description='A question solver plugin for ovos/neon/mycroft',
    url='https://github.com/NeonGeckoCom/neon_solver_wordnet_plugin',
    author='JarbasAi',
    author_email='jarbasai@mailfence.com',
    license='bsd3',
    packages=['neon_solver_wordnet_plugin'],
    zip_safe=True,
    keywords='mycroft plugin utterance fallback query',
    entry_points={'neon.plugin.solver': PLUGIN_ENTRY_POINT}
)
