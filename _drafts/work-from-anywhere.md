---
title: How I Work From Anywhere with mosh, tmux, git, and stow
layout: post
---

I configure my workspaces this crazy way. It might not be for everyone, but it works for me,
and I think it has some substantial benefits:

- It lets me work in a similar workspace no matter what host I'm on
- It lets me tweak/expand/improve all of my workspaces in one go
- It speeds up my ramp up time when I need to start working on a new host.
- It eliminates that tremendously irritating week long period of trying to run
  applications that aren't installed, hit hotkeys that aren't configured, and
  run bash aliases that aren't defined.

Overall, I want to work in familiar workspaces no matter the host I'm actually working
from. I think there are two major strategies to accomplish this:

* Go to a workspace I've already configured.
* Bring my configurations into the new workspace. 

Both of these strategies tend to be useful in different circumstances:

If I'm working on an open source project from lackluster hardware, or on a machine I'm only
using briefly, it makes more sense to **go to** a workspace I've already configured. 

If I'm working on proprietary code using a client supplied laptop I'll be using regularly 
it makes sense to **bring my configurations to** this new workspace.

In order to accomplish either of these strategies I use a couple of ubiquitous tools and
battle tested workflows. While there are several excellent blog posts (which I've linked
to later in this post) about different parts of this setup I don't think I've seen a single 
post or tutorial which ties them all together - so I'm giving it a go.

## Prerequisite: Ditch the GUI 

I've found that GUIs and GUI applications violate several criteria for setting up
a modular workspace that lends itself to being easily distributed to different environments, or
easily accessed from a remote environment:

- GUIs tend to behave poorly when used over networks, whether accessed via
  something like X forwarding or VNC.
- GUIs have many (usually heavy) requirements, which means they take more time to install,
  and may not be easy/appropriate to install in certain environments. (Don't be the guy that installed X
  on the headless Debian server)
- GUI applications are less consistent in where and how their configuration files are stored.
- GUI applications tend to have fewer synergies with each other, and follow the 
  [Unix philosophy](https://en.wikipedia.org/wiki/Unix_philosophy) more loosely in an attempt
  to wrap more functionality into the same application.

For these reasons, among others, I build my workspaces primarily with CLI applications. 

## Strategy 1: Go to Our Workspace

"Going somewhere" on the *nix CLI is a standard procedure. It's usually accomplished via
[SSH](https://en.wikipedia.org/wiki/Secure_Shell), and nearly every *nix system has a [CLI 
ssh client](https://linux.die.net/man/1/ssh) installed by default. In order to go to a workspace
I configure an SSH server on the host that contains the workspace. I'll not go so far as
to include a tutorial on installing and configuring a SSH server in this blog post, because there are
[plenty](https://help.ubuntu.com/community/SSH/OpenSSH/Configuring) 
[of](https://wiki.debian.org/SSH#Installation_of_the_server)
[them](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-16-04)
[already](https://wiki.archlinux.org/index.php/OpenSSH#Installation).

### I'm There, Now What?

SSHing into a server gives me a CLI interface on that host. I'm _there_ but I need some tools that
serve standard needs in order to get work done:

- [Bash](https://en.wikipedia.org/wiki/Bash_(Unix_shell)) fills the slot of a task 
  launcher and file system explorer. It's the interface I see when I "land" on the remote host.
- [git](https://git-scm.com/) provides access to version control repositories
- [tmux](https://github.com/tmux/tmux) can act as a window manager, providing different "windows"
  to open new terminals or applications in.
- [vim](https://www.vim.org/) is my editor of choice, giving me the ability to edit files. 

Beyond the basics I use a variety of other tools depending on the specific work
I'm trying to get done.

This works fine most of the time, but SSH has some annoying behaviors:

- it disconnects when ever I lose network access and doesn't
  automatically reconnect. 
- it kills foreground processes if I disconnect
- it blocks if I start a long running process in the foreground, and I have to open a new (local)
  terminal instance and start a new SSH connection to keep working.

[mosh](https://mosh.org/) and [tmux](https://github.com/tmux/tmux) to the rescue! 
 
### mosh

Mosh sits on top of SSH and provides  a near identical interface to ssh + some nice benefits:

- the ability to reconnect after sleeping/hibernating whatever local host I'm on, or roaming between
  different wifi networks.
- some basic persistence, so my foreground processes don't die if my local host loses connection.

Mosh is easy to setup, it installs just like any other application, is available in most Linux
distributions' package managers, it doesn't require any privileged code execution (sudo),
and it doesn't require a daemon. Putting all of that together, it means that if SSH is already
running on the host mosh can be installed and utilized entirely from userland on both the local
and remote hosts.

### tmux

Tmux, in addition to making a great terminal based window management solution, is also a [terminal
multiplexer](https://en.wikipedia.org/wiki/Terminal_multiplexer). While mosh provides the ability
to painlessly reconnect to SSH sessions and keeps foreground processes from being killed in the event that I
lose connection to the remote server, it doesn't provide the kind of fine grained manual control
of session persistence that a full blown terminal multiplexer does. Tmux also provides the ability to run
multiple virtual terminal windows within a single "real" terminal window - meaning that long running process
in the foreground can run happily while I open another tab or split and continue working.

The interplay between mosh and tmux can be a bit confusing off the bat, and getting them both
configured and working together in harmony (and utilizing them efficiently) can be tricky.
[This excellent blog post](https://blog.filippo.io/my-remote-shell-session-setup/) goes over configuring
this portion of a robust remote workspace setup with mosh and tmux working together, so I'll avoid 
reiterating its content here.

With this setup, I can use any host's ssh client, or install the mosh client, and
travel to my own pre-configured workspace from anywhere!

## Strategy 2: Bring My Configurations to ME

The majority of tools are only an ```apt-get install```
or ```git clone```  away from any machine though. So, if it makes sense to install software on the local host
(or if I can't use a remote host for whatever reason), why not bring my configurations to me rather than
going to my configurations.

Nearly all well behaved CLI tools can be configured via 
[dotfiles](https://en.wikipedia.org/wiki/Hidden_file_and_hidden_directory#Unix_and_Unix-like_environments),
configuration files that live in the home directory and start with a "." so that they don't clutter up
the default ```ls``` output. 

The majority of the "hard" work of setting up a workspace is done in the dotfiles
that contain their configuration (and any personalizations/tweaks). These files are plaintext, 
and in order to "bring my workspace to me" I need to distribute them to multiple hosts and keep them in sync.

### git

Distributing and syncing text files between multiple multiple workspaces sounds _a lot_ like a workflow 
that every developer is well acquainted with - distributing source code. With that in mind  the perfect 
tool for bringing dotfiles to me regardless of what host I'm working on is readily apparent: 
[git](https://git-scm.com/)!

### stow

But, home directories aren't source code. There are a multitude of reasons not to 
put a home directory under version control:

- It often contains large files
- It can contain caches, indices, and other host specific information
- It frequently contains passwords, secrets, and other private information
- etc

Given these points in combination with the relatively disasterous potential outcomes of a mistaken
git commit it's unreasonable to attempt to manage a git repository of a home directory using tools
like ``.gitignore``` files.

These issues are only compounded if I use a public repository, which is desirable so that 
my dotfiles can be accessed from anywhere (ie, any host I happen to be working from). 

Enter [GNU Stow](https://www.gnu.org/software/stow/). Stow is a simple utility at it's heart. It takes
files (or directories) from a directory below the current working directory and symlinks them in the 
parent directory of the current working directory. For example...

```bash
$ mkdir -p /tmp/fake_root/stow_example/some_stuff
$ mkdir -p /tmp/fake_root/stow_example/other_stuff
$ touch /tmp/fake_root/stow_example/some_stuff/foo.txt
$ touch /tmp/fake_root/stow_example/other_stuff/bar.txt
$ tree /tmp/fake_root/
/tmp/fake_root/
└── stow_example
    ├── other_stuff
    │   └── bar.txt
    └── some_stuff
        └── foo.txt

3 directories, 2 files
$ cd /tmp/fake_root/stow_example
$ ls
other_stuff  some_stuff
$ stow some_stuff/
$ tree /tmp/fake_root/
/tmp/fake_root/
├── foo.txt -> stow_example/some_stuff/foo.txt
└── stow_example
    ├── other_stuff
    │   └── bar.txt
    └── some_stuff
        └── foo.txt

3 directories, 3 files
$ stow other_stuff/
$ tree /tmp/fake_root/
/tmp/fake_root/
├── bar.txt -> stow_example/other_stuff/bar.txt
├── foo.txt -> stow_example/some_stuff/foo.txt
└── stow_example
    ├── other_stuff
    │   └── bar.txt
    └── some_stuff
        └── foo.txt

3 directories, 4 files
``` 

Stow allows me to put a directory in my home directory (called, appropriately, `dotfiles`), put
_that_ directory under version control, divide dotfiles and configuration file hierarchies up into 
directories per application in that directory and then use stow in order to symlink those files 
into my home directory. If that sounds a little confusing feel free to take a look at 
[my own dotfiles repo](https://github.com/bnbalsamo/dotfiles) to see what I'm talking about.

This works for single files (e.g.: ```.bashrc```) and for applications whose configuration 
live in the ```.config``` directory, or in dotfile directories (eg: ```.vim/```). 

Additionally, certain utilities (pyenv, for example) can live entirely within the home directory. 
With a conditional or two in ```~/.bashrc`` it is possible to dynamically activate tools if they've
been "unstowed", which can be very powerful. I do this with pyenv, for example, in my
[~/.bashrc](https://github.com/bnbalsamo/dotfiles/blob/master/bashrc/.bashrc).

Additionally, for tools like pyenv or vim extensions, which are typically distributed via git repositories,
[git submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules) can dynamically link the
latest versions of tools to my dotfiles repo, rather than vendoring them. I package 
[pyenv](https://github.com/bnbalsamo/dotfiles/tree/master/pyenv) like this in my own dotfiles repo, 
[as well as all of my vim plugins](https://github.com/bnbalsamo/dotfiles/tree/master/vim/.vim/bundle)

Once all of this has been set up, having "my" bash/vim/tmux in place on a brand new host where I can install
software is as simple as...

```bash
$ sudo apt-get install tmux vim  # Or whatever other package manager is on the host...
$ git checkout https://github.com/bnbalsamo/dotfiles.git
$ cd dotfiles
$ stow tmux
$ stow vim
$ stow bashrc
```

## Scenario 3: Putting It All Together

Potentially the biggest leap of them all: I configure my "home" workspaces, the ones I
can go to, in exactly the same way as I configure any other workspace that I would bring
my configurations to.

This lets me benefit from the modularity of my 'stowed' dotfiles configuration regardless of which
strategy I'm employing on a given host, and also keeps everything in sync because my configurations 
everywhere are all based in the same version control repository.

I'm only ever a couple of ```git``` and ```stow``` commands away from having my configurations
on whatever host I'm working on, or one ```mosh $USER@$SERVER tmux a``` from working on a remote
host I've already configured.

## In Conclusion

Though it may seem a bit crazy at first, I think this method of deploying workspaces provides
some excellent benefits. Once I took the initial "leap" of putting my dotfiles into a git repo
(after some slight refactoring) I started to see compounding benefits each time I've used either
of these strategies in terms of saved time and headaches.

If you'd like to out a similar setup I hope this post does a decent job at stitching together
the various tools and workflows required to accomplish it. If you find yourself wondering where to
put your remote host I can heartily recommend [Digital Ocean](https://www.digitalocean.com/) as that's
where I have a couple of my own VPSs parked for just this reason. If you decide to try them out feel free
to use [my referral link](https://m.do.co/c/28ea9e74ca5d), which will save us both a couple
of bucks.
