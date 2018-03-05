#!/bin/sh
docker run --rm -v $(pwd):/srv/jekyll jekyll/jekyll gem install minima \&\& jekyll build
