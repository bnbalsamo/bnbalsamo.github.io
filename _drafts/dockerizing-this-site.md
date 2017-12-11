---
layout: post
title: Dockerizing This Site
---

I am a **big** fan of [Docker](https://www.docker.com/).

If you have no idea what Docker is, I made a [presentation](https://bnbalsamo.github.io/presentations/docker_for_devs_part1.html#1) to introduce people to some basic concepts, and point them in the right direction for continued research.

When I started building this site with [Jekyll](https://jekyllrb.com/), which is what powers [GitHub Pages](https://pages.github.com/) (where this site is currently hosted), it occured to me that Jekyll is _exactly_ the kind of tool that lends itself to containerization and employing a couple of common Docker patterns with.

Jekyll provides a container image via Dockerhub [here](https://hub.docker.com/r/jekyll/jekyll/), so using it in a container is as simple as putting ```FROM jekyll/jekyll``` at the top of a Dockerfile, or running ```docker run -ti jekyll/jekyll bash``` from the CLI.

After some experimentation I've now got Docker and Jekyll wired up to make all the common tasks for writing posts, presentations, or new pages for this site completely painless, from development to deployment, and I honed my Docker-fu a bit in the process.

So, without further adieu, whether you want to apply similar dockerizations to your own Jekyll projects or just hone your Docker-fu with an example site, here's what I've done to make working with and deploying this site a breeze:

### Pattern 1) Development/Preview Server

I do most of my writing in [vim](http://www.vim.org/), and usually have it and some combination of browser windows open at any given time on my desktop. Vim is great for a lot of things, but one of those things is _not_ being a [WYSIWYG](https://en.wikipedia.org/wiki/WYSIWYG) markdown editor. Additionally, even with a markdown viewer, it would have been tricky, [fragile](https://en.wikipedia.org/wiki/Software_brittleness), and precisely the opposite of [DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself) to assemble my Jekyll templates into a separate static document so that I could keep checking up on how a blog post or presentation looked outside of my Jekyll environment. Luckily, Jekyll includes a preview server, which can dynamically reload when changes are made to content (thereby appeasing my need to hit save and check how my formatting looks every two sentences or so).

Thus, in order to use the Jekyll preview server (or, more generally, any development server) we need to leverage a few of Docker's capabilities:
- We need to get the data into a container, updating dynamically as we edit
- We need to get the container running the development server, looking at the data
- We need to expose the development server to our host, so we can access our preview

In order to get the data into the contianer, and maintain access to it on our own host, we leverage Docker's ability to mount host directories into containers, such that changes in the directories made on the host are also visible inside of the container. This is achieved via the ```-v``` argument to ```docker run```. This functionality works wonderfully here, but a word of warning - mounting host directories into containers permanently is usually a bad idea in production deployments, we'll get to what to do in that circumstance a bit later in this post.

Running the development server is precisely what Docker was built for, in order to accomplish that we just select the correct image (in this case ```jekyll/jekyll```) and provide it with the command we want to run (again, in this case, ```jekyll serve --watch -D```). Note that here we don't need to actually change the location Jekyll is looking for the data to be served, we can place our data in the default location when we mount our host directory into the container to simplify.

```docker run``` also allows exposing container ports to the outside world in several ways, which is how we'll access our development server. For our use case we'll bind a container port to a port on the host via the ```-p``` option. This option allows us to address the host on the supplied port number, and have the traffic pass through to a given container port.

Leveraging these capabilities we can create a container which runs in the background, serving up a preview of your site, dynamically updating each time you hit save (or ```:w```).

Putting it all together, we get this command:

```
$ docker run --name test_site -p 4000:4000 -d -v $(pwd):/srv/jekyll jekyll/jekyll jekyll serve --watch -D
```

That's quite a mouthful, so let's break it down

- ```docker run```: The CLI interface for running Docker containers
- ```--name test_site```: I like to give the container an easy to remember name, instead of using the automatically assigned identifier
- ```-p 4000:4000```: Jekyll, by default, serves the preview server up on port 4000, so we go ahead and bind the containers port 4000 to the hosts port 4000.
- ```-d```: Detaches the container from the terminal, so we can keep on typing away in the same window after starting the container.
- ```-v $(pwd):/srv/jekyll```: Mount the contents of this directory (aka, the output of the ```pwd``` command) into the container in the /srv/jekyll directory in the container. This is where the Jekyll preview server looks for your Jekyll environment by default.
    - I always run this command from the root of my Jekyll environment, if you weren't currently in your Jekyll environment root you could just replace ```$(pwd)``` with the absolute path to it.
- ```jekyll/jekyll```: The name of the container image to use, in this case pulled from the "jekyll" Dockerhub account and named "jekyll"
- ```jekyll serve --watch -D```: The Jekyll CLI command to fire up the preview server, watching for changes and publishing the contents of the _drafts/ directory as if it were a post.

After running that command I am a ```:w``` in vim, and a reload in my web browser from checking the formatting of a post, changes to any pages, template changes, etc at http://localhost:4000.


### Pattern 2) Build Container

Jekyll is essentially a build tool, which takes an input "slug" of some templates, metadata, and content, and builds a static output. This is a similar workflow to the way built/compiled languages handle ingesting source code and producing a built artifact to be run.

In order to accomplish this with Docker we need to...

- get the data we want built into the container
- run the build process
- get our built artifact out of the container

To get our data into the container we have two primary options:

1. Mounting the directory which contains the data into the container from the host
2. Copying the data into the container filesystem itself

Mounting the data into the container means that any changes which the build process may make to the data will also be made to the data on our host, which could be a good or a bad thing, depending on what the build process entails and what our end goal is.

Copying the data into the container means that the copy which is built won't effect the copy we maintain on our host, and also has the potential benefit of making the build container distributable, as it doesn't pre-suppose the data to be built exists on the host which will run the container.

Which method you should employ will be informed by what and how you are building. In our case, building a Jekyll site, distributability of the build process isn't a requirement, our build process doesn't produce anything except for the single artifact we _want_ to get out of the container, and we can use the same method we use to put data into the container to get the data back out of the container, so we will opt for mounting the data we want built into the container, rather than copying it.

Running the build process is handled by Docker, we just select the image to use and specify the build command, in our case ```jekyll/jekyll``` and ```jekyll build```, respectively.

In order to get our built artifact out of the container, typically, you would mount a host directory into the container at the target location of the build command. In our case, Jekyll builds into the same directory as we have mounted our data to be built, under the ```_site``` directory. Thus, we can get away with using just the volume mount we used to get data _into_ the container to also get the data _out_ of the container. This may vary with other build systems.

Putting all of that together, we get this command:
```
$ docker run --rm -v $(pwd):/srv/jekyll jekyll/jekyll jekyll build
```

Breaking it down:
- ```docker run```: The CLI interface for running Docker containers
- ```--rm```: Remove this container after it exits, we don't need to keep the build container around after we have the built artifact.
- ```-v $(pwd):/srv/jekyll```: Mount the contents of this directory (aka, the output of the ```pwd``` command) into the container in the /srv/jekyll directory in the container. This is where Jekyll looks for your Jekyll environment by default.
    - I always run this command from the root of my Jekyll environment, if you weren't currently in your Jekyll environment root you could just replace ```$(pwd)``` with the absolute path to it.
- ```jekyll/jekyll```: The name of the container image to use, in this case pulled from the "jekyll" Dockerhub account and named "jekyll"
- ```jekyll build```: The command we want to run inside of the container in order to produce our built artifact in the directory we have volume mounted from the host.

Running this command ingests my "source" (in this case, my Jekyll environment for this site), runs the build process within a container, writes the output into a shared directory so it is accessible by my host even after the container is removed, and then cleans up after itself. Leaving me with the built artifact to be run anywhere.


### Pattern 3) Deployment Container

With tools to develop and build our site we are left with a final question: How do we serve it?

Serving the Jekyll site is roughly analogous to installing any built artifact into a production environment capable of running it. In order to accomplish this with Docker we need to...

- Get the built artifact into the container
- Execute the built artifact using the appropriate tool

In order to get the data into the container, we again have two choices:

1. Mounting the data into the container
2. Copying the data into the container

In this case making our production image distributable is of _primary_ importance - that is to say, we should be able to run our container anywhere that Docker is run, on any host, in the cloud, across a Docker Swarm or a Kubernetes Cluster, etc. This means that unlike our development and our build containers, our deployment container shouldn't make any demands of the host it is run from (except, of course, that it be running Docker), so we must copy our data into the container filesystem itself.

Additionally, in the interest of making our deployment distributable, instead of exclusively using the ```docker run``` CLI interface to run our container, we'll create a container image that can be invoked either manually via the CLI or in orchestrated environments, and is itself a built artifact that can be executed by Docker.

Thus, the first step is to create an image which contains the tool(s) required to "execute" (serve, in our case) our built artifact, as well as the data that tool should act on.

Our very simple Dockerfile in order to create that image looks like this:

```
FROM nginx
COPY _site /usr/share/nginx/html
```

Notice here that we copy the contents of the _site directory directly into the default web root of the nginx server. This means we needn't (necessarily) change any of the nginx configuration variable in order to get the server serving our site.

With the above saved in a file named ```Dockerfile``` in the root of our Jekyll environment we can run the following command to build the Docker image:

```
$ docker build . -t my_site
```

Deconstructing this command yields...

- ```docker build```: The CLI interface for building Docker container images
- ```.```: The location to treat as the Docker build root
    - This assumes you are placing the Dockerfile and running the command from the Jekyll root, if not you would need to include the absolute path to the Jekyll directory here, and potentially the ```-f``` option to specify a different name for the Dockerfile, if it wasn't "Dockerfile"
- ```-t my_site```: Tags the image with a nice, easy to remember name, instead of a random name generated by Docker.


This creates an image which contains all of the required parts, minimally configured, to run an nginx webserver serving our built site. Deploying the site is now as simple as...

```
$ docker run -d -p 80:80 my_site
```

Dissecting this command yields...

- ```docker run```: The CLI interface for running Docker containers
- ```-d```: Detaches the container from the terminal, so we can keep on typing away in the same window after starting the container.
- ```-p 80:80```: Map port 80 on the host to port 80 in the container, the default port for HTTP connections to nginx (and almost all other webservers).
- ```my_site```: The nice human readable name we tagged our built image with in the previous step.

And, after running that command navigating to http://$yourHostOrDomainName should connect you to an nginx server serving the built Jekyll site!

### In Conclusion

Dockerizing this site has been tremendously helpful to me in working in a Jekyll-based environment, and I hope that this little walkthrough is helpful to you as well, either to make working within your own Jekyll environments more productive, or to help with learning a few common Docker patterns to apply to any environment.

To take a look at precisely how I employ this workflow feel free to have a look at [this site's GitHub repository](https://github.com/bnbalsamo/bnbalsamo.github.io) which contains a few scripts to save me some typing while performing the most common Docker operations I've gone over in this post.

I've also applied many of these patterns to other projects (most, if not all, of my [Flask](http://flask.pocoo.org/) based APIs are Dockerized). Feel free to have a look at what I've done (and/or what I'm up to currently) on my [GitHub profile](https://github.com/bnbalsamo).
