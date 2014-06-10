#!/usr/bin/env python2

from distutils.core import setup


setup(
    name='positronic-brain',
    version='0.0.1',
    description='Opinionated Buildbot workflow',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
    ],
    packages=['positronic.brain'],
    license='GNU General Public License 3',
    long_description=open('README.md').read(),
)
