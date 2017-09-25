---
layout: presentation
title: Semantic Versioning
---


class: center, middle

# Semantic Versioning
## A Brief Explanation

---

# Semantic & Versioning 
**Definitions**

- **Version**: A particular form of something differing in certain respects from an earlier form or other forms of the same type of thing.
- **Semantic**: Relating to meaning in language or logic


.footnote[google.com]

---

class: center, middle

**Semantic versioning is using versioning to convey meaning.**

---

# Why?

- Unifies/standardizes versioning practices
- Meaning can be leveraged by...
    - Developers
    - Managers
    - Stakeholders
    - Users
    - Programs
- Sane dependency resolution

---

# How?

- **Version Numbers**
    - Version numbers provide the medium to convey the meaning

- **Standardization**
    - By standardizing the format and procedures for incrementing version numbers
        they become understandable to all participants in a project

- **Interfaces**
    - Provide a strict definition of what is being versioned.

---

# The Basics

- Version numbers are minimally composed of three numbers, separated by a "."
- Each segment of the version of the version number communicates a different
    kind of change when incremented.

**$MAJOR.$MINOR.$PATCH**
- **MAJOR**: The interface has changed
- **MINOR**: Additional interface functionality is available
- **PATCH**: A bugfix has been applied

---

# The Rules
- Must define an interface
- $X.$Y.$Z
    - No leading zeros!
- No changing releases after release!

---

# The Exception

Version < 1.0.0

.center[![The Wild West](http://images.mentalfloss.com/sites/default/files/goodbadhed.jpg?resize=550x370)]

---

class: center, middle

"This doesn't look like a complete specif--"

[http://semver.org/](http://semver.org/)

---

# Tooling 

[bumpversion](https://github.com/peritus/bumpversion)

```
bumpversion [options] part [file]
```

or a config file: .bumpversion.cfg

```
[bumpversion]
current_version = 0.1.0

[bumpversion:file:README.md]

[bumpversion:file:VERSION.txt]
```

.footnote[In python land the config can live in setup.cfg]

---

# Why bumpversion?

- Language agnostic
- Configurable
- Extensible
- Usable
- [Well Documented](https://github.com/peritus/bumpversion/blob/master/README.rst)
- Git awareness if thats your thing
    - Auto-tag, Auto-commit
        - works nicely with github auto-release options

---

class: middle

.center[More information and the complete specification at [semver.org](http://semver.org/)]

---

class: middle

.center[**Thank you**]

.center[Questions?]

.center[Brian Balsamo]
.center[brian@brianbalsamo.com]