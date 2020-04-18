"""
Tasks for managing bnbalsamo.github.io
"""

import os
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from invoke import Collection, task
from werkzeug.utils import secure_filename

# Change the CWD to the repo root.
_LAST_DIR = None
while not Path("./tasks.py").exists():
    os.chdir("..")
    _CURRENT_DIR = Path(".").resolve()
    if _CURRENT_DIR == _LAST_DIR:
        # We hit the FS root :(
        raise FileNotFoundError("Could not find the repository root.")


# Relevant directories, relative to the repo root.
DIRECTORIES = {
    "drafts": Path("./_drafts"),
    "posts": Path("./_posts"),
    "presentations": Path("./_presentations"),
    "speaker_notes": Path("./_speaker_notes"),
}


# Used in some helper prints - never actually called.
EDITOR = os.environ.get("EDITOR") or "nano"


speaker_notes_header = """---
layout: page
---

"""


def parse_for_notes(p):
    note_lines = []

    with open(p) as f:
        capturing = False
        for line in f.readlines():
            if line == "???\n":
                capturing = True
                continue
            if line == "---\n":
                # Ignore the header
                if capturing:
                    note_lines.append(line)
                capturing = False
                continue

            if capturing:
                note_lines.append(line)

    notes_markdown = "".join(note_lines)
    return notes_markdown


def title_to_filename(title):
    """
    Convert a post or presentation title to a file name.
    """
    filename = title.lower()
    filename = secure_filename(filename)
    return filename


@task(name="post")
def new_post(c, title):
    """
    Create a new post.
    """
    print("Creating draft post")
    print(f"Title: {title}")
    filepath = DIRECTORIES["drafts"] / (title_to_filename(title) + ".md")
    filepath = filepath.resolve()
    print(f"File Path: {filepath}")
    if filepath.exists():
        raise FileExistsError(filepath.resolve())
    with open(filepath, "w") as f:
        f.write(f"---\nlayout: post\ntitle:{title}\n---\n\n")
    print("Open your new post for editing with...")
    print(f"{EDITOR} {filepath}")


@task(name="presentation")
def new_presentation(c, title):
    """
    Create a new presentation.
    """
    print("!!! Presentations don't support drafts, this will be published !!!")
    print("Creating presentation")
    print(f"Title: {title}")
    filepath = DIRECTORIES["presentations"] / (title_to_filename(title) + ".html")
    filepath = filepath.resolve()
    print(f"File Path: {filepath}")
    if filepath.exists():
        raise FileExistsError(filepath)
    with open(filepath, "w") as f:
        f.write(
            "---\n"
            "layout: presentation\n"
            f"pres_title: {title}\n---\n\n"
            "class: center, middle\n"
            f"# {title}\n\n"
            "---\n\n"
        )
    print("Open your new presentation for editing with...")
    print(f"{EDITOR} {filepath}")


@task(name="post")
def publish_post(c, title, year=None, month=None, day=None):
    """
    Publish a post from drafts.
    """
    print(f"Publishing Post: {title}")
    draft_filepath = DIRECTORIES["drafts"] / (title_to_filename(title) + ".md")
    draft_filepath = draft_filepath.resolve()
    print(f"Draft File Path: {draft_filepath}")
    if not draft_filepath.exists():
        raise FileNotFoundError(draft_filepath)
    if year is None:
        # Zero padding here might be overkill, but it's consistent!
        year = f"{datetime.now().year:04}"
    if month is None:
        month = f"{datetime.now().month:02}"
    if day is None:
        day = f"{datetime.now().day:02}"
    post_filepath = DIRECTORIES["posts"] / (
        f"{year}-{month}-{day}-{title_to_filename(title)}" + ".md"
    )
    post_filepath = post_filepath.resolve()
    print(f"Post File Path: {post_filepath}")
    if post_filepath.exists():
        raise FileExistsError(post_filepath)
    draft_filepath.rename(post_filepath)


@task(name="site")
def export_site(c):
    """
    Build and export the site to the local host.
    """
    print("Building site...")
    c.run("sudo docker run --rm -v $(pwd):/srv/jekyll jekyll/jekyll jekyll build")
    print(f"Site available in `{Path('./_site').resolve()}`")


@task(name="dockerimage")
def export_docker_image(c, image_name="bnbalsamo.github.io:latest"):
    """
    Build and export the docker image to the local host.
    """
    c.run(f"sudo docker build . -t {image_name}")


@task(name="speakernotes")
def export_speaker_notes(c):
    """
    Build and export speaker notes to the local host.
    """
    for x in Path("./_presentations").iterdir():
        notes_markdown = parse_for_notes(x)
        with open(DIRECTORIES["speaker_notes"] / (x.name[0:-5] + ".md"), "w") as f:
            f.write(speaker_notes_header + notes_markdown)


@task(name="dockerimage")
def run_docker_image(c, image_name="bnbalsamo.github.io:latest", port=80, build=True):
    """
    Run the docker image locally.
    """
    if build:
        export_docker_image(c, image_name=image_name)
    print(f"Running container. Access site at localhost:{port}")
    c.run(f"sudo docker run -p {port}:80 {image_name}")


@task(name="testsite")
def run_test_site(c, port=4000):
    """
    Run the test site locally.
    """
    uid = uuid4().hex
    print(f"Running test site on port {port}...")
    c.run(
        f"sudo docker run -d --name test_site_{uid} -p {port}:4000 "
        "-v $(pwd):/srv/jekyll jekyll/jekyll jekyll serve --watch -D"
    )
    print("Run the following to end the test server instance...")
    print(f"sudo docker stop test_site_{uid} && " f"sudo docker rm test_site_{uid}")


# Organize into our subcommands...
ns = Collection()  # Make implicit root explicit


# Add "new" subcommand
new_ns = Collection("new")
new_ns.add_task(new_post)
new_ns.add_task(new_presentation)
ns.add_collection(new_ns)


# Add "publish" subcommand
publish_ns = Collection("publish")
publish_ns.add_task(publish_post)
ns.add_collection(publish_ns)


# Add "export" subcommand
export_ns = Collection("export")
export_ns.add_task(export_site)
export_ns.add_task(export_docker_image)
export_ns.add_task(export_speaker_notes)
ns.add_collection(export_ns)


# Add "run" subcommand
run_ns = Collection("run")
run_ns.add_task(run_docker_image)
run_ns.add_task(run_test_site)
ns.add_collection(run_ns)
