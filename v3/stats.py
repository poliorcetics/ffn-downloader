# -*- coding : utf-8 -*-

import re
import os
import datetime as dt
from main3 import Story
import constants as c

""" -- stats.py

Author: Poliorcetics
1st version of the stats file of the ffn downloader.

This file gives you access to some functions which allow you to make stats
about the story you have, be it in general via a list of url or in a particular
folder.

Functions:
 - write_intro_stats(date: str, stories: int, words: int, chap: int,
                                                     universes: int) -> (str),
 - write_intro_universes()                                           -> (str),
 - write_div_universe(name: str, count: int)                         -> (str),
 - write_intro_universes()                                           -> (str),
 - write_div_story(url: str, title: str, universe: str, words: str,
                                                      chapters: int) -> (str),
 - remove_old_stats(path=None)                                       -> (None),
 - display_num(num: float)                                           -> (str),
 - display_story_line(title='Titles', words='Number of Words',
                            chap='Number of Chapters', v1=55, v2=20) -> (str),
 - display_end_stats(stories_count: str, words: str, chap: str)      -> (str),
 - write_stat_file(stories_list: list, words_count_total: int,
                           chap_count_total: int, universes: dict, folder=None,
                                                       display=True) -> (None),
 - write_stats_from_list(urls: list, display=True)                   -> (None),
 - write_stats_from_folder(path=None, display=True)                  -> (None).
"""


WORDS_REGEX = r' - Words: (.*?) - '

STATS_FILE_REGEX = r'(stats_.*\d*-.*-\d*.html)'

STATS_HEADER = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <style>
        * {
            font-family: "Helvetica";
            font-size: 20px;
            text-align: left;
        }
        h1 { font-size: 26px; }
        a { text-color: blue; }
        div { padding: 0px; }
        .story, .universe {
            width: 100%;
            display: flex;
            flex-wrap: nowrap;
        }
        .universe_name { width: 80%; }
        .universe_count { width: 20%; text-align: center; }
        .s_title {
            width: 50%;
            word-wrap: break-word;
        }
        .s_words, .s_chap, .s_ratio { text-align: center; }
        .s_words { width: 17%; }
        .s_chap { width: 15%; }
        .s_ratio { width: 18%; }
        em { font-size: 16px; }
    </style>
</head><body>"""


def write_intro_stats(date: str, stories: int, words: int, chap: int,
                      universes: int) -> (str):
    """Return the completed introduction of each stats file.

Parameters:
 - date                 - str - the formatted date of the last update,
 - stories              - int - the number of stories,
 - words                - int - the number of words (total),
 - chap                 - int - the number of chapters (total),
 - universes            - int - the number of universes (total).

Return:
 - str                  - the introduction of a stats file completed with the
                          given parameters."""

    if universes > 1:
        return """<h1>Stats</h1>

<strong>Informations:</strong>
<ul>
    <li>Last update: %s,</li>
    <li>%s universes,</li>
    <li>%s stories,</li>
    <li>%s words,</li>
    <li>%s chapters.</li>
</ul>\n""" % (date, display_num(universes), display_num(stories),
              display_num(words), display_num(chap))
    else:
        return """<h1>Stats</h1>

<strong>Informations:</strong>
<ul>
    <li>Last update: %s,</li>
    <li>%s universe,</li>
    <li>%s stories,</li>
    <li>%s words,</li>
    <li>%s chapters.</li>
</ul>\n""" % (date, display_num(universes), display_num(stories),
              display_num(words), display_num(chap))


def write_intro_universes() -> (str):
    """Return the beginning of the different columns for the universes."""

    return """\n<br />
<div class='universe' style='font-weight: bold;'>
<div class='universe_name'>Universe</div>
<div class='universe_count'>Stories</div>
</div><br />\n"""


def write_div_universe(name: str, count: int) -> (str):
    """Return the div for a single universe.

Parameters:
 - name                 - str - the name of the universe,
 - count                - int - the number of story for this universe.

Return:
 - str                  - the div containing the stats about the universe."""

    if count > 1:
        return """\n<div class='universe'>
<div class='universe_name'>• {name}</div>
<div class='universe_count'>{count} stories</div>
</div><br />\n""".format(name=name, count=count)
    else:
        return """\n<div class='universe'>
<div class='universe_name'>• {name}</div>
<div class='universe_count'>{count} story</div>
</div><br />\n""".format(name=name, count=count)


def write_intro_stories() -> (str):
    """Return the beginning of the different columns for the stories."""

    return """\n<br />
<div class='story' style='font-weight: bold;'>
<div class='s_title'>Story</div>
<div class='s_words'>Words</div>
<div class='s_chap'>Chapters</div>
<div class='s_ratio'>Ratio W/C</div>
</div><br />\n"""


def write_div_story(url: str, title: str, universe: str, words: str,
                    chapters: int) -> (str):
    """Return the div for a single story.

Parameters:
 - url                  - str - the link to the story (folder/real link),
 - title                - str - the title of the story,
 - universe             - str - the universe of the story,
 - words                - str - the number of words of the story (formatted),
 - chapters             - int - the number of chapters of the the story.

Return:
 - str                  - the div containing the stats about the story."""

    ratio = display_num(int(int(words.replace(' ', '')) / chapters))

    return """\n<div class='story'>
<div class='s_title'>• <a href='{url}'>{title}</a><br />
<em>({universe})</em></div>
<div class='s_words'>{words} words</div>
<div class='s_chap'>{chapters} chapters</div>
<div class='s_ratio'>~{ratio} w/c</div>
</div><br/>
""".format(url=url, title=title, words=words, chapters=display_num(chapters),
           universe=universe, ratio=ratio)


def remove_old_stats(path=None) -> (None):
    """Remove all the old stats files present in a directory."""

    global STATS_FILE_REGEX

    path = os.getcwd() if path is None else path
    base_path = os.getcwd()

    os.chdir(path)

    for file in os.listdir():
        m = re.match(STATS_FILE_REGEX, file)
        try:
            if m.group(1) == file:
                os.remove(file)
        except:
            pass

    os.chdir(base_path)


def display_num(num: float) -> (str):
    """Take a number and return it formatted: 5443 -> 5 443, 5443.3 -> 5 443.3
"""

    num = int(num) if int(num) == num else num

    return '{:,}'.format(num).replace(',', ' ')


def display_story_line(title='Titles', words='Number of Words',
                       chap='Number of Chapters', v1=55, v2=20) -> (str):
    """Display a line containing the infos about the story or the intro to
these infos.

Parameters:
 - title='Titles'               - str - the title of the story,
 - words='Number of Words'      - str - the number of words of the story,
 - chap='Number of Chapters'    - str - the number of chapters of the story.
 - v1=55                        - int - complete 'title' with ' ' to reach v1
 - v2=20                        - int - complete 'words' with ' ' to reach v2

Return:
 - str                          - the formatted line"""

    # V1 and V2 should be changed to please you
    return '{:<{v1}}{:<{v2}}{}'.format(title, words, chap, v1=v1, v2=v2)


def display_end_stats(stories_count: str, words: str, chap: str) -> (str):
    """Display the end part of the stats in the shell.

Paramters:
 - stories_count                - str - the formatted number of stories,
 - words                        - str - the formatted number of words,
 - chap                         - str - the formatted number of chapters.

Return
 - str                          - The formatted display for the end."""

    return """\nTotals for %s stories:

 - Words: %s
 - Chapters: %s\n""" % (stories_count, words, chap)


def write_stat_file(stories_list: list, words_count_total: int,
                    chap_count_total: int, universes: dict, folder=None,
                    display=True) -> (None):
    """Write the stats file from the given information.

Parameters:
 - stories_list                 - list - the list containing the dict of the
                                         stories,
 - words_count_total            - int - total number of words,
 - chap_count_total             - int - total number of chapters,
 - universes                    - dict - dict containing the universes as key
                                         and their stories' count as values,
 - folder=None                  - str - the name of the folder if wanted in the
                                        title of the file,
 - display=True                 - bool - if the progress are to be displayed.
"""

    global STATS_HEADER

    update = dt.datetime(1, 1, 1).today().strftime('%H:%M - %d %B %Y')
    date = dt.datetime(1, 1, 1).today().strftime('%d-%B-%Y')

    if display:
        print('\n' + display_story_line())

    # Remove the old file if needed, because if the date is different it won't
    # be deleted by being rewriten
    remove_old_stats()

    if folder is None:
        title = 'stats_{}.html'.format(date)
    else:
        title = 'stats_{}_{}.html'.format(folder, date)

    # Open the file to be written
    with open(title, 'w', encoding='utf-8') as f:

        # Write the header
        f.write(STATS_HEADER)

        # Write the intro of the file and universes
        f.write(write_intro_stats(update, len(stories_list), words_count_total,
                                  chap_count_total, len(universes)) +
                write_intro_universes())

        # Write the universes
        for key in sorted(universes.keys()):
            f.write(write_div_universe(key, universes[key]))

        # Write the stories
        f.write(write_intro_stories())
        for story in stories_list:
            f.write(write_div_story(title=story['title'], words=story['words'],
                                    url=story['url'], chapters=story['chap'],
                                    universe=story['universe']))

            if display:
                print(display_story_line(story['title'],
                      story['words'], display_num(story['chap'])))

        f.write('</body></html>')

    if display:
        print(display_end_stats(display_num(len(stories_list)),
              display_num(words_count_total),
              display_num(chap_count_total)))


def write_stats_from_list(urls: list, display=True) -> (None):
    """Take a list of stories and write a stat file from them.

Parameters:
 - urls                 - list - the urls from which to write the stats,
 - display=True         - bool - if the operations are to be shown in a console
"""

    global WORDS_REGEX

    words_count_total = 0
    chap_count_total = 0

    stories_list = []
    universes = {}

    # Get the infos for each urls
    for url in urls:

        if display:
            print('URL: %s' % url)

        try:
            st = Story(url)
        except:
            if display:
                print('!!! ERROR: Url not valid: %s' % url)
            continue
        else:
            words_match = re.search(WORDS_REGEX, st.tokens)
            words_count = words_match.group(1).replace(',', ' ')

            words_count_total += int(words_count.replace(' ', ''))
            chap_count_total += st.chap_count

            try:
                universes[st.universe] += 1
            except:
                universes[st.universe] = 1

            stories_list.append({'url': url,
                                 'title': st.s_title,
                                 'words': words_count,
                                 'chap': st.chap_count,
                                 'universe': st.universe})

    # Write the file containing all the stats
    write_stat_file(stories_list, words_count_total, chap_count_total,
                    universes, None, display)


def write_stats_from_folder(path=None, display=True) -> (None):
    """Take a path to a folder containing stories and write the stat file about
them.

Parameters:
 - path=None            - str - the path to the directory,
 - display=True         - bool - if the operations are to be shown in a console
"""
    global WORDS_REGEX

    path = os.getcwd() if path is None else path

    try:
        os.chdir(path)
    except:
        print('!!! ERROR: Not a valid path.')
        raise

    words_count_total = 0
    chap_count_total = 0

    stories_list = []
    universes = {}

    if display:
        print('\n--- FOLDER: %s ---\n' % os.getcwd())

    # For each folder
    for folder in os.listdir():

        # If the link do not point a folder, no use in continuing the process
        if not os.path.isdir(folder):
            if display:
                print('!!! ERROR: Not a folder: %s' % folder)
            continue

        # Else we try to get the id and name of the story
        try:
            s_name, s_id = folder.rsplit('_', 1)
        except:
            if display:
                print('!!! ERROR: Folder not valid: %s' % folder)
            continue
        # If there weren't any error so far, we compile the URL
        else:
            url = c.ROOT_URL + s_id + '/1/' + s_name

        # We try to get the story
        try:
            st = Story(url)
        except:
            if display:
                print('!!! ERROR: Folder not valid: %s' % folder)
                print('!!! ERROR: Url not valid: %s' % url)
            continue
        # If the URL was correct, we proceed to get the infos
        else:
            words_match = re.search(WORDS_REGEX, st.tokens)
            words_count = words_match.group(1).replace(',', ' ')

            words_count_total += int(words_count.replace(' ', ''))
            chap_count_total += st.chap_count

            try:
                universes[st.universe] += 1
            except:
                universes[st.universe] = 1

            stories_list.append({'url': '{}/{}_infos.html'.format(folder,
                                                                  st.text_id),
                                 'title': st.s_title,
                                 'words': words_count,
                                 'chap': st.chap_count,
                                 'universe': st.universe})

            if display:
                print('Folder: %s' % folder)

    # Finally we write the stats
    folder = os.getcwd().split(os.sep)[-1]
    write_stat_file(stories_list, words_count_total, chap_count_total,
                    universes, folder, display)
