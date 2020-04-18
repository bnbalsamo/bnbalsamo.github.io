# [bnbalsamo.github.io](https://bnbalsamo.github.io)

[![Build Status](https://travis-ci.org/bnbalsamo/bnbalsamo.github.io.svg?branch=master)](https://travis-ci.org/bnbalsamo/bnbalsamo.github.io)

## Additional Functionalities

All functionality is exposed via [invoke](http://www.pyinvoke.org/).

All requirements stored in `requirements_dev.txt`.

Create a virtualenv, `pip install -r requirements_dev.txt` - you're good to go.

```
$ inv --list
Available tasks:

  export.dockerimage    Build and export the docker image to the local host.
  export.site           Build and export the site to the local host.
  export.speakernotes   Build and export speaker notes to the local host.
  new.post              Create a new post.
  new.presentation      Create a new presentation.
  publish.post          Publish a post from drafts.
  run.dockerimage       Run the docker image locally.
  run.testsite          Run the test site locally.
```
