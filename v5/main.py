"""
File: main.py
Author: BOURGET Alexis
License: see LICENSE.txt
App version: 5.0
File version: 5.0

Contains the *main* function, which download/update a story.
"""

import os
import story


def main(url: str, update=False, display=True):
    """
    Downloads/Update a story from a given *url*.

    Args:
        url (str): the url of the story to process.
        update[False] (bool): True if the story should be updated
        display[True] (bool): Indicates if messages are displayed on stdout.
    """
    base_dir = os.getcwd()
    st = story.Story(url)
    writer = story.StoryWriter(display)

    if display:
        print('\n' + '_' * 80, f'\n\n{repr(st)}\n\n')

    if not update:
        writer.create(st)
    else:
        writer.update(st)

    del st
    os.chdir(base_dir)
