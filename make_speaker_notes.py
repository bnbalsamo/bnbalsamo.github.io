from os import scandir
from os.path import join


"""
ONLY RUN THIS FROM THE JEKYLL ROOT DIR

Generates notes that will be written
to the jekyll site for when I don't have
a dual screen setup to run presenter mode with.

Replacing /presentations/ with /speaker_notes/ in
the url on the site and it will pull up the notes page
on a phone/tablet/separate computer/etc
"""

speaker_notes_header = """---
layout:page
title: notes
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


def main():
    for x in scandir("./_presentations"):
        notes_markdown = parse_for_notes(x.path)
        with open(join("./_speaker_notes", x.name[0:-5]+".md"), 'w') as f:
            f.write(speaker_notes_header + notes_markdown)


if __name__ == "__main__":
    main()
