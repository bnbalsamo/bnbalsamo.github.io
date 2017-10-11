#!/bin/sh
docker run -p 4000:4000 -v $(pwd):/srv/jekyll jekyll/jekyll jekyll build
