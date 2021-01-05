__version__ = '2018.07.13'
__author__ = 'Alexis BOURGET'

import sqlite3 as sql

import utilities.tools as tls
import utilities.constants as cst


class DataHandler:
    """
    DataHandler class. It provides a controlled link to the database and offer
    some methods which accelerates common operations for this program.

    URLs are the primary key for this database (it seems logical that
    to one url correspond one story)
    """
    def __init__(self, database_file: str):

        self.__logger = tls.setup_logging('DataHandler')

        # Connection to the database
        self.__conn = sql.connect(database_file)
        # Cursor
        self.__cur = self.__conn.cursor()

        try:
            self.__cur.execute(cst.STORIES_TABLE_CREATION)
        # Error if the table already exists
        except sql.OperationalError as err:
            self.__logger.debug(f'DataHandler: {err}')
        else:
            self.__conn.commit()
            self.__logger.info('Database setup-ed')

    def add_story(self, st_obj):
        """
        Adds a story to the database, deleting any previous save of it. If the
        story is already present, it keeps the following values to ensure a
        smooth experience by not making the user enter them again:

            - read
            - series
            - position

        It is also used to update stories since it cost almost nothing to do it
        this way instead of choosing what to update

        :param st_obj: the story to add. Should be an object inheriting from
                      the Story class.
        """
        self.__logger.info(f'Saving "{st_obj.title}" ("{st_obj.url}")')
        # Defaults values
        read = False
        series = ''
        position = 0
        # Ensure the previous entry is deleted if necessary while saving all
        # user-entered values
        command = 'SELECT read, series, position FROM stories WHERE url="{}"'
        self.__cur.execute(command.format(st_obj.url))
        try:
            self.__logger.debug('Recuperating older values for continuity')
            result = self.__cur.fetchmany(1)
            # Getting older values to ensure continuity
            read = bool(result[0][0])
            series = str(result[0][1])
            position = int(result[0][2])
        except IndexError:
            self.__logger.debug('No older values were found')
        else:
            self.__logger.debug('Story was already saved: deleting it')
            self.__cur.execute(f'DELETE FROM stories WHERE url="{st_obj.url}"')
            self.__logger.debug('Story deleted')

        # To avoid any surprises later on
        if st_obj.status.lower() not in ['complete', 'in progress']:
            self.__logger.debug('Unknown status, setting it to "In Progress"')
            st_obj.status = 'In Progress'

        command = 'INSERT INTO stories VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
        values = (
            st_obj.url,
            # path_to_index
            '{}/{}/{}_informations.html'.format(
                st_obj.relative_path,
                st_obj.story_dir,
                st_obj.get_informations_title(),
            ).lower(),
            st_obj.site,
            st_obj.author,
            st_obj.title,
            st_obj.chapter_count,
            st_obj.word_count,
            st_obj.status,
            st_obj.language,
            st_obj.universe,
            st_obj.summary,
            st_obj.curated_tokens,
            read,
            series,
            position,
        )

        self.__cur.execute(command, values)
        self.__conn.commit()
        self.__logger.debug('Story added')

    def delete_story(self, url: str):
        """
        Deletes the given url

        :param url: url of the story to be deleted completely from the database
        """
        self.__logger.info(f'Deleting "{url}" from the database')
        self.__cur.execute(f'DELETE FROM stories WHERE url="{url}"')
        self.__conn.commit()
        self.__logger.debug(f'Deleted')

    def get_value_by_url(self, column: str, url: str) -> list:
        """
        Get a value from a given url

        :param column: the column containing the wanted value
        :param url: the url to check for
        :return: an empty list if the url wasn't found, else a list containing
                 the wanted value in position [0]
        """
        self.__logger.info(f'Getting "{column}" for "{url}"')
        self.__cur.execute(f'SELECT {column} FROM stories WHERE url="{url}"')
        values = [elem[0] for elem in self.__cur.fetchall()]
        self.__logger.debug(f'Got: {values}')
        return values

    def update_by_url(self, column: str, value, url: str):
        """
        Update a value for a given url

        :param column: the column in which the value should be updated
        :param value: the new value to use
        :param url: the url for which this change should take place
        """
        self.__logger.info(f'Setting "{column}" to {value} for "{url}"')
        if type(value) == str:
            # Ensure there is no bug with the sql
            value = value.replace('"', "'")
            cmd = f'UPDATE stories SET {column}="{value}" WHERE url="{url}"'
            self.__logger.debug('Special handling is required')
        else:
            value = int(value)
            cmd = f'UPDATE stories SET {column}={value} WHERE url="{url}"'
            self.__logger.debug('No special handling required')

        self.__cur.execute(cmd)
        self.__conn.commit()
        self.__logger.debug('Set')

    def get_column(self, column: str, distinct=False, where=None) -> list:
        """
        Get the values for a given column from the database

        :param column: the wanted column (must be present in the stories table)
        :param distinct: all the values or only the distinct one ?
        :param where: to select more precisely. Should follow the pattern:
            {column for the where}={value} if the value is numeric/boolean
            {column for the where}="{value}" if it is a string
        :return: the different values for the wanted column
        """
        self.__logger.info(
            f'Getting "{column}" with distinct={distinct} WHERE {where}'
        )
        if distinct:
            command = f'SELECT DISTINCT {column} FROM stories'
        else:
            command = f'SELECT {column} FROM stories'

        if where is not None:
            command += f' WHERE {where}'

        self.__cur.execute(command)
        values = [elem[0] for elem in self.__cur.fetchall()]
        self.__logger.debug(f'Got: {values}')
        return values

    def get_stories_by_site(self, site: str) -> list:
        """
        Get the stories coming from 'site' and **append** them in 'to_list'.
        Modify 'to_list' in place (like list.sort() does).

        Be sure to empty 'to_list' before, because no check is done.

        :param site: the site to check for
        :return: the list containing the stories, sorted by title
        """
        self.__logger.info(f'Getting the stories for site: "{site}"')
        self.__cur.execute(f'SELECT * FROM stories WHERE site="{site}"')
        # Sort the stories by title
        stories = sorted(self.__cur.fetchall(), key=lambda st: st[4])
        self.__logger.debug(f'Got: {stories}')
        return stories

    def get_urls_by_series(self, series: str) -> list:
        """
        Get the urls belonging to a given series

        :param series: the series to check for
        :return: the urls belonging to this series, unsorted
        """
        self.__logger.info(f'Getting the stories for series: "{series}"')
        self.__cur.execute(f'SELECT url FROM stories WHERE series="{series}"')
        stories = [elem[0] for elem in self.__cur.fetchall()]
        self.__logger.debug(f'Got: {stories}')
        return stories
