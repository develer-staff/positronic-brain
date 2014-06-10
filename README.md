Positronic Brain
================

![Logo](logo.png)

Opinionated BuildBot workflow.


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

master(url='https://buildbot.example.com/',
       email_from='buildbot@example.com',
       title='Example Buildbot')

slave('my-first-slave', 'secretpassword')
slave('my-second-slave', 'anothersecretpassword')

FreestyleJob('my-project', slaves=['my-first-slave', 'my-second-slave']) \
    .checkout('project', 'svn+ssh://svn.example.com/svn/project', 'trunk') \
    .command('make') \
    .command('make', 'check') \
    .command('make', 'packages') \
    .notify('dev1@example.com') \
    .collect_artifacts()
```


Goodies
-------

* Increased readability and terseness of the configuration file with declarative configuration and
  judicious defaults.
* Configure the master + Web interface with one function call.
* A base class (`FreestyleJob`) which automatically configures change sources, schedulers and
  common build steps.
