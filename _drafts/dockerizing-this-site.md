---
layout: post
title: Dockerizing This Site
---

I am a **big** fan of [docker](https://www.docker.com/).

If you have no idea what docker is, I made a [presentation](https://bnbalsamo.github.io/presentations/docker_for_devs_part1.html#1) to introduce people to some basic concepts, and point them in the right direction for continued research.

When I started building this site with [jekyll](https://jekyllrb.com/) it occured to me that jekyll is _exactly_ the kind of tool that lends itself to containerization and employing a couple of common docker patterns with.

The [jekyll installation docs](https://jekyllrb.com/docs/installation/) suggest installing jekyll via RubyGems, and jekyll is also available in most distributions package managers, but I tend to like to keep my systems relatively clean, and also tend to like to be able to work from anywhere as quickly as possible. Docker is already such an important part of my toolbelt that I install it just about anywhere as part of my initial workspace setup, so having it on hand is much more likely than having a functioning Ruby build environment where-ever I am working from. These facts, in combination with the fact that I never need jekyll for tasks outside of the context of managing this site, make it a prime candidate for running containerized.

Jekyll provides a container image via dockerhub [here](https://hub.docker.com/r/jekyll/jekyll/), so using it in a container is as simple as putting ```FROM jekyll/jekyll``` at the top of a Dockerfile, or running ```docker run -ti jekyll/jekyll bash``` from the CLI.

After some experimentation I've now got docker and jekyll wired up to make all the common tasks for writing posts, presentations, or new pages for this site completely painless, from development to deployment, and I honed my docker-fu a bit in the process.

So, without further adieu, whether you want to apply similar dockerizations to your own jekyll projects or just hone your docker-fu with an example site, here's what I've done to make working with and deploying this site a breeze:

### Pattern 1) Development/Preview Server

I do most of my writing in [vim](http://www.vim.org/), and usually have it and some combination of browser windows open at any given time on my desktop. Vim is great for a lot of things, but one of those things is _not_ being a WYSIWYG markdown editor. Additionally, even with a markdown viewer, it would have been tricky, fragile, and the opposite of [DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself) to assemble my jekyll templates into a separate static document so that I could keep checking up on how a blog post or presentation looked outside of my jekyll environment. Luckily, jekyll includes a preview server, which can dynamically reload when changes are made to content (thereby appeasing my need to hit save and check how my formatting looks every two sentences or so).

One of the great things docker allows for is mounting host directories into containers, such that changes in them made on the host are also made inside of the container via the ```-v``` argument to ```docker run```. ```docker run``` also allows exposing container ports to the outside world by binding them to host ports via the ```-p``` option.

Leveraging these capabilities in combination with jekylls built-in preview server which dynamically rebuilds and serves content on changes to files in the jekyll environment you can create a container which runs in the background, serving up a preview of your site, dynamically updating each time you hit save (or ```:w```)

In order to do just that, I use this command:

```
docker run --name test_site -p 4000:4000 -d -v $(pwd):/srv/jekyll jekyll/jekyll jekyll serve --watch -D```

That's quite a mouthful, so let's break it down

- ```docker run```: The CLI interface for running docker containers
- ```--name test_site```: I like to give the container an easy to remember name, instead of using the automatically assigned identifier
- ```-p 4000:4000```: Jekyll, by default, serves the preview server up on port 4000, so we go ahead and bind the containers port 4000 to the hosts port 4000.
- ```-d```: Detaches the container from the terminal, so we can keep on typing away in the same window after starting the container.
- ```-v $(pwd):/srv/jekyll```: Mount the contents of this directory (aka, the output of the ```pwd``` command) into the container in the /srv/jekyll directory in the container. This is where the jekyll preview server looks for your jekyll environment by default.
    - I always run this command from the root of my jekyll environment, if you weren't currently in your jekyll environment root you could just replace ```$(pwd)``` with the absolute path to it.
- ```jekyll/jekyll```: The name of the container image to use, in this case pulled from the "jekyll" dockerhub account and named "jekyll"
- ```jekyll serve --watch -D```: The jekyll CLI command to fire up the preview server, watching for changes and publishing the contents of the _drafts/ directory as if it were a post.

After running that command I am a ```:w``` in vim, and a reload in my web browser from checking the formatting of a post, changes to any pages, template changes, etc at http://localhost:4000.


### Pattern 2) Build Container

Jekyll is essentially a build tool, which takes an input "slug" of some templates, metadata, and content, and builds a static output. This is a _very_ similar workflow to the way built/compiled languages handle ingesting source code and producing a build artifact to be run.

### Pattern 4)

# Use Cases
- Viewing the site while writing (developing/previewing/testing)
- Building the static site (creating a build artifact)
- Hosting the site (installing the build artifact in a system)

An explanation of dockerizing (simple) jekyll sites, as well as how I use Docker with github pages
