"""
File: stats.py
Author: BOURGET Alexis
License: see LICENSE.txt
App version: 5.0
File version: 2.0

Contains the class 'Stats' which handles the creation of the statistics.
"""

import re
import os
import datetime as dt
import constants as c
import tools as tls


class Stats(object):
    """
    Format and writes statistics.

    Public methods:
        from_path(path: str, display=True) -> str
        from_paths(paths: list, display=True) -> str
        write_stats(paths: list, to='.', display=True)
    """

    @staticmethod
    def _get_intro(counts: tuple) -> str:
        """
        Returns the beginning of a stats file.

        Args:
            counts (tuple): contains the numbers of (in the following order):
                            - stories (int)
                            - chapters (int)
                            - words (int)
                            - universes (int)
                            All these numbers are totals, not those of a
                            particular story.

        Returns:
            The beginning of a stats file, as a `str`.
        """
        date_obj = dt.datetime(1, 1, 1)
        p_date = date_obj.today().strftime('%H:%M - %d %B %Y')

        s_count = tls.display_num(counts[0])
        c_count = tls.display_num(counts[1])
        w_count = tls.display_num(counts[2])
        u_count = tls.display_num(counts[3])

        return (f"{c.STATS_HEADER}\n"
                "<h1>Stats</h1>\n<strong>Informations:</strong>\n<ul>\n<li>"
                f"Last update: {p_date},</li>\n<li>{u_count} universe"
                f"{'s' if counts[3] > 1 else ''},</li>\n<li>{s_count} stories,"
                f"</li>\n<li>{w_count} words,</li>\n<li>{c_count} chapters."
                f"</li>\n</ul>\n\n<br />"
                "<div class='universe' style='font-weight: bold;'>\n"
                "<div class='universe_name'>Universe</div>\n"
                "<div class='universe_count'>Stories</div>\n</div><br />\n"
                )

    @staticmethod
    def _get_uni_div(uni: str, count: int) -> str:
        """
        Returns a universe html div.

        Args:
            uni (str): The universe to place in the div.
            count (int): The number of stories for this universe.

        Returns:
            The completed html div for this universe, as `str`.
        """
        return (f"\n<div class='universe'>\n<div class='universe_name'>• {uni}"
                f"</div>\n<div class='universe_count'>{tls.display_num(count)}"
                f"stor{'ies' if count > 1 else 'y'}</div>\n</div><br />\n"
                )

    @staticmethod
    def _get_stories_intro() -> str:
        """
        Returns the beginning of the stories part of the stats.
        """
        return ("\n<br />\n<div class='story' style='font-weight: bold;'>"
                "<div class='s_title'>Story</div>"
                "<div class='s_words'>Words</div>"
                "<div class='s_chap'>Chapters</div>"
                "<div class='s_ratio'>Ratio W/C</div>\n</div><br />\n"
                )

    @staticmethod
    def _get_story_div(story: dict, link: str) -> str:
        """
        Returns a story html div.

        Args:
            story (dict): The story to place in the div. The keys are:
                          - c_count: Chapters count.
                          - status: 'Complete' or 'In Progress'.
                          - path_infos: Path to the informations.
                          - smry: Summary.
                          - title: Title.
                          - uni: Universe.
                          - url: Url.
                          - w_count: Words count.
                          - ratio: Ration (Words count // Chapters count).
                          - n_id: Numerical ID.
            link (str): Can be 'infos' or 'url', indicates if the url put in
                        the stats links to FFN.net or to the story folder

        Returns:
            The completed html div for this story.

        Raises:
            ValueError(f'{link} is not a valid value for *link*.')
        """
        if link == 'infos':
            url = story['path_infos']
        elif link == 'url':
            url = story['url']
        else:
            raise ValueError(f'{link} is not a valid value for *link*.')

        c_count = tls.display_num(story['c_count'])
        w_count = tls.display_num(story['w_count'])
        ratio = tls.display_num(story['ratio'])

        return (f"\n<div class='story' title='{story['n_id']}'>\n"
                f"<div class='s_title'>• <a href='{url}'>{story['title']}</a>"
                f"<br/>\n<em>{story['uni']} — {story['status']}</em></div>\n"
                f"<div class='s_words'>{w_count} words</div>\n"
                f"<div class='s_chap'>{c_count} chapters</div>\n"
                f"<div class='s_ratio'>~{ratio} w/c</div>\n</div>\n"
                f"<div class='s_summary'>    {story['smry']}</div><br/>\n"
                )

    @staticmethod
    def _get_stats(stories: dict, unvrs: dict, counts: tuple, frm: str) -> str:
        """
        Returns the full stats.

        Args:
            stories (dict): Associates the informations of stories to their url
                            The keys are (for each url):
                            - c_count: Chapters count.
                            - status: 'Complete' or 'In Progress'.
                            - path_infos: Path to the informations.
                            - smry: Summary.
                            - title: Title.
                            - uni: Universe.
                            - url: Url.
                            - w_count: Words count.
                            - ratio: Ration (Words count // Chapters count).
                            - n_id: Numerical ID.
            unvrs (dict): Associates the number of stories for a universe
                          to this universe.
            counts (tuple): contains the numbers of (in the following order):
                            - stories (int)
                            - chapters (int)
                            - words (int)
                            - universes (int)
                            All these numbers are totals, not those of a
                            particular story.
            frm (str): Possibles values are 'folder' and 'list', indicates
                       what type of stats is asked.

        Returns:
            The full stats properly formatted.

        Raises:
            ValueError(f'{frm} is not a valid value for *frm*.')
        """
        if frm == 'folder':
            link = 'infos'
        elif frm == 'list':
            link = 'url'
        else:
            raise ValueError(f'{frm} is not a valid value for *frm*.')

        text = Stats._get_intro(counts)

        for uni in sorted(unvrs.keys()):
            text += Stats._get_uni_div(uni, unvrs[uni])

        text += Stats._get_stories_intro()
        for story in tls.sort_urls(stories.keys()):
            text += Stats._get_story_div(stories[story], link)

        text += '</body>\n</html>'

        return text

    @staticmethod
    def _get_path(path: str, display=True) -> (dict, dict, tuple):
        """
        Returns the components of the stats for a given directory (*path*)

        Args:
            path (str): The path in which the stats will be taken.
            display[True] (bool): Indicates if messages are printed on stdout.

        Returns:
            In the following order:
            - url_ifs (dict): Associate the infos of stories to their url.
                              The keys are (for each url):
                              - c_count: Chapters count.
                              - status: 'Complete' or 'In Progress'.
                              - path_infos: Path to the informations.
                              - smry: Summary.
                              - title: Title.
                              - uni: Universe.
                              - url: Url.
                              - w_count: Words count.
                              - ratio: Ration (Words count // Chapters count).
                              - n_id: Numerical ID.
            universes (dict): Associates the number of stories for a universe
                              to this universe.
            counts (tuple): contains the numbers of (in the following order):
                            - stories (int)
                            - chapters (int)
                            - words (int)
                            - universes (int)
                            All these numbers are the totals for the directory,
                            not those of a particular story.
        """
        tls.chdir(path, display)

        urls = tls.get_urls_from_folder(path)
        s_count = len(urls)

        urls_ifs = dict()
        universes = dict()

        for i in range(s_count):

            url = urls[i]
            t_id = url.split('/')[6]
            n_id = url.split('/')[4]
            raw_infos = f'{t_id}_{n_id}{os.sep}.{n_id}'

            with open(raw_infos, 'r', encoding='utf-8') as f:
                lines = [l.rstrip('\n') for l in f.readlines()]

            urls_ifs[url] = {
                'c_count': int(lines[0]),
                'status': lines[1],
                'path_infos': lines[2],
                'smry': lines[3],
                'title': lines[4],
                'uni': lines[5],
                'url': lines[6],
                'w_count': int(lines[7]),
                'ratio': int(lines[7]) // int(lines[0]),
                'n_id': n_id,
            }

            try:
                universes[lines[5]] += 1
            except KeyError:
                universes[lines[5]] = 1

            if display:
                print(f'REGISTERED -- {lines[4]:60}',
                      f'{str(i + 1).zfill(len(str(s_count)))} / {s_count}')

        counts = (s_count,
                  sum(int(urls_ifs[url]['c_count']) for url in urls_ifs),
                  sum(int(urls_ifs[url]['w_count']) for url in urls_ifs),
                  len(universes))

        return urls_ifs, universes, counts

    @staticmethod
    def from_path(path: str, display=True) -> str:
        """
        Returns the stats for a given directory.

        Args:
            path (str): The path in which the stats will be done.
            display[True] (bool): Indicates if messages are printed on stdout.

        Returns:
            The stats for the given directory, as a `str`.
        """
        urls_ifs, universes, counts = Stats._get_path(path, display)

        return Stats._get_stats(urls_ifs, universes, counts, 'folder')

    @staticmethod
    def from_paths(paths: list, display=True) -> str:
        """
        Returns the stats for a list of directories.

        Args:
            paths (list): The directories to use.
            display[True] (bool): Indicates if messages are printed on stdout.

        Returns:
            The stats for the given directories, as a `str`.

        Raises:
            ValueError("*paths* can't be an empty list.")
        """
        if len(paths) > 1:
            frm = 'list'
        elif len(paths) == 1:
            frm = 'folder'
        else:
            raise ValueError("*paths* can't be an empty list.")

        urls_ifs = dict()
        universes = dict()
        counts = [0, 0, 0, 0]

        for path in paths:
            ifs, uni, cts = Stats._get_path(path, display)
            urls_ifs.update(ifs)  # If a url is present in several directories
                                  # The informations from the last one are
                                  # used
            # Can't use .update() here because we want to add the values, not
            # juste take the last one
            for universe in sorted(uni.keys()):
                try:
                    universes[universe] += uni[universe]
                except KeyError:
                    universes[universe] = uni[universe]
            for i in range(4):
                counts[i] += cts[i]

        return Stats._get_stats(urls_ifs, universes, tuple(counts), frm)

    @staticmethod
    def _del_old_stats_file(path: str):
        """
        Deletes all old stats file in a given directory.

        Args:
            path (str): the path to work with.
        """
        base_path = os.getcwd()
        tls.chdir(path, False)

        for file in os.listdir():
            if re.fullmatch(c.STATS_FILE_REGEX, file) is not None:
                os.remove(file)

        os.chdir(base_path)

    @staticmethod
    def write_stats(paths: list, to='.', display=True):
        """
        Writes the stats for a list of directories.

        Args:
            paths (list): The directories to use.
                          If there is only one, the title of the stats file
                          will be adapted to precise it.
            to['.'] (str): The path in which to write the file.
                           Defaults to current directory.
            display[True] (bool): Indicates if messages are printed on stdout.

        Raises:
            ValueError("*paths* can't be an empty list.")
        """
        date = dt.date.today()
        base_path = os.getcwd()

        if len(paths) > 1:
            file_title = f'stats_{date}.html'
            text = Stats.from_paths(paths, display)
        elif len(paths) == 1:
            path = paths[0]
            i = -2 if path[-1] == os.sep or path[-1] == '.' else -1
            folder = path.split(os.sep)[i]
            file_title = f'stats_{folder}_{date}.html'
            text = Stats.from_path(path, display)
        else:
            raise ValueError("*paths* can't be an empty list.")

        Stats._del_old_stats_file(to)

        os.chdir(to)

        with open(file_title, 'w', encoding='utf-8') as f:
            f.write(text)

        if display:
            print(f'DONE -- {file_title}')

        os.chdir(base_path)

