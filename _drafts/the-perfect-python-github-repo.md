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
### pip
### Docker
#### .dockerignore
### DockerHub
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

```
$repo_name/
├── docs                   <--
│   ├── conf.py            <--
│   └── index.rst          <--
├── hello_world
│   └── __init__.py
├── LICENSE
├── README.md              <--
├── requirements_dev.txt
├── requirements.txt
├── setup.py
└── tests
    ├── test_$componentOne
    ├── test_$componentTwo
    └── test_$interfaces
```

Documentation... ah, documentation.

Documentation is a vital part of every code base that sees the light of day. It should, minimally:

- Tell people what your code does
- Tell people how to get your code to do that
- (if open source) Tell people how to work on the code

Programmers, in my experience, have a very contentious relationship with documentation. Everyone
loves when a project they want to use/implement/fork/etc has great documentation. Some legitimately
enjoy writing documentation, some tolerate writing documentation, and others claim that the only
kinds of grammar they know is [formal grammar](https://en.wikipedia.org/wiki/Formal_grammar).

I, personally, may not _love_ writing documentation, but I must admit I am a sucker for toying
with documentation systems, and I do get a warm fuzzy feeling when I see documentation I have
written pop out the other end of a documentation build system looking all crisp and professional.
(Are those clickable PDF table of contents links? Why yes they are.)

On this note, recent developments in documentation technology, DevOps, and collaboration tooling
have made writing documentation much less reminiscent of writing that final paper for a semester
long project in undergrad, and instead _much_ more like the act of writing code itself, if you
are willing to utilize some of the same practices as are employed in your code's build pipeline
in your docs build pipeline.

Documentation also shares another important feature with your code - parts of it are meant
for internal purposes, other parts might be meant for a more technical audience (eg, other devs
calling/forking your code), and finally parts of it serve as the "interface" to your project,
an entrypoint which should serve as a regular way to access functionality (in this case, the
'functionality' is explanation and reference).

Documentation meant for different purposes should usually be included in your repository (and
supporting services) in different ways - and keeping in mind how the final product will be
exposed via your repository, to both yourself and others, is vital in developing a documentation 
system that works for you. With that in mind, this is how I tend to organize my own documentation...

### README.{md, txt, rst, etc}

I tend to stick to markdown (.md) in my repository READMEs. This means that they're easy to edit,
easy enough to read in a text editor, and I can render them in a pinch just about anywhere via
either local tools or an online markdown editor (eg: just about any GitHub input field).

I consider the README to be the "home page" of my repository in terms of the documentation.
This means, instead of trying to cram _all_ the information into a single README.md file, I use
the README to show:

- my projects name
- it's 1-3 sentence description
- it's (human readable) version number
- any "big ticket" functionalities or defining properties
- some mile high metrics

depending on the project I sometimes also like to throw in...

- default installation procedures
- "Quick Start"
- a _tiny_ usage example
- etc

My guiding principal here is that the repository README should give enough information that
someone who ends up there will now what the project is, how to get it, how to use it minimally,
that it works, and where to get the more verbose documentation.

### docs/

Within my docs folder itself my person choice is to switch to using 
[rST](http://docutils.sourceforge.net/rst.html) markup utilizing 
[sphinx](http://www.sphinx-doc.org/en/master/) to build my documentation.

This results in (in my own opinion) slightly less readable docs in a raw text editor, but
_significantly_ more power for intra and inter-documentation linking, as well as more control
of formatting and better support/more bells and whistles for things like code blocks.

The sphinx documentation build system uses a configuration file defining build instructions
(conf.py). It can draw content from a variety of sources, but the most common is separate
rST pages in the docs directory linked in the index.rst file.

The other **big** difference in switching to sphinx is the tremendously helpful
[autodoc extension](http://www.sphinx-doc.org/en/stable/ext/autodoc.html). Autodoc
will extract specially formatted comments, as well as all docstrings, from your code and build
documentation from them. This means that all of your documentation regarding things like
function behavior, arguments, argument types, return values, etc stays in one place: the code.
Once you develop the habit of writing a docstring for functions off the bat, and taking the second
or two to edit the docstring any time you tweak a function, this becomes _invaluable_.

So, with autodoc handling most of the documentation from docstrings, whats left the include
in the docs/ folder itself? (Besides the obvious autodoc calls?) In depth documentation (aka,
deeper than you would want to go in the README.md) which doesn't fit nicely into a docstring.
I find that detailed installation procedures, usage examples beyond the bare minimum, links
to supporting projects/documentation, examples, etc, all find their ways into my docs/ folder
in  most projects. All of the autodocs then fit in nicely under an "API Reference" section.

### docstrings

Your code should have docstrings in it. Docstrings are little bits of documentation which
live in the source in order to provide in-code documentation for yourself or others while
you are working on the code base, as well as being the source of the output for the builtin
[help()](https://docs.python.org/3/library/functions.html#help) function. Minimally they provide
a brief description of the function, however, more documentation is (almost) always better.

I follow the following rules when generating a docstring, typically:

- (first line) One line description of function
- (optional, if first line not enough) a longer function description
- A list of arguments, their expected types, and brief descriptions of each arg
- A list of kwargs, their expected types, and brief descriptions of each kwarg
- An explanation of the return value of the function
- The return type of the function.

This has the effect of producing a reasonable default docstring within the source which,
when combined with some sphinx syntax, will produce the kind of documentation that most people
are familar with because it will resemble the 
[Python standard library docs](https://docs.python.org/3/library/index.html)

[PEP 257](https://www.python.org/dev/peps/pep-0257/) goes over basic docstring conventions,
though it obviously does not bias itself towards autodoc style rST docstring formatting.
Despite this, it does provide compatible recommendations I would highly recommend following
in order to keep your documentation well written, and your source readable.

In order to get pretty, linked documentation via autodocs I recommend reading over a general
reStructuredText tutorial, the 
[sphinx intro docs](http://www.sphinx-doc.org/en/stable/tutorial.html), and the docs for the
[autodoc extension](http://www.sphinx-doc.org/en/stable/ext/autodoc.html#module-sphinx.ext.autodoc).

I have some docstrings written in this style 
[in my flask_jwtlib source](https://github.com/bnbalsamo/flask_jwtlib/blob/master/flask_jwtlib/__init__.py), and I would also encourage you to seek out some examples from the stdlib in 
[the python source](https://github.com/python/cpython) as well as any other projects which
use rST to produce their documentation.

# Repositories and Continuous Integration Pipelines

One additional, potentially minor seeming, benefit of storing your source in a repository is
that it is available over the internet. While previously this may have been more of a convenience
than anything else (being able to access/work on your source from anywhere), now, with the power
of webhooks, the fact that your code is available on the internet, and your repository can
ping other services whenever there is an update, it is possible to build out tools which
react dynamically to your code changing to do all kinds of cool stuff.

## What's a Webhook?

Webhooks are really the crux that makes all of this dynamic functionality possible. Though they
have a fancy name, and a lot of people are talking about them in pretty technical contexts,
web hooks are pretty simple at their core.

Webooks typically have two parts: A 'broadcasting' end and 'receiving' end.

The 'broadcasting end' is an extension to a service that takes an address 
to shoot some information at when some event happens within that service. 

In the most basic cases "some event" is "pretty much anything" and "some
information" is information pertinent to the event that occured, along with an explanation
of what particular event occurred.

The 'receiving end' is some other service that is waiting to hear about events, and when
it receives information it performs some actions.

The nice thing here is that there is a clean 
[separation of concerns](https://en.wikipedia.org/wiki/Separation_of_concerns). The 'broadcasting'
end of the webhook just needs a target and then describes an event it knows about because
it occurred under it's purview. The 'receiving' end then parses an event description and enacts
whatever action falls under its purview.

Why is this a big deal? - Because it's an effective way to eliminate the need for 
[polling](https://en.wikipedia.org/wiki/Polling_system), thus making services where polling
would have been a bottle-neck _much_ more scalable and responsive.

## What's Continuous Integration?

Continuous Integration (or in some circles Continuous Delivery, or in others Continuous Integration
and Delivery, or in others Continuous Deployment, it all depends on what you consider to be being
integrated, deployed, delivered (in)to whatever else) is the use of (usually several) services
to perform some of the steps necessary to take code after some event (commit, merge, review, etc)
and move it further through the deployment pipeline.

In a personal project the deployment pipeline might look something like...

- You branch from master and create $FeatureBranch
- You write code in $FeatureBranch until the feature is complete, and
    no previous work has been broken (unintentionally) by any changes
- You submit a pull request against your master branch 
- You merge $FeatureBranch into master
- master is re-deployed to production at the next opportunity

in a work context there might be a few extra steps...

- $DevTeam branches from master creating $FeatureBranch
- $DevTeam works in $FeatureBranch until the feature is complete, and
    no previous/contemporaneous work has been broken (unintentionally) by any changes.
- $DevTeam submits a pull request for $FeatureBranch to be merged into master
- $FeatureBranch is reviewed by $ManagementTeam
- $FeatureBranch is reviewed by $QaTeam
- $FeatureBranch is reviewed by $SecurityTeam
- Once $ManagementTeam, $QaTeam, and $SecurityTeam all sign off, $FeatureBranch
    is merged into master by $ManagementTeam
- master is redeployed to production at the next opportunity

Your own branching policies, organizational charts, stakeholders, etc may differ, but you
get the idea. Deployment pipelines are how code goes from a feature request/bug report to 
a reality in a production system.

Both of these flows can seem daunting at first, but with the addition of some automation and
standardization it becomes possible to:

- Speed up feedback loops required for different parties to do their parts
- Keep people in the loop, and centralize 'canonical' communications as much as possible
- Automate large repeatable portions of the above workflows, either for all projects
    or in a project specific manner.

And that is what continuous integration is all about - speeding up the processes involved in
developing, testing, integrating, and deploying software (where appropriate) such that the
project can keep moving forward _continuously_ and incrementally instead of infrequently and
in leaps and bounds.

## Automated Tests

Implementing automated testing is by far one of the biggest changes I have ever made to my
own personal workflows, and it has _without a doubt_ made me a better programmer. It is
(almost) impossible to over-state it's usefullness once you've got it up and running in
your repository.

Earlier we went over including tests in your repository and why they're important, now we
can use CI technologies to run those tests on just about every event during the entirety of the
pipeline to be sure that nothing breaks anywhere along the way.

Did I say just about every event? I did.

- Commits
- PRs
- Merges
- You sneezed and maybe hit the keyboard with the source open
    - ```git add -u && git commit -m "sneezed" && git push```
- You wrote a new test
- You edited an old test
- It's lunch time
- You're back from lunch
- You feel like it

When's a good time to run your tests? All the time. Commit often.

Will your tests come back red sometimes? Yes.

\<aside\>

This will make your git log look like a log of messy development work (reality). 

Is it pretty and easy to follow? No - not always.

I (personally) think there is value in retaining all
of this information. If you disagree there are alternatives to committing often to fire up
tests, or there is always 
[rewriting history](https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History) to make things
cleaner in your master branch's git log. However, I find that the ease of committing often to run
tests for feedback, along with the benefits of committing often on its own, far outweigh the benefits of a 'clean' git log.

\</aside\>

The key here, is a good CI solution allows this testing to be going on all the time, in the
background, with no (or minimal) effort, providing feedback to you each time the tests run.
Sometimes you'll commit and expect your tests to be broken because development is in some
in-between state, other times you'll commit and expect them to pass. Both of those cases
provide valuable information both in the positive and negative cases which you'll be glad
you have when invariably there's some debugging to do.

### TravisCI

```
$repo_name/
├── docs
│   ├── conf.py
│   └── index.rst
├── hello_world
│   └── __init__.py
├── LICENSE
├── README.md
├── requirements_dev.txt
├── requirements.txt
├── setup.py
├── tests
│   ├── test_$componentOne
│   ├── test_$componentTwo
│   └── test_$interfaces
└── .travis.yml             <--
```

## Automated Coverage
### Coveralls.io
## Automated Docs
### readthedocs.io
## Automated Deployment
# Github Goodies
## Issue, PR, etc Templates
## .gitignore
## Badges!
# Meta
## Scripts
## setup.cfg
# Conclusion
