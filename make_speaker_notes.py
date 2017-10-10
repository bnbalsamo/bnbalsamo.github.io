from sys import argv
from os import scandir
from os.path import join

from markdown2 import Markdown

speaker_notes_header = """---
layout:page
title: notes
---

"""

def parse_for_notes(p):
    note_lines = []

    with open(p) as f:
        capturing = False
        for l in f.readlines():
            if l == "???\n":
                capturing = True
                continue
            if l == "---\n":
                if capturing:
                    note_lines.append(l)
                capturing = False
                continue

            if capturing:
                note_lines.append(l)

    notes_markdown = "".join(note_lines)
    return notes_markdown


def main():
    for x in scandir("./_presentations"):
        notes_markdown = parse_for_notes(x.path)
        with open(join("./_speaker_notes", x.name[0:-5]+".md"), 'w') as f:
            f.write(speaker_notes_header + notes_markdown)


if __name__ == "__main__":
    main()
