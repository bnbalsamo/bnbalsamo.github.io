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
## Packaging
### Docker
#### .dockerignore
### pip
## Licensing
## Tests
### Local Coverage Metrics
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
