#!/bin/sh
docker run --rm -v $(pwd):/srv/jekyll jekyll/jekyll sh -c 'gem install minima && jekyll build'
