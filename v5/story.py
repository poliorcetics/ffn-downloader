"""
File: story.py
Author: BOURGET Alexis
License: see LICENSE.txt
App version: 5.3.3
File version: 2.5.1

Contains the class 'Story' which handles the infomations and the downloading
of the chapters of a particular story, and the class 'StoryWriter' which
handles the downloading/updating part.
"""

import re
import os
import datetime
import urllib
import constants as c
import tools as tls


class Story(object):
    """
    Collects informations and chapters for a given story.

    Initialization:
        url (str): the url of the targeted story.

    Public methods:
        get_infos(self, mode: str) -> str
        get_chapter(self, c_num: int) -> str

    Public attributes:
        ifs (dict): keys: - auth    (str): Story author.
                          - auth_id (str): Author's ID.
                          - c_count (int): Number of chapters.
                          - lang    (str): Language.
                          - chap    (list): Ordered list of the chapters.
                          - n_id    (str): Numeric id.
                          - publ    (str): Date of first publication.
                          - rating  (str): Rated: K/K+/T/M.
                          - status  (str): Complete/In Progress.
                          - s_dir   (str): Story directory.
                          - smry    (str): Summary.
                          - t_id    (str): Textual id (title with dashes).
                          - title   (str): Title.
                          - tk      (str): Tokens.
                          - uni     (str): Universe(s).
                          - upd     (str): Date of the last update.
                                           (May not exist, then is 'Never').
                          - url     (str): Url for the first chapter.
                          - w_count (str): Number of words.
    """

    def __init__(self, url: str):
        """
        __init__ method, initializes the variables.

        Args:
            url (str): the url to use.

        Raises:
            ValueError(f"{url} is not a valid fanfiction.net URL for a story")
            urllib.error.HTTPError
            ValueError(f"{url} is not the URL of an accessible story.")
        """

        if not tls.is_url(url):
            raise ValueError(f"{url} is not a valid fanfiction.net URL for a "
                             "story.")

        try:
            page = tls.get_page(url)
        except urllib.error.HTTPError as e:
            raise e

        # Here I get the informations which will be needed to create self.ifs
        try:
            text_id = tls.clean(re.search(c.TEXT_ID_REGEX, page).group(1))
        except AttributeError:
            raise ValueError(f"{url} is not the URL of an accessible story.")
        num_id = url.split('/')[4]
        tokens = Story._get_tokens(page)
        chap_count = Story._get_chap_count(tokens)
        status = Story._get_status(tokens)

        # Informations are sorted alphabetically here
        self.ifs = {
            'auth': re.search(c.AUTHOR_REGEX, page).group(1),         # str
            'auth_id': re.search(c.AUTHOR_ID_REGEX, page).group(1),   # str
            'c_count': Story._get_chap_count(tokens),                 # • int
            'lang': tokens.split(' - ')[2],                           # str
            'chap': re.findall(c.CHAPTERS_REGEX, page)[:chap_count],  # • list
            'n_id': num_id,                                           # str
            'publ': re.search(c.PUBLISHED_REGEX, tokens).group(1),    # str
            'rating': tokens.split(' - ')[1],                         # str
            's_dir': f'{text_id}_{num_id}'.lower(),                   # str
            'status': Story._get_status(tokens),                      # str
            'smry': re.search(c.SUMMARY_REGEX, page).group(1),        # str
            't_id': text_id.lower(),                                  # str
            'title': re.search(c.STORY_TITLE_REGEX, page).group(1),   # str
            'tk': Story._insert_status(tokens, status),               # str
            'uni': Story._get_universe(page),                         # str
            'upd': Story._get_update(tokens),                         # str
            'url': f'{c.ROOT_URL}{num_id}/1/{text_id}',               # str
            'w_count': Story._get_words_count(tokens),                # • int
        }

    def __repr__(self) -> str:
        """
        The representation of a Story class.

        Returns:
            Title, universe, author, url, summary and the tokens.
            Each on a separate line.

        Example:
            >>> a = Story('https://www.fanfiction.net/s/424242/1/')
            >>> a
            Title:      Hey, I'm a title !
            From:       Farenheit 451
            Author:     F.451
            Url:        https://www.fanfiction.net/s/424242/1/title-with-dashes
            Tokens:     All the tokens, separated by ' - '

            Here is the summary !
        """
        return (f'{"Title:":12}{self.ifs["title"].upper()}\n'
                f'{"From:":12}{self.ifs["uni"]}\n'
                f'{"Author:":12}{self.ifs["auth"]}\n'
                f'{"Url:":12}{self.ifs["url"]}\n'
                f'{"Tokens:":11}{self.ifs["tk"]}\n\n'
                f'{self.ifs["smry"]}'
                )

    @staticmethod
    def _get_universe(page: str) -> str:
        """
        Gets the universe from a fanfiction.net HTML page.

        Args:
            page (str): the HTML page to use.

        Returns:
            The universe as a `str`.title().
        """
        return re.search(c.UNIVERSE_REGEX, page).group(2).title()

    @staticmethod
    def _get_tokens(page: str) -> str:
        """
        Gets the tokens from a fanfiction.net HTML page.

        Args:
            page (str): the HTML page to use.

        Returns:
            The tokens as a `str` starting by a space.
        """
        tk = re.search(c.TOKENS_REGEX, page).group(1)
        return ' ' + re.sub(c.HTML_FROM_TOKENS_REGEX, '', tk)

    @staticmethod
    def _get_chap_count(tokens: str) -> int:
        """
        Gets the number of chapter from the tokens of a story.

        Args:
            tokens (str): the tokens to use.

        Returns:
            The number of chapters as an `int`.
        """
        try:
            chap_count = re.search(c.CHAPTERS_COUNT_REGEX, tokens).group(1)
        except AttributeError:
            chap_count = '1'
        return int(chap_count.replace(',', ''))

    @staticmethod
    def _get_words_count(tokens: str) -> int:
        """
        Gets the number of words from the tokens of a story.

        Args:
            tokens (str): the tokens to use.

        Returns:
            The number of words as an `int`.
        """
        words_count = re.search(c.WORDS_COUNT_REGEX, tokens).group(1)
        return int(words_count.replace(',', ''))

    @staticmethod
    def _get_update(tokens: str) -> str:
        """
        Gets the time of the last from the tokens of a story.

        Args:
            tokens (str): the tokens to use.

        Returns:
            The date of the last update as a `str`.
        """
        try:
            updated = re.search(c.UPDATED_REGEX, tokens).group(1)
        except AttributeError:
            updated = 'Updated: Never'
        return updated

    @staticmethod
    def _get_status(tokens: str) -> str:
        """
        Gets the status from the tokens of a story.

        Args:
            tokens (str): the tokens to use.

        Returns:
            The status as a `str`.
        """
        status = re.search(c.STATUS_REGEX, tokens)
        return 'Status: In Progress' if status is None else 'Status: Complete'

    @staticmethod
    def _insert_status(tokens: str, status: str) -> str:
        """
        Inserts the status in the tokens of a story.

        Args:
            tokens (str): the tokens to use.
            status (str): the status to insert.

        Returns
            The tokens as a `str` with the status properly registered in it.
        """
        if 'Status: Complete' in tokens:
            return tokens
        else:
            return tokens.replace('- id:', f'- {status} - id:')

    def get_infos(self, mode: str) -> str:
        """
        Return the informations formatted as asked (*mode* parameter).

        Args:
            mode (str): The mode of saving:
                        - 'h' to save in a human-readable format (.html),
                           File name is then: {num_id}_{text_id}_infos.html
                        - 's' to save in a stats-usable format (UTF-8 encoded).
                           File name is then: {num_id}

        Returns:
            The formatted informations as `str`, ready to be written in a file.

        Raises:
            ValueError(f"'mode' cannot be '{mode}', only 'h' or 's'.")
        """

        def gen_toc(self) -> str:
            """
            Generates a table of contents to be printed in the human stats.
            """
            c_count = self.ifs['c_count']
            lgth = len(str(c_count))
            toc = ''
            if c_count > 1:
                for num in range(1, c_count + 1):
                    toc += (f"<li><a href='{str(num).zfill(lgth)}.html'>"
                            f"{self.ifs['chap'][num - 1]}</a></li>\n")
            else:
                toc = f"<li><a href='1.html'>{self.ifs['title']}</a></li>"

            return toc

        if mode == 'h':
            toc = gen_toc(self)
            tk_formatted = '- ' + self.ifs['tk'].replace(' - ', '<br/>\n- ')
            date_obj = datetime.datetime(1, 1, 1)
            p_date = date_obj.today().strftime('%H:%M - %d %B %Y')

            auth_url = f"{c.AUTH_URL}{self.ifs['auth_id']}/"
            page_title = self.ifs['title'] + ' | Informations'

            # Informations are ready to be saved in a .html file
            return c.INFOS_TEMPLATE.format(ttl=page_title,
                                           ffn_title=self.ifs['title'],
                                           p_date=p_date,
                                           auth_url=auth_url,
                                           author=self.ifs['auth'],
                                           ffn_url=self.ifs['url'],
                                           universe=self.ifs['uni'],
                                           summary=self.ifs['smry'],
                                           tk_formatted=tk_formatted,
                                           chap_count=self.ifs['c_count'],
                                           toc=toc
                                           ).replace('CSS_STYLE_INSERT',
                                                     c.INFOS_CSS)
        elif mode == 's':

            # Only keeping what we whant from the tokens
            tk = self.ifs['tk']
            patterns = (r' Rated: ',
                        r' - Words: .*',  # Deleted because not every fanfic
                                          # has several chapters
                        r' - Chapters: \d*',
                        )
            for pattern in patterns:
                tk = re.sub(pattern, '', tk)

            # Informations are ready to be saved in plain text file
            return (f"{self.ifs['c_count']}\n"
                    f"{self.ifs['status'][8:]}\n"
                    f"{self.ifs['s_dir']}/{self.ifs['t_id']}_infos.html\n"
                    f"{self.ifs['smry']}\n"
                    f"{self.ifs['title']}\n"
                    f"{self.ifs['uni']}\n"
                    f"{self.ifs['url']}\n"
                    f"{self.ifs['w_count']}\n"
                    f"{self.ifs['auth']}\n"
                    f"{tk}\n"
                    )
        else:
            raise ValueError(f"'mode' cannot be '{mode}', only 'h' or 's'.")

    def _format_chapter(self, c_text: str, c_num: int) -> str:
        """
        Formats a given chapter.

        Args:
            c_text (str): the chapter to use, in its basic form from FFN,
            c_num (int): the number of the chapter.

        Returns:
            The formatted chapter, as a `str`.
        """
        # NOTE:
        # lk is used for an internal link (to a local file)
        # url is used for an external link (to FFN.net most likely)

        # Some hard formatting, allow for better readability in Web Inspectors
        c_text = c_text.replace('<p>', '\n<p>\n    ')
        c_text = c_text.replace('</p>', '\n</p>')

        c_count = self.ifs['c_count']
        lgth = len(str(c_count))
        p_lk = ''  # Link to the previous chapter
        n_lk = ''  # Link to the next chapter
        page_title = self.ifs['title']

        if c_count > 1:
            c_title = self.ifs['chap'][c_num - 1]
            page_title += f' | Ch. {c_title}'
            if c_num > 1:
                p_lk = (f"<a href='{str(c_num - 1).zfill(lgth)}.html'>"
                        f"Previous ({c_num - 1}/{c_count})</a> "
                        f"<em>{self.ifs['chap'][c_num - 2]}</em>"
                        )

            if c_num < c_count:
                n_lk = (f"<a href='{str(c_num + 1).zfill(lgth)}.html'>"
                        f"Next ({c_num + 1}/{c_count})</a> "
                        f"<em>{self.ifs['chap'][c_num]}</em>"
                        )
        else:
            c_title = self.ifs['title']
            page_title += f' | Ch. 1'

        auth_url = f"{c.AUTH_URL}{self.ifs['auth_id']}/"
        ifs_lk = f"{self.ifs['t_id']}_infos.html"

        # Link to the info file and to the author's page
        links = (f"<span class='small'><em><strong><a href='{ifs_lk}'>"
                 f"{self.ifs['title']}</a></strong></em> | "
                 f"<em><a href='{auth_url}'>{self.ifs['auth']}</a></em></span>"
                 )

        return c.CHAP_TEMPLATE.format(ttl=page_title,
                                      prev_link=p_lk,
                                      lks=links,
                                      chap_title=c_title,
                                      chap_text=c_text,
                                      next_link=n_lk)

    def get_chapter(self, c_num: int) -> str:
        """
        Gets the *c_num* chapter.

        Args:
            c_num (int): the number of the chapter.

        Returns:
            Returns a chapter in its formatted form, ready to be filed.

        Raises:
            ValueError(f"{c_num} not in range [1; {c_count}].")
        """
        c_count = self.ifs['c_count']
        if not 0 < c_num <= c_count:
            raise ValueError(f"{c_num} not in range [1; {c_count}].")

        page = tls.get_page(f"{c.ROOT_URL}{self.ifs['n_id']}/{c_num}/")

        chap = c.BEGINNING + page.split(c.BEGINNING, 1)[1]
        if c_count > 1:
            chap = chap.split(c.END_MANY, 1)[0]
        else:
            chap = chap.split(c.END_ONE, 1)[0]

        return self._format_chapter(chap, c_num)


class StoryWriter(object):
    """
    Writes stories.

    Initialization:
        display[True] (bool): Indicates if messages are displayed on stdout.

    Public methods:
        write_infos(self, st: Story)
        create(self, st: Story) -> (int)
        update(self, st: Story) -> (int)

    Public attributes:
        self.display (bool): see above
    """

    def __init__(self, display=True):
        """
        __init__ method, set the *self.display* paramater from *display* (bool)
        """
        self.display = display

    @staticmethod
    def _write_css():
        """
        Write the CSS file used for the files.
        """

        with open('style.css', 'w', encoding='utf-8') as f:
            f.write(c.FFN_CSS)

    def _write_chapters(self, st: Story, frm: int, to: int):
        """
        Writes chapters of story *st* from *frm* to *to*.

        Args:
            st (Story): the story whose chapters will be written.
            frm (int): the number of the first chapter to write.
            to (int): the number of the last chapter to write.

        N.B:
            *frm* and *to* are assumed to be valid: 1 <= frm/to <= c_count.
        """

        c_count = st.ifs['c_count']
        lgth = len(str(c_count))

        for c_num in range(frm, to):

            f_title = f'{str(c_num).zfill(lgth)}.html'
            text = st.get_chapter(c_num)

            if self.display:
                print(f"DOWNLOADED: n° {str(c_num).zfill(lgth)} /{c_count}",
                      end=' -- ')

            with open(f_title, 'w', encoding='utf-8') as f:
                f.write(text)

            if self.display:
                print("SAVED.")

    def write_infos(self, st: Story):
        """
        Writes the informations (h and s) about *st*.

        Args:
            st (Story): the story whose informations will be written.

        N.B:
            Assumes the current directory is the valid one.
        """

        file_title = f".{st.ifs['n_id']}"
        with open(file_title, 'w', encoding='utf-8') as f:
            f.write(st.get_infos('s'))

        file_title = f"{st.ifs['t_id']}_infos.html"
        with open(file_title, 'w', encoding='utf-8') as f:
            f.write(st.get_infos('h'))

        if self.display:
            print(f"DONE -- {file_title}")

    def create(self, st: Story) -> (int):
        """
        Downloads a full story and creates all the files needed: infos/chaps.

        Args:
            st (Story): the story to download.

        Returns:
            0 - the story was added for the first time to the directory
            1 - an older version was replaced
        """
        replacement = 0
        s_dir = st.ifs['s_dir']
        try:
            os.mkdir(s_dir)
        except FileExistsError:
            for file in os.listdir(s_dir):
                os.remove(f'{s_dir}{os.sep}{file}')
            os.rmdir(s_dir)
            os.mkdir(s_dir)
            replacement = 1
        finally:
            os.chdir(s_dir)

        StoryWriter._write_css()
        self.write_infos(st)
        self._write_chapters(st, 1, st.ifs['c_count'] + 1)

        return replacement

    def update(self, st: Story) -> (int):
        """
        Downloads the missing chapters of *st* and update informations about it

        Args:
            st (Story): the story which will be updated.

        Returns:
            0 - the story was added for the first time to the directory
            1 - the story was updated correctly
            2 - the story was already up-to-date
        """

        old_chap_files = []
        try:
            os.chdir(st.ifs['s_dir'])
        except FileNotFoundError:
            if self.display:
                print('[ERROR]: Story was not present in the directory, full '
                      'download is now started.\n\n')
            self.create(st)
            # Full download done
            return 0
        else:
            for file in sorted(os.listdir()):
                if re.fullmatch(c.CHAPTER_FILE_REGEX, file) is not None:
                    old_chap_files.append(file)

        StoryWriter._write_css()
        self.write_infos(st)

        old_chap_count = len(old_chap_files)
        c_count = st.ifs['c_count']

        if old_chap_count == c_count:
            if self.display:
                print('Story already up-to date. No actions undertaken.')
            # Story already up-to-date
            return 2

        # Update the old chapters to the new 'c_count' (In the 'previous' and
        # 'next' links)
        for file in old_chap_files:

            with open(file, 'r', encoding='utf-8') as f:
                c_text = f.read()

            p_lk = re.search(c.PREVIOUS_REGEX, c_text)
            n_lk = re.search(c.NEXT_REGEX, c_text)

            try:
                tmp = p_lk.group(0)
                new_p_lk = tmp.replace(f'/{p_lk.group(1)}', f'/{c_count}')
            except AttributeError:
                pass
            else:
                c_text = c_text.replace(tmp, new_p_lk)

            try:
                tmp = n_lk.group(0)
                new_n_lk = tmp.replace(f'/{n_lk.group(1)}', f'/{c_count}')
            except:
                pass
            else:
                c_text = c_text.replace(tmp, new_n_lk)

            with open(file, 'w', encoding='utf-8') as f:
                f.write(c_text)

        self._write_chapters(st, old_chap_count, c_count + 1)

        # All good
        return 1

    def update_infos(self, st: Story):
        """
        Updates the informations of a given story.

        Args:
            st (Story): the story whose informations will be updated.
        """
        base_dir = os.getcwd()
        os.chdir(st.ifs['s_dir'])

        self.write_infos(st)

        os.chdir(base_dir)
