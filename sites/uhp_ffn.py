__version__ = '2018.06.28'
__author__ = 'Alexis BOURGET'

import re

import utilities.tools as tls

import sites.story as st
import sites.uhp_ffn_constants as uhp_cst


class UHP(st.Story):
    """
    Represent a story coming from the ultimatehpfanfiction.com website
    """
    def __init__(self, url: str):

        self.site = 'ultimatehpfanfiction.com'
        self.relative_path = 'uhp-fanfiction'

        # Get the important parts of the URL
        parts = url.split('/')[3:]

        # Careful, this URL may not be unique
        super(UHP, self).__init__(
            f'https://www.ultimatehpfanfiction.com/{parts[0]}/{parts[1]}'
        )

        # This site only hosts completed stories written in English
        self.status = 'Complete'
        self.language = 'English'
        # That one is a given, just look at the name of the site
        self.universe = 'Harry Potter'

        # Get the page containing the informations
        base_page = tls.get_page(
            self.url
        ).split(
            uhp_cst.INFORMATIONS_BEGINNING
        )[1].split(
            uhp_cst.INFORMATIONS_END
        )[0]

        # Remove those pesky tabulations and format the informations a little
        base_page = re.sub(r'\t*', '', base_page).replace('<tr>', '\n<tr>')

        # If the story is part of a series, ensures we get the informations
        # about the correct story, or, if nothing is precised, about the first
        # in the series
        try:
            pos = parts[2] if parts[2] != '' else 'a'
        except IndexError:
            pos = 'a'

        for result in re.finditer(uhp_cst.RE_INFORMATIONS, base_page):
            parts = result.group(1).split('/')[1:]
            if pos == parts[2]:

                # Used to access the chapters
                self.__chapter_link = (
                    f'{self.url}/{pos}/CHAPTER_NUM/{"/".join(parts[4:])}'
                )

                # Ensure the URL is unique
                self.url = f'{self.url}/{pos}/0/{"/".join(parts[4:])}'

                self.chapter_count = int(parts[-1])
                self.chapters = []
                for i in range(1, self.chapter_count + 1):
                    self.chapters.append(f'Chapter {i}')

                self.title = result.group(2)
                self.author = result.group(3)
                self.word_count = int(result.group(4))
                self.curated_tokens = (
                    f'{result.group(5)} - {result.group(6).replace(" ", "/")}'
                )
                self.tokens = (
                    f'{self.curated_tokens} - Words: {self.word_count:,}'
                )
                self.summary = result.group(7)
                self.story_dir = '_'.join((
                    # Story title + author
                    re.sub(r'[^a-z\d]', '-', self.title.lower()),
                    re.sub(r'[^a-z\d]', '-', self.author.lower()),
                ))

                # No need to do more tests since the informations were found
                break

    def get_informations_title(self) -> str:
        return re.sub('[^a-z\d]', '-', self.title.lower())

    def get_author(self) -> str:
        return self.author

    def get_universe(self) -> str:
        return self.universe

    def get_chapter(self, num_chapter: int) -> str:

        page = tls.get_page(
            self.__chapter_link.replace('CHAPTER_NUM', str(num_chapter))
        )

        # Remove the parts of the page that are not the chapter itself
        page = re.split(uhp_cst.CHAP_BEGINNING, page)[1]
        page = re.split(uhp_cst.CHAP_END, page)[0]

        return page
