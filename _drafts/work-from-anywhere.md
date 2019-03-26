---
title: Work From Anywhere with mosh, tmux, git, and stow
layout: post
---

Ever been stuck working from a general purpose AWS workspace, client provided laptop, or while SSH'd
into a server you haven't worked from before? 

I have, and no matter how many times it happened it used to be nearly
impossible to not run into a little annoyance here and there for days, if not a week: trying to run
an application that hadn't been installed yet, trying to use a hotkey that wasn't the same on that
host, typing an undefined alias, etc. All of these little inconveniences added up. 
They took time to remedy, and disturbed the flow of work in the most irritating ways.

Worst of all was remembering how I had experienced the exact same issues the last time I
had started working from a new environment!

I'm sure if you've also had to work in multiple changing environments you've run into similar issues.

So, how do we avoid these inconveniences? We've got two real options:

* Go to our digital workspace 
* Bring our digital workspace to us

When dealing with development environments both of these options are feasible,
and both are going to be appropriate in different scenarios. 

This post outlines my own methodology for making both of these scenarios a reality in my day to day
work.

## The Elephant in the Room

Check your GUI at the door.

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

For these reasons, among others, I've chosen to build my own workspaces with CLI applications. 

## Scenario 1: Go to Our Workspace

"Going somewhere" on the *nix CLI is a standard procedure. It is accomplished via
[SSH](https://en.wikipedia.org/wiki/Secure_Shell), and nearly every *nix system has a [CLI 
ssh client](https://linux.die.net/man/1/ssh) installed by default. In order to go to our workspace
we'll need to configure an SSH server on the host that contains our workspace. I'll not go so far as
to include a tutorial on installing and configuring a SSH server in this blog post, because there are
[plenty](https://help.ubuntu.com/community/SSH/OpenSSH/Configuring) 
[of](https://wiki.debian.org/SSH#Installation_of_the_server)
[them](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-16-04)
[already](https://wiki.archlinux.org/index.php/OpenSSH#Installation).

### I'm There, Now What?

SSHing into a server gives you a CLI interface. If you aren't comfortable working on the CLI already
that might not help you very much. To do real work we'll need some applications which fulfill standard
needs. 

- Bash fills the slot of a task launcher and file system explorer. 
- [git](https://git-scm.com/) provides us access to version control repositories
- [tmux](https://github.com/tmux/tmux) can act as a window manager, providing us with different "windows"
to open new terminals or applications in.
- [vim](https://www.vim.org/) can act as our editor, giving
us the ability to edit files. 

Beyond these basic tools your workflows may dictate other requirements,
if so, find some CLI tools that provide them!

Now we've gone to our workspace, and we've got access to tools so that we can do our work, but SSH has
some annoying behaviors:

- it disconnects when ever we lose network access and doesn't
 automatically reconnect. 
- it kills our processes if we disconnect
- it blocks if we run a long running process in the foreground, and we have to open a new (local)
  terminal instance and start a new SSH connection to keep working.

[mosh](https://mosh.org/) and [tmux](https://github.com/tmux/tmux) to the rescue! 
 
### mosh

Mosh sits on top of SSH and provides
us with a near identical interface to ssh so we can connect to the host with our workspace and provides some
nice benefits, like the ability to reconnect after sleeping/hibernating the connected machine, or roaming
between different networks. Mosh is easy to setup, it installs just like any other application on a 
host we can SSH into, it doesn't require a daemon, or even to be invoked with sudo, so it can be run 
entirely in user-land if required.

### tmux

Tmux, in addition to making a great terminal based window management solution, is also a [terminal
multiplexer](https://en.wikipedia.org/wiki/Terminal_multiplexer). While mosh provides us with the ability
to painlessly reconnect to SSH sessions, and keeps our processes from being killed in the event that we
lose connection to the remote server, it doesn't provide us with the kind of fine grained manual control
of session persistence that a full blown terminal multiplexer does. Tmux also gives us the ability to run
multiple virtual terminal windows within a single "real" terminal window - meaning that long running process
in the foreground can run happily while we open another tab or split and continue working.

The interplay between mosh and tmux can be a bit confusing off the bat, and getting them both
configured and working together in harmony (and utilizing them effeciently) can be tricky.
[This excellent blog post](https://blog.filippo.io/my-remote-shell-session-setup/) goes over configuring
this portion of a robust remote workspace setup with mosh and tmux working together, so I'll avoid 
reiterating it's content here.

With this type of setup, we can use the ubiquitous ssh client, or download the mosh client, and
travel to our own pre-configured workspace!

## Scenario 2: Bring Our Workspace to Us

We took the time to configure a CLI based workspace so that we could remote into a server and get work done 
in scenario 1, however, the vast majority of our tools are only an ```apt-get install``` or ```git clone``` 
away from any machine. 

Nearly all well behaved CLI tools can be configured via 
[dotfiles](https://en.wikipedia.org/wiki/Hidden_file_and_hidden_directory#Unix_and_Unix-like_environments),
configuration files that live in your home directory and start with a "." so that they don't clutter up
your default ```ls``` output. 

The majority of the "hard" work of setting up our workspace is done in the dotfiles
that contain their configuration (and our personalizations). These files are plaintext, and in order to
bring our workspace to us we need to distribute them to multiple hosts and keep them in sync.

### git

Distributing and syncing text files between multiple multiple workspaces sounds _a lot_ like a workflow 
that developers are well acquainted with - distributing source code. With this in mind we already
have the perfect tool for bringing our dotfiles to us regardless of what host we're working on: 
[git](https://git-scm.com/)!

### stow

But, our home directories aren't source code. There are a multitude of reasons not to 
put your home directory under version control:

- It often contains large files
- It can contain caches, indices, and other host specific information
- It frequently contains passwords, secrets, and other private information
- etc

Given these points in combination with the relatively disasterous potential outcomes of a mistaken
git commit it's unreasonable to attempt to manage a git repository of our home directory using tools
like ``.gitignore``` files.

These issues are only compounded if we use a public repository, which is desirable so that 
our dotfiles can be accessed from anywhere (ie, any host we happen to be working from). 

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

Stow allows us to put a directory in our home directory (usually called something like `dotfiles`), put
_that_ directory under version control, divide dotfiles and configuration file hierarchies up into 
directories per application and then use stow in order to symlink those files into your home directory.
If that sounds a little confusing feel free to take a look at 
[my own dotfiles repo](https://github.com/bnbalsamo/dotfiles) to see what I'm talking about.

This works for single files (e.g.: ```.bashrc```) and for applications whose configuration 
live in the ```.config``` directory, or in dotfile directories (eg: ```.vim/```). 

Additionally, certain utilities (pyenv, for example) can live entirely within the users home directory. 
With a conditional or two in ```~/.bashrc`` it is possible to dynamically activate tools if they've
been "unstowed", which can be very powerful. I do this with pyenv, for example, in my own 
[~/.bashrc](https://github.com/bnbalsamo/dotfiles/blob/master/bashrc/.bashrc).

Additionally, for tools like pyenv or vim extensions, which are typically distributed via git repositories,
[git submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules) can dynamically link the
latest versions of tools to your dotfiles repo, rather than vendoring them. I package pyenv like
this in my own dotfiles repo, 
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

## Scenario 3: The Best of Both Worlds

So, when all is said and done, which scenario works best in real world scenarios?

...

![porque no los dos?](https://i.imgur.com/s4eamxv.jpg)

If we configure our "home" workspace in the same way as we would any other remote workspace, we can
benefit from both approaches in a modular manner as appropriate in any given circumstance.

We maintain a "home base" configured to our liking that we can use ```mosh $USER@$SERVER tmux a``` to
access whenever we need to in combination with a VPS provider like [Digital Ocean](https://www.digitalocean.com/)
to house this environment, so it's available easily over the internet (Shameless plug, if you feel like trying
this aspect of the approach out, and aren't a DO customer already, here's [my referral link](https://m.do.co/c/28ea9e74ca5d)).

Then, in scenarios where we can install software in a new workspace (even if only into user space) 
we can use a dotfiles git repository, in combination with stow, to move our customizations and
configurations seamlessly between hosts.

## In Conclusion...

Never be left wanting for your customizations or preferred development workflows again,
use mosh, tmux, git, and stow in order to work seamlessly from just about anywhere.
