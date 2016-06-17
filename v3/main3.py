# -*- coding : utf-8 -*-

import os
import sys
import re
import time
from urllib import request
from bs4 import BeautifulSoup
import constants as c

""" -- main3.py

author: Poliorcetics
3rd version of the ffn_downloader.

Main program to download stories from fanfiction.net. Use the main() function
to do exactly that, everything else will be handled by the code.

Classes:
 - Chapter(self, chapter: BeautifulSoup, num_chap: int, list_chap: list),
 - Story(self, url=None, update=False).

Functions:
 - correct_html(chap: str)                                          -> (str),
 - main(url: str, update=False)                                     -> (bool).
"""


class Chapter:
    """Represent a chapter (the minimal component) of a story.

Methods:
    Private
 - __init__(self, chapter: BeautifulSoup, num_chap: int, list_chap: list),
 - _get_chapter_text(self, chap: BeautifulSoup, chap_count: int)    -> (str):
 - _insert_anchor(self, title: str, num_chap: int)                  -> (str),
    Public
 - write_chap(self)                                                 -> (str),
 - get_chap(self)                                                   -> (str).

Variables:
    Private
 - self._previous_link                                              - str,
 - self._next_link                                                  - str,
    Public
 - self.text_chap                                                   - str,
 - self.title_chap                                                  - str,
 - self.title_file                                                  - str.
"""

    def __init__(self, chapter: BeautifulSoup, num_chap: int, list_chap: list):
        """Initialize the variables to handle a chapter.

Parameters:
 - chapter          - BeautifulSoup - the chapter itself,
 - num_chap         - int - the number of the chapter,
 - list_chap        - list - the list of the chapters.
"""

        # Find the text of the chapter and make it readable
        # If there are too many tags and it causes a recursion error,
        # I modify the base parameter for it and retry
        chap_count = len(list_chap)
        while True:
            try:
                self.text_chap = self._get_chapter_text(chapter, chap_count)
                break
            except Exception:
                print('---------------------- I DID A SETRECURSION !!!!!!!!!!')
                sys.setrecursionlimit(sys.getrecursionlimit() + 500)

        # Compute the number of '0's needed to equalize the length
        zeros = '0' * (len(str(len(list_chap))) - len(str(num_chap)))

        # Compute both titles
        self.title_chap = '\n<h1>%s%s</h1>\n' % (zeros, list_chap[num_chap-1])
        self.title_chap = self._insert_anchor(self.title_chap, num_chap)
        self.title_file = zeros + str(num_chap) + '.html'

        # Insert the 'previous' link if needed
        if num_chap > 1:
            prev = '0' * (len(str(chap_count)) - len(str(num_chap - 1)))
            self._previous_link = '%s%s.html' % (prev, num_chap - 1)
        else:
            self._previous_link = None

        # Insert the 'next' link if needed
        if num_chap < chap_count:
            nex = '0' * (len(str(chap_count)) - len(str(num_chap + 1)))
            self._next_link = '%s%s.html' % (nex, num_chap + 1)
        else:
            self._next_link = None

    def _get_chapter_text(self, chap: BeautifulSoup, chap_count: int) -> (str):
        """Return the text of the chapter itself in its entirety.

Parameter:
 - chap                     - BeautifulSoup - the html in a BeautifulSoup
object,
 - chap_count               - int - the number of chapter(s)."""

        text = str(chap).replace('\n', '')
        text = c._BEGINNING + text.split(c._BEGINNING, 1)[1]
        if chap_count > 1:
            text = text.split(c._END_MANY, 1)[0] + '</div>'
        else:
            text = text.split(c._END_ONE, 1)[0] + '</div>'

        return correct_html(text)

    def _insert_anchor(self, title: str, num_chap: int) -> (str):
        """Insert the anchor around the title of the chapter to help creating
a table of contents of the story.

Return the title as a string."""

        title = title.replace('<h1>', '<h1><a name="chap%s">' % num_chap)
        title = title.replace('</h1>', '</a></h1>')

        return title

    def write_chap(self) -> (str):
        """Write the chapter in its corresponding file with the proper
formatting and return it without it."""

        with open(self.title_file, 'w', encoding='utf-8') as f:
            f.write(c.HEADER)

            if self._previous_link is not None:
                f.write("\n<a href='%s'>Previous</a>\n" % self._previous_link)

            f.write(self.title_chap)
            f.write(self.text_chap)

            if self._next_link is not None:
                f.write("\n<a href='%s'>Next</a>\n" % self._next_link)

            f.write('\n</body>\n</html>')

        return self.get_chap()

    def get_chap(self) -> (str):
        """Return the basic form of a chapter, as a string."""

        return '<br /><br />' + self.title_chap + self.text_chap


class Story:
    """Represent a full story. The user just has to let the download/update
be done though, everything is supposed to be handled by the code.

Methods:
    Private
 - __init__(self, url=None, update=False)                   -> (None),
 - _get_infos(self, html: BeautifulSoup.prettify)           -> (None),
 - _get_list_chapters(self)                                 -> (list),
 - _write_infos(self)                                       -> (None),
 - _add_table_of_contents(self)                             -> (None),
    Public
 - download_story(self)                                     -> (bool).

Variables
    Private
 - self._first_chap                                         - BeautifulSoup,
 - self._update                                             - bool,
    Public
 - self.updated                                             - bool,
 - self.text_id                                             - str,
 - self.num_id                                              - str,
 - self.s_title                                             - str,
 - self.author                                              - str,
 - self.summary                                             - str,
 - self.tokens                                              - str,
 - self.infos                                               - list,
 - self.chap_count                                          - int,
 - self.story                                               - str.
"""

    def __init__(self, url=None, update=False):
        """Initialize the variables to handle a complete story.

Parameters:
 - url          - str - the url of the first chapter of the story,
 - update       - bool - True if the story must be updated, False if it should
                         be done from the very beginning."""

        # Open the first chapter to know everything there is to know about the
        # story
        for _ in range(10):
            try:
                first_chap = request.urlopen(url)
                break
            except:
                first_chap = None
            time.sleep(1)

        if first_chap is None:
            raise

        first_chap = first_chap.read().decode('utf-8')
        self._first_chap = BeautifulSoup(first_chap, 'html.parser')

        # To know if the story is here to be updated or completely downloaded
        self._update = update
        # Will be switched to True if the story was really updated
        self.updated = False

        # The informations about the story
        self.text_id = ''
        self.num_id = ''
        self.s_title = ''
        self.author = ''
        self.summary = ''
        self.tokens = ''

        # To ease accessing all of them
        self.infos = [
            self.text_id,
            self.num_id,
            self.s_title,
            self.author,
            self.summary,
            self.tokens,
        ]

        # Get the informations and the chapters early on
        self._get_infos(self._first_chap.prettify())
        self.list_chapters = self._get_list_chapters(self._first_chap)

        # Get the number of chapters
        self.chap_count = len(self.list_chapters)

        # Will contain the full story
        self.story = ''

    def _get_infos(self, html: BeautifulSoup.prettify) -> (None):
        """Get all the available infos about the story."""

        # The one we can be sure to found:
        self.text_id = re.search(c._TEXT_ID_REGEX, html).group(1)
        self.num_id = re.search(c._NUM_ID_REGEX, html).group(1)
        self.s_title = re.search(c._TITLE_REGEX, html).group(1)
        self.author = re.search(c._AUTHOR_REGEX, html).group(1)
        self.summary = re.search(c._SUMMARY_REGEX, html).group(1)

        tokens_text = str(self._first_chap.find('span', 'xgray xcontrast_txt'))
        tokens_soup = BeautifulSoup(tokens_text, 'html.parser')
        self.tokens = tokens_soup.get_text()
        ' '.join(self.tokens.split())

        self.infos = [
            self.text_id,
            self.num_id,
            self.s_title,
            self.author,
            self.summary,
            self.tokens,
        ]

    def _get_list_chapters(self, html: BeautifulSoup) -> (list):
        """Return a list containing the chapters of the story."""

        list_chapters = []

        # With this method we can now if the story is a one-shot or not and
        # handle it now
        try:
            html_chapters = html.find(id='chap_select').prettify()
        except AttributeError:
            list_chapters.append(self.s_title)
        else:
            for chapter in re.findall(c._CHAPTERS_REGEX, html_chapters):
                list_chapters.append(chapter[1])

        return list_chapters

    def _write_infos(self) -> (None):
        """Write the informations about the story in the proper file."""

        # Format the chapters to allow a clean display
        chap_formatted = ""
        for chap in self.list_chapters:
            chap_formatted += chap + '<br />'

        # The same with the tokens
        tokens_formatted = self.tokens.replace(' - ', '\n<br />\n- ')

        # Open and write
        with open('%s_infos.html' % self.text_id, 'w', encoding='utf-8') as f:

            f.write("""{header}
<h1>{title}</h1><br />
By: {author}<br />
URL: {base_url}{num_id}/1/{text_id}<br />
<br />
{summary}<br />
<br />
Other informations:<br />
- {tokens}<br />
<br />
Chapters ({chap_count}):<br />
<br />
{chapters}
\n</body>\n</html>
""".format(header=c.HEADER, title=self.s_title, author=self.author,
           base_url=c.ROOT_URL, num_id=self.num_id, text_id=self.text_id,
           summary=self.summary, tokens=tokens_formatted,
           chap_count=self.chap_count, chapters=chap_formatted))

    def _add_table_of_contents(self) -> (None):
        """Generate a table of contents for the story."""

        self.story += '\nTable of contents:<br /><br />\n'

        # Each entry is linked to its chapter, allowing in-page navigation
        for num_chap in range(1, self.chap_count + 1):
            self.story += """
<a href="#chap%s">%s</a><br />
""" % (num_chap, self.list_chapters[num_chap - 1])

    def download_story(self) -> (bool):
        """Download the story, save it in all the wanted files and display
its work as it is going on.

Return:
 - self.updated         - bool - True if the story was updated, False if not.
"""

        # Introduction
        print('_' * 80)
        print('\n\n\nDOING: %s \n' % self.s_title)

        # Some basic informations to let the user know what it is downloading
        print("""AUTHOR: {author}
ID: {num_id}
URL: {base_url}{num_id}/1/{text_id}
CHAPTERS: {chap_count}""".format(author=self.author, base_url=c.ROOT_URL,
                                 num_id=self.num_id, text_id=self.text_id,
                                 chap_count=self.chap_count))

        # Save the base directory and set up the one for the story
        base_dir = os.getcwd()
        story_dir = '%s_%s' % (self.text_id, self.num_id)

        # If the story is updated, it is assumed the directory exists
        # If the story is downloaded, it is wiped and recreated
        if not self._update:
            try:
                os.mkdir(story_dir)
            except:
                for file in os.listdir(story_dir):
                    os.remove('%s%s%s' % (story_dir, os.sep, file))
                os.rmdir(story_dir)
                os.mkdir(story_dir)
            finally:
                os.chdir(story_dir)
        else:
            os.chdir(story_dir)
            # Count the chapters. To account for the two files that
            # are not chapters, -2
            num_old_chaps = - 2
            for file in os.listdir():
                # Count the chapters only if they are .html files
                if '.html' in file:
                    num_old_chaps += 1
            # Display the number of chapters that are already done
            print('OLD CHAPTERS: %s' % num_old_chaps)

        # Write the file containing the informations
        self._write_infos()
        print('\nDONE -- %s_infos.html' % self.text_id)

        # First part of the story
        self.story = c.HEADER

        # Add the table of contents if needed
        if self.chap_count > 1:
            self.story += '\n<h1>%s</h1><br /><br />\n' % self.s_title
            self._add_table_of_contents()

        # Deal with each and every chapter
        for num_chap in range(1, self.chap_count + 1):

            # Get the chapter
            url = '%s%s/%s/' % (c.ROOT_URL, self.num_id, num_chap)
            # To handle possible network problems
            trials = 0
            while trials < 10:
                try:
                    chap = request.urlopen(url)
                    break
                except:
                    chap = None
                time.sleep(1)
                trials += 1
            if chap is None:
                print('!!! ERROR: Network Error while opening the chapter.')
                raise Exception

            # Get the chapter in the proper format
            chap = chap.read().decode('utf-8')
            chap = correct_html(chap)
            chap = BeautifulSoup(chap, 'html.parser')
            chap = Chapter(chap, num_chap, self.list_chapters)

            # If the story is to be updated
            if self._update:
                # Write the chapter only if needed
                if num_chap <= num_old_chaps:
                    self.story += chap.get_chap()
                    print('ALREADY DONE -- %s' % chap.title_file)
                else:
                    self.story += chap.write_chap()
                    print('NEW -- %s' % chap.title_file)
                    self.updated = True
            # Not to update
            else:
                # If the story is not a one-shot
                if self.chap_count > 1:
                    self.story += chap.write_chap()
                    print('DONE -- %s' % chap.title_file)
                # If the story is a one-shot
                else:
                    self.story += chap.get_chap()

        # Write the full story itself
        with open('%s.html' % story_dir, 'w', encoding='utf-8') as f:
            f.write(self.story + '\n</body>\n</html>')

        print('DONE -- %s.html' % story_dir)
        os.chdir(base_dir)

        return self.updated


def correct_html(chap: str) -> (str):
    """I encountered stories where FFN had messed up the code to the point
where it caused troubles getting the chapter. Here are the fixes for what I
saw until today.

Parameter:
 - chap             - str - the text to modify as a string."""

    chap = re.sub(c._WRONG_PAR_REGEX, '</p>', chap)

    for match in re.findall(c._WRONG_PAR_REGEX_2, chap):
        to_repl = ''
        # </p>
        to_repl += match[0] + '<hr size=1 ' if match[0] else '<hr size=1 '
        # width=100%
        to_repl += match[1] + 'noshade>' if match[1] else 'noshade>'
        # </p>
        to_repl += match[2] if match[2] else ''
        # <p>
        to_repl += match[3] if match[3] else ''
        chap = chap.replace(to_repl, '</p><hr width=100% size=1 noshade><p>')

    chap = re.sub(c._WRONG_PAR_REGEX, '</p>', chap)

    return chap


def main(url: str, update=False) -> (bool):
    """Ease the use of the downloader.

Parameters:
 - url                  - str - the url of the first chapter of the story,
 - update=False         - True if the story must be updated, False if it should
be done from the very beginning.

Return:
 - self.updated         - bool - True if the story was updated, False if not.
"""

    st = Story(url, update)
    return st.download_story()
