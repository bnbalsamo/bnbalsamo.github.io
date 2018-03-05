#!/bin/sh
docker run --rm -v $(pwd):/srv/jekyll jekyll/jekyll sh -c 'cd /srv/jekyll && gem install minima && jekyll build'
