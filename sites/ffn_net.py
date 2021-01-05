__version__ = '2018.07.13'
__author__ = 'Alexis BOURGET'

import re

import utilities.tools as tls

import sites.story as st
import sites.ffn_net_constants as ffn_cst


class FFN(st.Story):
    """
    Represent a story coming from the fanfiction.net website.
    """
    def __init__(self, url: str):

        self.site = 'fanfiction.net'
        # Same as self.site but it's not required
        self.relative_path = 'fanfiction.net'

        # Numerical id used to identify stories at fanfiction.net
        self.__num_id = url.split('/')[4]

        # Initialize the url
        super(FFN, self).__init__(
            f'https://www.fanfiction.net/s/{self.__num_id}/1/'
        )

        # Initialize everything else

        page = tls.get_page(self.url)
        tokens = FFN.__get_tokens(page)
        self.title = FFN.__get_title(page)

        self.chapter_count = FFN.__get_chap_count(tokens)
        self.status = FFN.__get_status(tokens)
        self.language = tokens.split(' - ')[1]
        self.tokens = FFN.__insert_status(tokens, self.status)
        self.curated_tokens = FFN.__get_curated_tokens(tokens)
        self.word_count = FFN.__get_words_count(tokens)

        self.author = re.search(ffn_cst.RE_AUTHOR, page).group(1)
        self.summary = re.search(ffn_cst.RE_SUMMARY, page).group(1)
        self.universe = re.search(ffn_cst.RE_UNIVERSE, page).group(2).title()
        self.chapters = re.findall(ffn_cst.RE_CHAPTERS,
                                   page)[:self.chapter_count]

        # ID used to identify the author of the story
        self.__author_id = re.search(ffn_cst.RE_AUTHOR_ID, page).group(1)
        # Textual ID which is basically the title of the story in lower case
        # with all non-alphanumeric characters replaced by -
        self.__text_id = tls.clean(re.search(ffn_cst.RE_TEXT_ID,
                                             page).group(1)
                                   ).lower()

        # The self.__num_id ensure it is unique to the story
        self.story_dir = f'{self.__text_id}_{self.__num_id}'

    @staticmethod
    def __get_tokens(page: str) -> str:
        """
        Get the tokens from a fanfiction.net HTML page

        :param page: the HTML page to use
        :returns: The tokens
        """
        return re.sub(ffn_cst.RE_HTML_FROM_TOKENS,
                      '',
                      re.search(ffn_cst.RE_TOKENS, page).group(1))

    @staticmethod
    def __get_curated_tokens(tokens: str) -> str:
        """
        Curate the tokens for the statistics

        :param tokens: the raw tokens
        :returns: The tokens curated
        """
        patterns = (
            r'.Rated: ',
            # Deleted because not every fanfic has several chapters
            r' - Words: .*',
            r' - Chapters: \d*',
        )
        for pattern in patterns:
            tokens = re.sub(pattern, '', tokens)

        return tokens

    @staticmethod
    def __get_title(page: str) -> str:
        """
        Ensure the title is properly formatted

        :param page: the HTML page from which to get the title
        :returns: the title formatted
        """
        title = re.search(ffn_cst.RE_STORY_TITLE, page).group(1).title()

        # Corrections because .title() mess up with letters after '
        to_correct = (
            ('’', "'"),
            ("'S ", "'s "),
            ("'T ", "'t "),
            ("'M ", "'m "),
            ("'Ll ", "'ll "),
            ("'Ve ", "'ve "),
            ("'Re ", "'re "),
        )
        for old, new in to_correct:
            title = title.replace(old, new)

        return title

    @staticmethod
    def __get_chap_count(tokens: str) -> int:
        """
        Gets the number of chapter from the tokens of a story

        :param tokens: the tokens to use
        :returns: The number of chapters as an `int`
        """
        try:
            chap_count = re.search(ffn_cst.RE_CHAPTER_COUNT, tokens).group(1)
        except AttributeError:
            chap_count = '1'
        return int(chap_count.replace(',', ''))

    @staticmethod
    def __get_words_count(tokens: str) -> int:
        """
        Gets the number of words from the tokens of a story

        :param tokens: the tokens to use
        :returns: The number of words as an `int`
        """
        words_count = re.search(ffn_cst.RE_WORD_COUNT, tokens).group(1)
        return int(words_count.replace(',', ''))

    @staticmethod
    def __get_status(tokens: str) -> str:
        """
        Gets the status from the tokens of a story

        :param tokens: the tokens to use
        :returns: The status as a `str`
        """
        status = re.search(ffn_cst.RE_STATUS, tokens)
        return 'In Progress' if status is None else 'Complete'

    @staticmethod
    def __insert_status(tokens: str, status: str) -> str:
        """
        Inserts the status in the tokens of a story

        :param tokens: the tokens to use
        :param status: the status to insert
        :returns: The tokens as a `str` with the correct status in it
        """
        if 'Status: Complete' in tokens:
            return tokens
        else:
            return tokens.replace('- id:', f'- {status} - id:')

    # Below are the implementations of the methods inherited from story.Story
    # For the documentation about those, see the base Story class

    def get_informations_title(self) -> str:
        return self.__text_id

    def get_author(self) -> str:
        """
        :return: the author name's embedded in a link to their page
        """
        author_url = f'https://www.fanfiction.net/u/{self.__author_id}/'
        return f"<a href='{author_url}'>{self.author}</a>"

    def get_universe(self) -> str:
        # TODO: Do not handle a link to the universe yet, correct that
        return self.universe

    def get_chapter(self, chapter_num: int) -> str:

        page = tls.get_page(
            f'https://www.fanfiction.net/s/{self.__num_id}/{chapter_num}/'
        ).replace('noshade>', 'noshade/>')

        page = ffn_cst.CHAP_BEGINNING + page.split(ffn_cst.CHAP_BEGINNING, 1)[1]
        if self.chapter_count > 1:
            page = page.split(ffn_cst.CHAP_END_MANY, 1)[0]
        else:
            page = page.split(ffn_cst.CHAP_END_ONE, 1)[0]

        return page
