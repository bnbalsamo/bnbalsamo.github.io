# [bnbalsamo.github.io](https://bnbalsamo.github.io)

[![Build Status](https://travis-ci.org/bnbalsamo/bnbalsamo.github.io.svg?branch=master)](https://travis-ci.org/bnbalsamo/bnbalsamo.github.io)

Additional Functionalities

* ```python make_speaker_notes.py```: Produces speakernotes markdown pages from presentations - swap /presentations/ for /speaker_notes/ in the site url to get the speaker notes as a stand alone page.
* ```./make_pres.sh $1```: Make a presentation template named $1 in _presentations
* ```./make_post.sh $1```: Make a post named $1 in _posts
* ```./build_site.sh```: Builds the _site directory using a docker container
* ```./test_site.sh```: Mounts the _site directory and spins up a test instance using a docker container
* ```docker build . -t $1```: Builds a docker image tagged as $1 running nginx hosting the site.
    * Requires the _site directory exist.
    * resulting site can then be run with ```docker run -d -p 80:80 $1```, where $1 is the tag applied at build time
