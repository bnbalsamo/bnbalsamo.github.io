---
layout:page
title: notes
---

---
---
---
---

Who doesn't love dictionary definitions?

You probably know what these terms mean separately,
but what do you get when you cram them together?

---

We make "version" a verb, versioning - that mystical thing
that version control systems do.

And then, and here's the key, we convey **meaning** beyond
"this thing changed" through the act of versioning.

---

Why?

So people know whats going on.

Developers, managers, stakeholders, users, dependencies - all of them like
to know "whats happening?" on a project, but all of them probably want some
different facet of that question answered.

Semantic versioning helps us do that.

---

How?

Version numbers are the medium - the thing we communicate through

Interfaces provide the answer to "What exactly are we versioning?"

What is your projects interface? Thats for you to decide!

In a web API it's probably the endpoints

In a library it's probably the objects, methods, functions, etc
you provide.

In a command line utility it's probably the CLI syntax.

We standardize this business, so everyone can glean the information
they're looking for from the version number.

---

The very basics: How we construct the medium

Version numbers are three parts: MAJOR[dot]MINOR[dot]PATCH

(you can tack more stuff on, and you've probably definitely
seen projects that do, but lets start with the basics here)

---

The basic rules

In order to version something you have to have something to version

Leading zeros are a pain, and everyone built tooling to avoid them

After you release a version people expect it to stay the same for a
variety of reasons

- sanity
- stability
- reusability
- security
- etc

---

Every rule has it's exception. With Semantic Versioning we keep
that encapsulated below version 1.0.0, the "Wild West" period
of the project.

Changes are probably happening fast at this point, and you can
assume that no one is using your project in production (or if they are,
they've accepted the risk).

You can use the MINOR and PATCH numbers or you can ignore versioning at this
point, whatever works for you.

---

The contents of this presentation, as you've undoubtably noticed, isn't a full specification.

To avoid copy pasting the whole thing, here's the link.

A jaunt through this should clear up ambiguities, edge cases, extensions, and the like

---

So - this all seems well and good, but you don't want to have to keep
track of an entire specification, and how it applies to each of your projects,
entirely in your head.

Enter bumpversion

bumpversion is a handy little utility (written in python) that takes care of the
details for you, after you take the time to set it up once

---

Bumpversion has a couple of great features that make it hard to justify
not using on almost any project.

- You can use it with any language
- it's configurable enough to handle most anything
- It's dead simple to use once you've set it up
- It's not hard to learn how to set up
- It ties in with the tools you're already using
    - or probably should be using

---
---
