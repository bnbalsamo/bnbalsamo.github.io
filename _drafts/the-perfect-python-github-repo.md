---
title: The Perfect Python Github Repository 
layout: post
---

# Disclaimer

This post goes over a lot of stuff you can do with git, GitHub, and several other tools. 
But, right off the bat, I want to say this:

**USE VERSION CONTROL FOR YOUR SOURCE CODE**.

Even if you don't have any interest in implementing anything else discussed in this post -
even if you get this far into this post and decide to stop reading because you feel like
people who use boldface are yelling at you (Don't we all?). Please, if you aren't currently
using version control, git or otherwise, for your source code, [start](https://guides.github.com/activities/hello-world/).

Using version control teaches good habits, saves you from catastrophes, and makes collaboration
on programming projects possible without going absolutely insane.

Perhaps in the future I'll write a post singing the praises of version control itself, but until
then, just take my word for it.

With that out of the way, let's move on to the...

# Introduction

Maybe you're just learning Python, or you've been writing it for a while now, and you decide
to have a look at this 'Github' thing that appears to come up every once in a while. So, you
google your favorite project name + "github" and...

> Woah! Parts of this look recognizable, there's definitely code in here, but whats all this
> other stuff?
>
> -- You, hypothetically

Version control systems, and GitHub in particular (because it's accessible, full-featured, 
frequently used, and frequently supported by integration authors) provide an excellent 
backbone for automating certain tasks, enforcing best practices, displaying information, 
collecting and correlating feedback, and storing _everything_ that pertains to your project,
not just the source.

In this post I intend to break down what I consider (at the moment) to be a _perfect_ GitHub
setup. 

Is this setup perfect for _every project_? - Nope

Is this setup perfect for _every person_? - Also nope

But, I find it to be the perfect baseline to work from, tweaking on a per project basis,
and though you may need to tweak, adjust, omit, add, etc to what I describe in this post, I
hope it helps to teach you about some of these tools, or plan your own perfect repository
structure that works for you and your projects.

So, lets break down the parts of a perfect repository...

# Parts of a Repository
## Code

Duh. The source code of your project should be of your repository. All of it.

In Python-land there are two primary ways to do this.

One looks like this:
```
$repo_name/
└── hello_world.py
```

and the other looks like this:
```
$repo_name/
└── hello_world/
    └── __init__.py
```

The first method is packaging as a Python _module_, while the second is packaging as a Python
_package_. Both of these options are equally valid, and you can pick the one that works for you,
however I'll say this on the subject:

The downside of starting your project as a module and needing to expand it to a package is making
several changes, potentially to code (imports) and packaging configurations.

The downside of starting your project as a package and never needing to leverage the additional
namespaces it affords you is... you have one extra directory in your repository.

Personally, I like to standardize, and so I (nearly) always opt to begin new projects as a package,
rather than a module. This allows me to be ready for the project to grow in scope, 
as well as to be able to leverage the organizational potential provided by the package format.
It also means during development I can (usually) avoid drastically modifying my packaging 
configuration or import structures.

One more note:

> But, I put the database password in the conf--

Stop. No. Bad. If your configuration is mixed with your logic you're 
[doing it wrong](https://12factor.net/config). Abstract configuration away from
the logic, include a dummy configuration in your repository if you must.


## Versioning

> Wait a second, I'm already using version contr--

Correct, but version control systems have two main target audiences

1. Developers working on the source
2. Machines

It's a fairly good bet that the majority of the people looking at your project don't fall
into one of those two camps (_though I am on to you, replicants_).

Git version identifiers, for example, look like this: ```221d0ad8239b8a856a0607949d9c344788f69169```

These things (they're hashes, actually) get resolved via the use of an index in order for git to
keep track of versions in as detailed a manner as it does.

So, in order to convey more relevant information faster to the majority of your audience, you
should implement a simpler versioning scheme on top of this.

Here is where we get the version numbers people are used to seeing, 1.0, 1.0.0, 42.5.9, etc.

How _exactly_ you apply human-readable versioning to your project is up to you, but I heartily
recommend taking a look at [Semantic Versioning](https://semver.org/) to save yourself the trouble
of coming up with your own method of communicating version information quickly to a human audience.

I employ Semantic Versioning in my own projects, and have even written a [quick little tutorial
presentation/elevator pitch for it]({{ site.baseurl }}{% link _presentations/Semantic Versioning.html %}).

Alright, so we're going to implement a more human-readable version number - where do we put it?

Probably a couple of places
- the code itself
    - It is sometimes import for your code to know what version it is
    - It is often times important for your code to be able to report to
        other parties/code what version it is
- the documentation
    - Where human actors will most likely look for it
    - So people can be sure the documentation they are looking at pertains
        to the code they are running/want to run.
- the packaging metadata 
    - So other packaging systems/package managers can display it
- etc

Documentation and packaing metadata are both covered a bit later in this post.

Tools like bumpversion (detailed in my tutorial) make it trivial to include this valuable
information in a variety of useful places, all while keeping it in sync and correctly
delivering information about your code. 

## Dependencies

> If I have seen further it is by standing on the shoulders of Giants.
>
> -- Isaac Newton

When writing a package or module often you depend on other packages or modules 
for functionality, these packages or modules are called dependencies.
Dependencies are referenced by your code, you import them,
but they don't necessarily exist in the Python environment without some intervention by the user.

Python provides two 'common' ways of dealing with dependencies, and though the differences between
them are hard to spot on the surface, I recommend implementing both in your repositories.

### setup.py

```
$repo_name/
├── hello_world/
│   └── __init__.py
└── setup.py         <--
```


We'll discuss ```setup.py``` in detail in the packaging section, but for now let's focus on
exclusively one array in there ```install_requires```.

When packages are added to the ```install_requires``` array and they don't already exist in the
Python path [setuptools](https://setuptools.readthedocs.io/en/latest/) will retrieve the packages.
You specify requirements using [specially formatted strings](https://setuptools.readthedocs.io/en/latest/setuptools.html?highlight=install_requires#declaring-dependencies).

Despite the fact that you _can_ leverage quite a bit of control here, I recommend instead that
you don't. Instead in setup.py I _only_ specify package names. Thus, for me, setup.py is a kind
of "sanity check" before my code is installed - being sure that all of my dependencies are in place
already before it is run (we'll get to that in just a moment). The fact that 
```python setup.py install``` can install packages is, at this point, more a kind of 
"fall back" than a feature. This is only because failing loudly at install time isn't
an option, and the alternative would be run time exceptions.

In certain cases, it might even be a misfeature, rather than a fallback, but because
```python setup.py install``` produces such verbose output on downloading a package, and because
(in my own repositories) setup.py not finding a package is an error case, I figure verbosely
experiencing an error case (with some potential to still be working despite it) is preferrable
to not knowing that an error case ever existed until runtime (when an ```ImportError``` is raised).

So, if we're using setup.py as a 'sanity check' to be sure that our packages exist in the
environment, what are we actually using to download them?

### pip and requirements.txt

```
$repo_name/
├── hello_world
│   └── __init__.py
├── requirements.txt  <--
└── setup.py

```

[pip](https://github.com/pypa/pip) is a tool built specifically for installing python packages,
which includes dependencies. It supports a wide variety of input specifications (CLI, files, pipes,
etc) and a gives a tremendous amount of control over the particularities of installing
dependencies. 

This makes it ideal for explicitly specifying dependencies, package names, download locations,
specific versions, etc, in order to _actually_ download and install them.

Remember - if a package is specified just by package name in ```setup.py``` and it already exists
in the Python environment, it won't be redownloaded. Thus, we can explicitly set requirements in
a requirements.txt file, use the increased control granted to us by pip in order to get _exactly_
the package we want, and then have ```setup.py``` check that we have everything we mean to (by
watching the output, and being sure nothing new is downloaded).

This _slightly_ complicates the install procedures from source, as now instead of just a single
```bash
$ python setup.py install
```

you have to run
```bash
$ pip install -r requirements.txt
$ python setup.py install
```

but, in my opinion, this is worth it in order to have fine grain control over the dependency
resolution process.

### Other Requirements Files

```
$repo_name/
├── hello_world
│   └── __init__.py
├── requirements_dev.txt  <--
├── requirements.txt
└── setup.py
```

All of my projects include one more requirements file: ```requirements_dev.txt```. This
requirements file includes all of the dependencies (if there are any) exclusive to running
tests, as well as a few handy utilities for working with the packaging process itself. This
allows for developers to just toss in one more step in order to work on the code:

```bash
$ pip install -r requirements_dev.txt
$ pip install -r requirements.txt 
$ python setup.py develop
```

This also has the nice side effect, assuming you run ```pip install -r requirements_dev.txt```
first, that you can clobber dependencies in your development environment with development versions,
while leaving the dependencies for the stable version untouched.

In this case your ```requirements_dev.txt``` is a bit more verbose, including the 'development'
versions of all of your dependencies, and to set up you run

```bash
$ pip install -r requirements_dev.txt
$ python setup.py develop
```

Just be sure to remember to updated your ```requirements.txt``` before pulling into master!

### Further Reading

Don't take my word for it, this is just one way to approach documenting dependencies in
a Python GitHub repository - there are plenty more and plenty of shades of gray. I recommend
reading the following two articles, to get an understanding of Python dependency handling:

- [setup.py vs requirements.txt @ caremad.io](https://caremad.io/posts/2013/07/setup-vs-requirement/)
- [install_requires vs Requirements files @ packaging.python.org](https://packaging.python.org/discussions/install-requires-vs-requirements/)


## Packaging
### Docker
#### .dockerignore
### pip
## Licensing

```
$repo_name/
├── hello_world
│   └── __init__.py
├── LICENSE               <--
├── requirements_dev.txt
├── requirements.txt
└── setup.py
```

Licenses are important. 

I'm not a lawyer. 

[Pick the right license](https://choosealicense.com/licenses/). 

Include it with your source in a ```LICENSE``` file in the root of your repository, and abide by any license requirements in your source code.

## Tests

```
$repo_name/
├── hello_world
│   └── __init__.py
├── LICENSE
├── requirements_dev.txt
├── requirements.txt
├── setup.py
└── tests                   <--
    ├── test_$componentOne  <--
    ├── test_$componentTwo  <--
    └── test_$interfaces    <--
```

Your repository should contain tests, no ifs, ands, or buts. 

Tests assure you, as well as others, that software will
provide certain functionalities and behave according to certain constraints. The details
of tests are many and nuanced, and beyond the scope of this post. 

Python has a variety of testing frameworks, I'll not try to enumerate all of them here, but I
encourage you to go out and find the ones that will work best for you, and to utilize one of them
in order to embed provable assertions of functionality into your repository.

My own personal choice here is a combination of good ol' [unittest](https://docs.python.org/3/library/unittest.html)
straight out of the standard library in combination with [pytest](https://docs.pytest.org/en/latest/)
(which plays nicely with unittest out of the box).

(We'll get to more exciting kinds of testing a bit further down, in the "Automated Tests" section)

This allows for storing all of the tests outside of the code in a modular fashion. Then, when it
comes time to run tests, a simple ```py.test``` in the repository root will run all your tests for
you.

### Local Coverage Metrics

So, you've got some tests, and they're all passing, but those pesky users keep finding bugs!

Here-in lies a critical (and too often forgotten) component of software testing - coverage metrics.

Coverage metrics are a measure of how much of your code is _actually_ tested by your tests, most
of the time defined as "lines that were executed at some point while your unit tests ran".

To state the obvious, lines of code that aren't run during your tests aren't tested - and so can
contain those pesky bugs that crop up in releases _even though_ the tests came back green.

There are a variety of methods and tools for measuring coverage, but my tool of choice here
is a handy python tool called [coverage.py](https://coverage.readthedocs.io/en/coverage-4.5.1/).

This tool allows you to wrap your calls to your tests such that coverage runs the tests while
also inspecting them and the code you are testing - all while generating metrics about what
is called and what isn't.

To get setup you'll need to ```pip install coverage``` or (if you've gone with my 
```requirements_dev.txt``` type approach) go ahead and add coverage to your development dependencies.

After that, instead of using...

```bash
$ py.test
``` 

to run your tests, instead use...

```bash
$ coverage run -m py.test
```

and....

Your tests ran but there's to other output?!

Not quite - one of the strengths of ```coverage.py``` is that it isn't tightly coupled to reporting
it's results in a single output format - instead it stores some stats in a file (in the
directory in which it was run) called ```.coverage``` - this file is then interpretted by coverage
itself, or other tools, in order to present the coverage metrics to you. For a full explanation
of the available reporting formats see the docs, but two handy formats to know off the bat are...

```
$ coverage report
```

which will dump a minimal report straight into your terminal, and...

```
$ coverage html
$ firefox htmlcov/index.html
```

which will pop open a browser window with some stats, and a nice file browser type web interface
which will allow you to open files and see (highlighted in red) any lines which are not executed
by your tests.

#### A Word on Metrics

Different folks have different opinoins on coverage numbers (and testing in general) but you're
reading my blog so now I get to subject you to part of mine:

100% reported coverage by a single coverage tool, eg ```coverage.py``` or a CI solution, isn't _that_
important.

> WHAT?!? But untested code is broken code!

Yes, correct. 

However, I have seen many a project, in pursuit of 100% test coverage reported by
tool $x, write tests that are _completely unreadable_. Tests are exactly as useful as they
are understandable to developers, tests should be understable as a promise of functionality
or a constraint of some sort.

Thus, some tests are more appropriately run in different contexts if including them in Python
unit tests results in too much cruft _just to run a test_ when in reality that functionality
will never occur from within a python environment.

Almost all of my web applications sit at somewhere below 100% as reported by coverage, because
I usually have a _second_ set of tests, tests which are a hassle to write in the python context,
written in bash. The tests in bash don't involve any of the complication of setting up mocks,
or fixtures, or what have you, instead they are (often) just a lot of cURLs against a flask debug
server (or, if possible, a complete production-esque deployment).

What does this mean?

- My line coverage numbers from unit tests aren't 100%
- My tests are _more readable_
- My functionality is _equally as tested_
- Occassionally I have to manually read a coverage report to be _absolutely sure_ that what
    isn't covered by unit tests is covered by bash tests

In my opinion this trade off is worth it, as opposed to convoluting tests and bending over
backwards in order to get a 100 to appear in a green box in my README.

## Docs
### README.{md, txt, rst, etc}
### docs/
# Repositories and CI Pipelines
## Automated Tests
## Automated Coverage
## Automated Docs
## Automated Deployment
# Github Goodies
## Issue, PR, etc Templates
## .gitignore
## Badges!
# Meta
## Scripts
## setup.cfg
# Conclusion
