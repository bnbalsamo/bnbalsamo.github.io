#!/bin/sh
docker run -p 4000:4000 -d -v $(pwd):/srv/jekyll jekyll/jekyll jekyll serve --watch
echo "Test server running on localhost:4000, watching for changes"
