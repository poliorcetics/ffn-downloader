"""
File: worker.py
Author: BOURGET Alexis
License: see LICENSE.txt
App version: 5.3.0
File version: 2.3.2

Contains functions which can be used for real-life use of this app.
Can also be used directly in a shell, see 'python3.6 worker.py help' for help.
"""

import os
import re
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
        new_stories(self, dic)

    Public attribute:
        M_PATH (str): Root of the directory tree containing the fanfictions.
    """

    def __init__(self, m_path: str):
        """
        Initializes 'OnComputer'.

        Args:
            m_path (str): The path to the directory tree containing the
                          targeted fanfictions.
        """
        # Ensure the path is properly formatted
        path = re.sub(f'{os.sep}{os.sep}+', f'{os.sep}', m_path)
        if path[-1] == os.sep:
            path = path[:-1]
        self.M_PATH = path

    def _get_full_path(self, path: str) -> str:
        """
        Takes a *path* and returns a full path, using *self.M_PATH*.

        Args:
            path (str): the path to process.
                        If it's a full path, nothing is done, else self.M_PATH
                        is placed at the beginning.
        Returns:
            A full path following the pattern: {self.M_PATH}{os.sep}{path}
        """
        if not(path[0] == '/' or path[1] == ':'):
            path = f'{self.M_PATH}{os.sep}{path}'

        return path

    def update_infos_in_paths(self, paths: list):
        """
        Update the informations of all the stories contained in all the *dirs*.

        Args:
            paths (list): the pathes containing the stories.
        """
        base_dir = os.getcwd()

        for path in paths:
            tls.chdir(self._get_full_path(path))

            urls = tls.get_urls_from_folder(os.getcwd())
            writer = story.StoryWriter()

            for url in urls:
                st = story.Story(url)
                writer.update_infos(st)
                del st

        os.chdir(base_dir)

    def update_stats(self, paths: list, renew=False, main=False):
        """
        Update the stats.html from all *paths* and then in *M_PATH* if asked,
        and only after having renewed the informations for each story in these
        *paths* if *renew* is True.

        Args:
            paths (list): the paths where the stats must be renewed.
            renew[False] (bool): indicates if the informations are to be
                                 updated too.
            main[False] (bool): indicates if the stats should be updated in
                               *M_PATH* too.

        N.B:
            Even if the paths aren't full paths, the M_PATH variable is used to
            complete them.
        """
        if renew:
            self.update_infos_in_paths(paths)

        paths2 = []

        for path in paths:
            path = self._get_full_path(path)
            stats.Stats.write_stats([path], path)
            paths2.append(path)

        # Doesn't display the second time the statistics are done (IF they
        # are done a second time obviously)
        if main:
            stats.Stats.write_stats(paths2, self.M_PATH, False)
            print('\nMAIN STATS: DONE.')

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
            - Even if the path isn't a full path, the M_PATH variable is used
            to complete it.
            - Update the stats of the differents paths, but not the main stats
            because if not all paths were given, those missing will not be
            accounted for.
        """

        paths = sorted(dic.keys())
        updated_stories = {}

        for path in paths:
            tls.chdir(self._get_full_path(path))
            urls = dic[path]

            updated_stories[path] = []

            for url in urls:
                result = m.main(url, True)
                # If the story was in need of an update, its url is saved
                if result == 0:
                    updated_stories[path].append(url)

        self.update_stats(paths, False, False)

        # Print the updated stories, by folder
        for path in updated_stories.keys():
            if updated_stories[path] != []:
                print(f'\n\nStories updated in: {path}\n')
                for url in updated_stories[path]:
                    print(f'     - {url}')

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
            - Even if the path isn't a full path, the M_PATH variable is used
            to complete it.
            - Update the stats of the differents paths, but not the main stats
            because if not all paths were given, those missing will not be
            accounted for.
        """

        paths = sorted(dic.keys())

        for path in paths:
            tls.chdir(self._get_full_path(path))
            urls = dic[path]

            for url in urls:
                m.main(url)

        self.update_stats(paths, False, False)


def get_help() -> str:
    """
    Returns the help for the shell part of this program, as a `str`.
    """
    return ('Help for program: worker.py\n\n'
            'This program is a shell program designed to use the FFN '
            'DOWNLOADER application.\n\n'
            'Command syntax: python3.6 worker.py [fld] [opt] [...]\n'
            '                                    help\n\n'
            'Options:\n'
            '••••••••\n\n'
            '  - [fld]: The folder in which the program will run. Can be a '
            'full path or a relative one.\n\n'
            '  - [opt]: can take the following values\n\n'
            '    ui: updates informations in multiple paths\n'
            '        Syntax for [...]: [path1] [path2] ...\n\n'
            '    ut: updates statistics in multiple paths\n'
            '        Syntax for [...]: [renew] [path1] [path2] ...\n\n'
            '    us: updates stories in a single path\n'
            '        Syntax for [...]: [path] [url1/id1] [url2/id2] ...\n\n'
            '    ns: downloads new stories in a single path\n'
            '        Syntax for [...]: [path] [url1/id1] [url2/id2] ...\n\n'
            '  - help: displays this help\n\n'
            'Note:\n'
            '•••••\n\n'
            '- It is possible to use either URLs or IDs to identify stories. '
            'It is also possible to mix the two type of identification without'
            ' a problem.\n'
            '- The main stats file will never be updated if you have one. That'
            ' is because it can not find all story folders so to avoid errors '
            'in counting them you will have to do it yourself separately if '
            'you wish to update it.\n\n'
            'Example:\n'
            '••••••••\n\n'
            '(This examples assume you are in the correct directory to '
            'directly access worker.py)\n\n'
            'This will download "https://www.fanfiction.net/s/1/1/Example-Url"'
            ' in "ffn/", which is found in "/":\n\n'
            '  python3.6 worker.py / ns ffn/ https://www.fanfiction.net/s/1/1/'
            'Example-Url\n\n'
            'This command will accomplish exactly the same task:\n\n'
            '  python3.6 worker.py / ns ffn/ 1\n\n'
            )


if __name__ == '__main__':

    # Two function to avoid files named 'stats_._{date}.html'
    def clean_path(path: str, fld: str) -> str:
        return fld if path == '.' else path

    def clean_paths(paths: list, fld: str) -> list:
        for i in range(len(paths)):
            paths[i] = clean_path(paths[i], fld)
        return paths

    # A function to ensure IDs and URLs are correclty handled
    def setup_urls(args: tuple) -> list:
        urls = list()
        for arg in args:
            urls.append(arg if tls.is_url(arg) else tls.id_to_url(arg))
        return urls

    fld = sys.argv[1]

    if fld == 'help':
        print(get_help())
    else:
        # Intends to test if the path is a full path (Unix or Windows)
        if not(fld[0] == '/' or fld[1] == ':'):
            fld = f'{os.getcwd()}{os.sep}{fld}{os.sep}'

        opt = sys.argv[2]
        oc = OnComputer(fld)
        urls = list()

        if opt == 'ui':  # Update informations
            paths = list(sys.argv[3:])
            oc.update_infos_in_paths(clean_paths(paths, fld))

        elif opt == 'ut':  # Update statistics
            renew, paths = sys.argv[3], list(sys.argv[4:])
            oc.update_stats(clean_paths(paths, fld), renew, False)

        elif opt == 'us':  # Update stories
            path, args = sys.argv[3], tuple(sys.argv[4:])
            oc.update_stories({clean_path(path, fld): setup_urls(args)})

        elif opt == 'ns':  # New stories
            path, args = sys.argv[3], tuple(sys.argv[4:])
            oc.new_stories({clean_path(path, fld): setup_urls(args)})

        else:
            print(f'[ERROR]: {opt} is not a valid value for *opt*.\n')
            print(get_help())
