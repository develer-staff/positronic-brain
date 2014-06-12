Positronic Brain
================

<img align="right" src="logo.png"/>

> *Opinionated BuildBot workflow.*

[![Build Status](https://travis-ci.org/develersrl/positronic-brain.svg?branch=master)](https://travis-ci.org/develersrl/positronic-brain)

We abstract away BuildBot configuration with an embedded DSL (in Python) so that a complete
workflow can be expressed with few lines dropped in your `master.cfg`.

Adding a positronic brain to your BuildBot gives you the following:

* Out-of-the-box sane defaults for your BuildBot master.
* Automated emails sent to developers after a build failure.
* Automated emails sent to administrators for all builds on all projects.
* Automatic configuration of Change Sources and Schedulers when you add a source checkout
  step to a build (SVN only, for now).
* Automated archiving of artifacts on the master after a successful build.


Installation
------------

This package is not being published to PyPI, so for the time being you have to install it by
running:

    pip install https://github.com/develersrl/positronic-brain/archive/master.zip#egg=positronic-brain

Please note that this package depends on a very specific version of the BuildBot master and you
have to make sure to have it installed first (see [requirements.txt](requirements.txt) for more
details).


Usage
-----

In your BuildBot master configuration file (`master.cfg`) import everything from the
"positronic.brain" package and perform some basic initialization:

```python
from positronic.brain import *

master(url='https://buildbot.example.com/')

slave('my-first-slave', 'secretpassword')
slave('my-second-slave', 'anothersecretpassword')

with FreestyleJob('my-project', slaves=['my-first-slave', 'my-second-slave']) as j:
    j.checkout('project', 'svn+ssh://svn.example.com/svn/project', 'trunk')
    j.command('make')
    j.command('make', 'check')
    j.command('make', 'packages')
    j.notify('dev1@example.com')
```
