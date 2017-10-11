#!/bin/sh
docker run -v $(pwd):/srv/jekyll jekyll/jekyll jekyll build
