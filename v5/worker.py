"""
File: worker.py
Author: BOURGET Alexis
License: see LICENSE.txt
App version: 5.0
File version: 2.0

Contains functions which can be used for real-life use of this app.
Can also be used directly in a shell, see 'python3.6 worker.py help' for help.
"""

import os
import sys
import story
import stats
import main as m
import tools as tls


class OnComputer(object):
    """
    Handles the managing of several fanfictions and folders containing
    fanfictions.

    Public methods:
        update_infos_in_paths(self, paths: list)
        update_stats(self, paths: list, renew=False, main=True)
        update_stories(self, dic: dict)
        finished_story(self)
        new_stories(self, dic)

    Public attribute:
        M_PATH (str): Root of the directory tree containing the fanfictions.
    """

    def __init__(self, m_path: str):
        """
        Initializes 'OnConputer'.

        Args:
            m_path (str): The path to the directory tree containing the
                          targeted fanfictions.
        """
        self.M_PATH = m_path

    def update_infos_in_paths(self, paths: list):
        """
        Update the informations of all the stories contained in all the *dirs*.

        Args:
            paths (list): the pathes containing the stories.
        """
        base_dir = os.getcwd()

        for path in paths:

            tls.chdir(self.M_PATH + path if path[0] != '/' else path)

            urls = tls.get_urls_from_folder(os.getcwd())
            writer = story.StoryWriter()

            for url in urls:
                st = story.Story(url)
                writer.update_infos(st)
                del st

        os.chdir(base_dir)

    def update_stats(self, paths: list, renew=False, main=True):
        """
        Update the stats.html from all *paths* and then in *M_PATH* if asked,
        and only after having renewed the informations for each story in these
        *paths* if *renew* is True.

        Args:
            paths (list): the paths where the stats must be renewed.
            renew[False] (bool): indicates if the informations are to be
                                 updated too.
            main[True] (bool): indicates if the stats should be updated in
                               *M_PATH* too.
        """
        if renew:
            self.update_infos_in_paths(paths)

        for path in paths:
            path = self.M_PATH + path if path[0] != '/' else path
            stats.Stats.write_stats([path], path)

        # Doesn't display the second time the statistics are done (IF they
        # are done a second time obviously)
        if main and self.M_PATH not in paths:
            stats.Stats.write_stats(paths, self.M_PATH, False)

    def update_stories(self, dic: dict):
        """
        Update multiple stories in differents paths or not.

        Args:
            dic (dict): the dictionnary containing the paths as key and the
                        list of stories as value. Example:
                           {
                               '/Users/user/foo': [
                                   'url_1',
                                   'url_2',
                               ],
                               '/Users/user/bar': [
                                   'url_3',
                                   'url_4',
                               ],
                           }

        N.B:
            Also update the stats of the paths and the main path.
        """

        paths = sorted(dic.keys())

        for path in paths:

            tls.chdir(self.M_PATH + path if path[0] != '/' else path)
            urls = dic[path]

            for url in urls:
                m.main(url, True)

        self.update_stats(paths)

    def new_stories(self, dic: dict):
        """
        Download multiple stories in differents paths or not.

        Args:
            dic (dict): the dictionnary containing the paths as key and the
                        list of stories as value. Example:
                           {
                               '/Users/user/foo': [
                                   'url_1',
                                   'url_2',
                               ],
                               '/Users/user/bar': [
                                   'url_3',
                                   'url_4',
                               ],
                           }

        N.B:
            Also update the stats of the paths and the main path.
        """

        paths = sorted(dic.keys())

        for path in paths:

            tls.chdir(self.M_PATH + path if path[0] != '/' else path)
            urls = dic[path]

            for url in urls:
                m.main(url)

        self.update_stats(paths)


def get_help() -> str:
    """
    Returns the help for the shell part of this program, as a `str`.
    """
    return ('Help for program: worker.py\n\n'
            'This program is a shell program designed to use the FFN '
            'DOWNLOADER application.\n\n'
            'Command syntax: python3.6 worker.py [fld] [arg] [...]\n'
            '                                    help\n\n'
            'Arguments:\n'
            '  - fld\n'
            '      The folder in which the program will run. Can be a full '
            'path or a relative one.\n\n'
            '  - arg: can take the following values\n'
            '      ui: updates informations in multiple paths\n'
            '          Syntax for [...]: [path1] [path2] ...\n'
            '      ut: updates statistics in multiple paths\n'
            '          Syntax for [...]: [renew] [main] [path1] [path2] ...\n'
            '      us: updates stories in a single path\n'
            '          Syntax for [...]: [path] [url1] [url2] ...\n'
            '      ns: downloads new stories in a single path\n'
            '          Syntax for [...]: [path] [url1] [url2] ...\n\n'
            '  - help: displays this help\n\n'
            'Example:\n'
            'This will download "https://www.fanfiction.net/s/1/1/Example-Url"'
            ' in "ffn/", which is found in "/":\n\n'
            '  python3.6 worker.py / ns ffn/ https://www.fanfiction.net/s/1/1/'
            'Example-Url\n'
            )


if __name__ == '__main__':

    # To avoid files named 'stats_._{date}.html'
    def clean_path(path: str, fld: str) -> str:
        return fld if path == '.' else path

    def clean_paths(paths: list, fld: str) -> list:
        for i in range(len(paths)):
            paths[i] = clean_path(paths[i], fld)
        return paths

    fld = sys.argv[1]

    if fld == 'help':
        print(get_help())
    else:
        # Intends to test if the path is a full path (Unix or Windows)
        if not(fld[0] == '/' or fld[1] == ':'):
            fld = f'{os.getcwd()}{os.sep}{fld}{os.sep}'

        arg = sys.argv[2]
        oc = OnComputer(fld)

        if arg == 'ui':  # Update informations
            paths = list(sys.argv[3:])
            oc.update_infos_in_paths(clean_paths(paths, fld))
        elif arg == 'ut':  # Update statistics
            renew, main, paths = sys.argv[3], sys.argv[4], list(sys.argv[5:])
            oc.update_stats(clean_paths(paths, fld), renew, main)
        elif arg == 'us':  # Update stories
            path, urls = sys.argv[3], list(sys.argv[4:])
            oc.update_stories({clean_path(path, fld): urls})
        elif arg == 'ns':  # New stories
            path, urls = sys.argv[3], list(sys.argv[4:])
            oc.new_stories({clean_path(path, fld): urls})
        else:
            print(f'[ERROR]: {arg} is not a valid value for *arg*.\n')
            print(get_help())
