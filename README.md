Positronic Brain
================

<img align="right" src="logo.png"/>

> *Opinionated BuildBot workflow.*

[![Build Status](https://travis-ci.org/develersrl/positronic-brain.svg?branch=master)](https://travis-ci.org/develersrl/positronic-brain)
[![Coverage Status](https://coveralls.io/repos/develersrl/positronic-brain/badge.png)](https://coveralls.io/r/develersrl/positronic-brain)
[![Stories in Ready](https://badge.waffle.io/develersrl/positronic-brain.png?label=ready&title=Ready)](https://waffle.io/develersrl/positronic-brain)

Positronic Brain makes it extremely easy to get up and running with your BuildBot server by dropping
few lines in your `master.cfg` file. Gone are the days of having to figure out how to wire all
pieces together.

Adding a positronic brain to your BuildBot brings you:

* Sensible defaults for your BuildBot master.
* Notification emails sent to _developers_ after a build failure.
* Notification emails sent to _administrators_ for all builds on all projects.
* No need to mess with Change Sources or Schedulers.
* Archiving of artifacts on the master after each successful build.
* Automatic deletion of old artifacts on the master.


Installation
------------

This package is not being published to PyPI, so for the time being you have to install it by
running:

    pip install https://github.com/develersrl/positronic-brain/archive/master.zip#egg=positronic-brain

Please note that this package depends on a very specific version of the BuildBot master and you have
to make sure to have it installed first (see [requirements.txt](requirements.txt) for more details).


Usage
-----

In your BuildBot master configuration file (`master.cfg`) import everything from the
"positronic.brain" package and perform some basic initialization:

```python
from positronic.brain import *

#      basedir=basedir looks weird, but we need it.
master(basedir=basedir, url='https://buildbot.example.com/')

worker('my-first-worker', 'secretpassword')
worker('my-second-worker', 'anothersecretpassword')

with FreestyleJob('my-project', workers=['my-first-worker', 'my-second-worker']) as j:
    j.checkout('project', 'svn+ssh://svn.example.com/svn/project', 'trunk')
    j.command('make')
    j.command('make', 'check')
    j.command('make', 'packages')
    j.notify('dev1@example.com')
```
