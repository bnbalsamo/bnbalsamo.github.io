#!/bin/sh
docker run --rm -v $(pwd):/srv/jekyll jekyll/jekyll sh -c 'cd /srv/jekyll && mkdir _site && gem install minima && jekyll build'
