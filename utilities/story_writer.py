__version__ = '2018.06.30'
__author__ = 'Alexis BOURGET'

import os
import re
import datetime

import utilities.tools as tls
import utilities.constants as cst

################################################################################
# This part is to be updated each time a new site is added
# Yes it will be horribly long if there are 100+ sites. We will burn that bridge
# when we get to it

# IMPORT HERE ALL THE SITES MODULES
import sites.ffn_net as ffn_net
import sites.uhp_ffn as uhp_ffn

# For each site add their relevant class and their identifier under the form
# SITES[site_name] = (site_class, site_identifier)

# - The key is what will be used in the statistics and the ComboBox in the UI so
#   choose a good name or abbreviation for the site it represents
# - The first element of the tuple is the access to the class
# - The second is a identifier used to check if a story belongs to the site.
# It should be unique amongst the handled sites (be aware of both mobile and
# desktop urls if they exist), meaning 'fanfiction' and 'fanfiction.net' cannot
# both be identifiers for different sites since the second risk capturing the
# first each time a check is made. The check is made using the re.search()
# method from the re module so do not hesitate to use regex to ensure the
# closest possible match
# NOTE: The identifier can be equal to the key but it's not required at all

# ADD HERE THE SITE, THE ACCESS TO ITS CLASS AND ITS IDENTIFIER

# fanfiction.net has a mobile version and a desktop version with different base
# urls so the identifier cannot be more precise
cst.SITES['fanfiction.net'] = (
    ffn_net.FFN,
    r'https://(?:www)?(?:m)?.fanfiction.net/s/\d+/\d+.*?'
)
cst.SITES['ultimatehpfanfiction.com'] = (
    uhp_ffn.UHP,
    r'https://www.ultimatehpfanfiction.com/.+?'
)

################################################################################


class StoryWriter:
    """
    Writes stories, one at a time. It can only handle url which hails from
    handled site (sites for which a class exists and has been added in the
    `SITES` variable).

    Use `.set_url(url: str)` each time you want to setup a new story to be
    downloaded or updated.

    To only update the informations, use `.write_informations()`.
    To download or update, use either `.download()` or `.update()` accordingly.

    The css corresponding to the action is automatically written in the `0/css/`
    directory.
    """

    def __init__(self):

        self.__logger = tls.setup_logging('StoryWriter')

        self.story = None
        self.folder = ''

    def set_url(self, url: str):
        """
        Set the new url to use for the writer

        :param url: the new url to use
        :raise: AttributeError if the url does not belong to a handled site
                Internet related errors if the connection fails
        """
        del self.story
        self.story = None
        for site_class, site_identifier in cst.SITES.values():
            if re.search(site_identifier, url) is not None:
                self.__logger = tls.setup_logging(
                    f'StoryWriter | {site_class.__name__}'
                )
                self.__logger.info(f'Setting {site_class.__name__}("{url}")')
                self.story = site_class(url)
                self.__logger.debug('Set')
                break

        folder = f'{self.story.relative_path}/{self.story.story_dir}/'
        self.folder = folder.lower()

    def __write_chapters(self, frm: int, end: int):
        """
        Write the chapters between the given limits (including those limits)

        :param frm: the first chapter to be written
        :param end: the last chapter to be written
        """
        self.__logger.info(f'Writing chapters from {frm} to {end}')

        # Writing the chapter's css
        self.__logger.debug('Writing chapter css')
        with open('0/css/chapter_style.css', 'w', encoding='utf-8') as f:
            f.write(cst.CHAPTER_CSS)

        if not 0 < frm <= end <= self.story.chapter_count:
            raise ValueError(f'Invalid interval of chapters [{frm}:{end}]')

        length = len(str(self.story.chapter_count))

        # Link to the informations file, which is the same for each chapter
        index_link = cst.LINK_BASE.format(
            'index',
            f'{self.story.get_informations_title()}_informations'.lower(),
            f'{self.story.title} by {self.story.author}'
        )

        for chapter_num in range(frm, end + 1):

            self.__logger.debug(f'Writing chapter {chapter_num}')

            # Link to the previous chapter in case none exists
            previous_link = "<a class='previous'>Nothing more this way</a>"
            # Link to the next chapter in case none exists
            next_link = "<a class='next'>Nothing more this way</a>"

            if len(self.story.chapters) == 0:
                chapter_title = self.story.title
            # Chapters title are accessible
            else:
                chapter_title = self.story.chapters[chapter_num - 1]

                if chapter_num > 1:
                    previous_link = cst.LINK_BASE.format(
                        'previous',
                        str(chapter_num - 1).zfill(length),
                        f'<< {chapter_num - 1} <<'
                    )
                if chapter_num < self.story.chapter_count:
                    next_link = cst.LINK_BASE.format(
                        'next',
                        str(chapter_num + 1).zfill(length),
                        f'>> {chapter_num + 1} >>'
                    )

            file_title = f'{str(chapter_num).zfill(length)}.html'
            with open(self.folder + file_title, 'w', encoding='utf-8') as f:
                f.write(cst.CHAPTER_TEMPLATE.format(
                    page_title=f'{self.story.title} | {chapter_num}',
                    previous_link=previous_link,
                    index_link=index_link,
                    next_link=next_link,
                    chapter_title=chapter_title,
                    chapter_text=self.story.get_chapter(chapter_num),
                ))

            self.__logger.debug('Chapter written')

        self.__logger.debug('Chapters written')

    def write_informations(self):
        """
        Write the informations for the current story
        """
        self.__logger.info('Writing informations')

        # Writing the css
        with open('0/css/informations_style.css', 'w', encoding='utf-8') as f:
            f.write(cst.INFORMATIONS_CSS)

        file_title = f'{self.story.get_informations_title()}_informations.html'
        date = datetime.datetime(1, 1, 1).today().strftime('%H:%M - %d %B %Y')

        table_of_contents = ''

        length = len(str(self.story.chapter_count))
        if len(self.story.chapters) == 0:
            self.story.chapters = [self.story.title]
            length = 1

        for i, chapter in enumerate(self.story.chapters):
            table_of_contents += (
                f"<a class='chapter' href='{str(i+1).zfill(length)}.html'>"
                f"{self.story.chapters[i]}</a>\n"
            )

        with open(self.folder + file_title.lower(), 'w', encoding='utf-8') as f:
            f.write(cst.INFORMATIONS_TEMPLATE.format(
                story_title=self.story.title,
                site=self.story.site,
                author=self.story.get_author(),
                writing_date=date,
                universe=self.story.get_universe(),
                url=self.story.url,
                summary=self.story.summary,
                tokens=self.story.tokens,
                chapter_count=self.story.chapter_count,
                table_of_contents=table_of_contents,
            ))

        self.__logger.debug('Informations written')

    def download(self):
        """
        Fully download the current story, deleting any previous save of it
        """
        self.__logger.info("Downloading story")

        try:
            os.makedirs(self.story.relative_path.lower())
        except FileExistsError:
            self.__logger.debug('Site directory exists')
        else:
            self.__logger.debug(f'Created: {self.story.relative_path.lower()}')

        try:
            os.mkdir(self.folder)
        except FileExistsError:
            self.__logger.debug('Story directory existed: deleting it')
            for file in os.listdir(self.folder):
                os.remove(self.folder + file)
            os.rmdir(self.folder)
            os.mkdir(self.folder)
            self.__logger.debug('Story directory deleted')
        else:
            self.__logger.debug(f'Created: {self.folder}')

        self.write_informations()
        self.__write_chapters(1, self.story.chapter_count)

        self.__logger.debug('Story downloaded')

    def update(self):
        """
        Update the current story, adding the missing content (if there is any)
        to any previous save of it or downloading it fully if it had not been
        saved before

        If it has been downloaded and the site does not allow update, nothing is
        done
        """
        self.__logger.info('Updating story')

        # Story wasn't present already
        if not os.path.isdir(self.folder):
            self.download()
            return

        # Check at which chapter is the first discontinuity
        # If there are none, highest_chapter is the number of chapter already
        # downloaded
        highest_chapter = 0
        for file in sorted(os.listdir(self.folder)):
            result = re.fullmatch(r'(\d*).html', file)
            # If the file is a chapter
            if result is not None:
                # If there is no discontinuity, prepare the next check
                if int(result.group(1)) == highest_chapter + 1:
                    highest_chapter += 1
                else:
                    break

        # The story was registered but no chapter has been downloaded or they
        # were manually deleted outside of the application
        if highest_chapter == 0:
            self.download()
            return
        else:
            self.__logger.debug(f'{highest_chapter} chapters already present')

        # Passed a number like 9->10, 99->100, 999->1000 and so changed all
        # the internal links. Easier to update them by downloading all again
        # Yes, that's laziness but it shouldn't happen that often except for
        # the 9->10 which is not that costly to do
        if len(str(highest_chapter)) < len(str(self.story.chapter_count)):
            self.__logger.info(
                f'{highest_chapter} chapters are present and story has '
                f'currently {self.story.chapter_count} chapters'
            )
            self.download()
            return
        else:
            self.__logger.debug('No re-download due to 9->10 like change')

        # Update the informations
        self.write_informations()

        # Story already up-to-date
        if highest_chapter == self.story.chapter_count:
            self.__logger.info('Story already up-to-date')
            return

        # Always rewrite the last correct chapter to ensure the link to the next
        # one is correct
        self.__write_chapters(highest_chapter, self.story.chapter_count)

        self.__logger.debug('Story updated')
