#!/bin/sh
docker run --name test_site -p 4000:4000 -d -v $(pwd):/srv/jekyll jekyll/jekyll sh -c 'cd /srv/jekyll && gem install minima && jekyll serve --watch -D'
echo "Test server running on localhost:4000, watching for changes" && \
echo "Stop server with: docker stop test_site"
