__version__ = '2018.06.28'
__author__ = 'Alexis BOURGET'


class Story:
    """
    The base class for each site. It provides a model but none of the
    methods are implemented. Calling them will raise a NotImplementedError
    because each of them are site-dependant.

    All the basic properties are:

        :param str site: the site from which hails the story. It corresponds to
          a key in the `constants.SITES` dictionary
        :param str url: the url to the relevant web page for the story
        :param str relative_path: name of the folder containing the story's
          directory. **Should be lower_case**
        :param str story_dir: name of the folder containing the story itself.
          **Should be lower_case**
        :param str author: name of the author
        :param str title: title of the story
        :param int chapter_count: number of chapters in the story
        :param list chapters: titles of the different chapters. Some stories do
          not have any (like one-shots on fanfiction.net): in this case, having
          it empty or filled with the story's title is ok
        :param int word_count: number of words in the story
        :param str status: Either "Complete" or "In Progress". Anything else
          will result in undefined behaviors in the statistics files.
        :param str language: the main language in which the story is written
        :param str universe: the universe of the story (Harry Potter, Star Wars,
          ...)
        :param str tokens: miscellaneous informations about the story, like
          characters, rating, update/publication date
        :param str curated_tokens: the tokens used when building the statistics
        :param str summary: the summary of the story

    Except for `url`, none of the values are initialized to force you to do it
    when subclassing.
    """
    def __init__(self, url: str):

        # Site where the story was originally found
        # Should be part of the base url of the site (like 'fanfiction.net')
        self.site: str

        # URL of the story (first chapter of index, depending on the site)
        self.url = url
        # Path to the story directory from the base directory
        self.relative_path: str
        # Directory containing the story
        self.story_dir: str

        # Author of the story
        self.author: str
        # Title of the story
        self.title: str

        # The number of chapters in the story
        self.chapter_count: int
        # Titles of the different chapters
        self.chapters: list
        # The number of words in the story
        self.word_count: int
        # Is the story 'Complete' or 'In Progress' ?
        self.status: str

        # The language in which the story is written
        self.language: str
        # The universe from which the story comes
        self.universe: str
        # Miscellaneous informations about the story, most notably used when
        # writing the informations about the story
        self.tokens: str
        # The tokens used to build the statistics
        self.curated_tokens: str
        # Summary of the story
        self.summary: str

    def __str__(self) -> str:

        return (
            f'Site: {self.site}\n'
            f'URL: {self.url}\n'
            f'Relative_path: {self.relative_path}\n'
            f'Story directory: {self.story_dir}\n'
            f'Author: {self.author}\n'
            f'Title: {self.title}\n'
            f'Chapter count: {self.chapter_count}\n'
            f'Chapters: {self.chapters}\n'
            f'Word count: {self.word_count}\n'
            f'Status: {self.status}\n'
            f'Language: {self.language}\n'
            f'Universe: {self.universe}\n'
            f'Tokens: {self.tokens}\n'
            f'Curated tokens: {self.curated_tokens}\n'
            f'Summary: {self.summary}\n'
        )

    def get_informations_title(self) -> str:
        """
        Format to use for the title: {file_title}_informations.html
        Using lower case or not do not matter (when used, it will be transformed
        to lower case) but it preferably should

        :return: The 'file_title' part of the format above, in lower case
        """
        raise NotImplementedError

    def get_author(self) -> str:
        """
        :return: the author's name (can also be a link to the author's page)
                 See ffn_net.py for an example
        """
        raise NotImplementedError

    def get_universe(self) -> str:
        """
        :return: the universe (can also be a link to the universe page on the
                 site)
        """
        raise NotImplementedError

    def get_chapter(self, num_chapter: int) -> str:
        """
        Get the wanted chapter components for the current story

        :param num_chapter: the number of the chapter wanted
        :return: the string containing the text of the chapter, html and all.
                 It should not be a full html web page, just the part containing
                 the chapter's content. Any other information is to be excluded
                 if possible, to avoid any duplicates.

        For more informations about how this text will be used when writing the
        chapter, see constants.CHAPTER_TEMPLATE
        """
        raise NotImplementedError
