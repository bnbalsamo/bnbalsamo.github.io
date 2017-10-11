#!/bin/sh
IDENT=$(docker run -p 4000:4000 -d -v $(pwd):/srv/jekyll jekyll/jekyll jekyll serve --watch -D)
echo "Test server running on localhost:4000, watching for changes"
echo "Stop server with: docker stop $(echo -n $IDENT | cut -c -4)"
