#!/bin/sh
docker run --rm -v $(pwd):/srv/jekyll jekyll/jekyll jekyll build
