"""
File: main.py
Author: BOURGET Alexis
License: see LICENSE.txt
App version: 5.3.3
File version: 5.1

Contains the *main* function, which download/update a story.
"""

import os
import story


def main(url: str, update=False, display=True) -> (int):
    """
    Downloads/Update a story from a given *url*.

    Args:
        url (str): the url of the story to process.
        update[False] (bool): True if the story should be updated
        display[True] (bool): Indicates if messages are displayed on stdout.

    Returns:
        In case *update* is False:
            0 - the story was added for the first time to the directory
            1 - an older version was replaced
        In case *update* is True:
            0 - the story was added for the first time to the directory
            1 - the story was updated correctly
            2 - the story was already up-to-date
    """
    base_dir = os.getcwd()
    st = story.Story(url)
    writer = story.StoryWriter(display)

    if display:
        print('\n' + '_' * 80, f'\n\n{repr(st)}\n\n')

    if not update:
        result = writer.create(st)
    else:
        result = writer.update(st)

    del st
    os.chdir(base_dir)

    return result
