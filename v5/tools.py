"""
File: func_tools.py
Author: BOURGET Alexis
License: see LICENSE.txt
App version: 5.3.1
File version: 2.5

Contains some functions needed to make the app works.
"""

import urllib.request
import urllib.error
import urllib.parse
import socket
import re
import os
import constants as c
import story as st


def chdir(path: str, display=True):
    """
    Tries to set the working directory to *path*.

    Args:
        path (str): the path to use.
        display[True] (bool): specify if messages are displayed on stdout.

    Raises:
        FileNotFoundError
    """
    os.chdir(path)

    if display:
        folder = os.getcwd().split(os.sep)[-1]
        print(f'\n---- FOLDER: {folder} ----\n')


def is_url(url: str) -> bool:
    """
    Checks if a *url* appears to be a valid FFN url.

    Args:
        url (str): the url to check.

    Returns:
        True if the url is correct (in appearance) else False.
    """
    if re.match(c.MOBILE_URL_REGEX, url) is not None:
        url = url.replace('://m', '://www')

    return re.match(c.CORRECT_URL_REGEX, url) is not None


def id_to_url(id_: str) -> str:
    """
    Gets an ID *id_* as a `str` and returns the corresponding url, as a `str`.

    Args:
        id_ (str): the id to use in the url returned

    Returns:
        A valid fanfiction.net url based on the given id, as a `string`.
    """

    return f'{c.ROOT_URL}{id_}/1/'


def get_page(url: str, display=True, max_tries=5) -> str:
    """
    Takes an *url* and returns the associated HTML page as a `str`.

    Args:
        url (str): the url to use
        display[True] (bool): specify if error messages are displayed or not.
        max_tries[5] (int): the maximum number of tries to get the url.

    Returns:
        A `str` where all multiples spaces have been corrected.
        (See constants.py *WRONG_SPACES_REGEX* for more informations)

    Raises:
        urllib.error.HTTPError
        Exception('Error not encountered yet.')
    """
    for _ in range(max_tries):
        try:
            page = urllib.request.urlopen(url, timeout=5)
        # Just caught to be able to display the error and be sure not to try
        # several times
        except urllib.error.HTTPError as err:
            if display:
                print(f'[ERROR]: {err}')
            raise err
        except urllib.error.URLError as err:
            if display:
                print(f'[ERROR]: URLError: {err}')
        except socket.timeout as err:
            if display:
                print(f'[ERROR]: TimeoutError: {err}')
        except Exception as err:
            if display:
                print(f'[ERROR] not dealt with: {type(err)}: {err}')
            continue
        # In case everything has gone well until now
        else:
            html = page.read().decode('utf-8')
            return re.sub(c.WRONG_SPACES_REGEX, ' ', html)
    else:
        raise Exception('Error not encountered yet.')


def display_num(num: float) -> (str):
    """
    Takes a `float` *num* and displays it properly.

    Args:
        num (float): the number to display.

    Returns:
        A string with the number formatted.
        If the number can be made an `int`, it is done.

    Example:
        >>> display_num(100000.1)
        '100 000.1'
    """

    num = int(num) if int(num) == num else num

    return f'{num:,}'.replace(',', ' ')


def get_urls_from_folder(path: str) -> list:
    """
    Takes a *path* and returns a list of the urls found in it.

    Args:
        path (str): the path to process.

    Returns:
        An alphabetically sorted `list` containing all the urls found.
        (See function )

    Raises:
        FileNotFoundError
    """

    folders = os.listdir(path)
    urls = list()
    path += os.sep if path[-1] != os.sep else ''

    for f in sorted(folders):
        is_dir = os.path.isdir(path + f)
        is_valid_story_dir = re.fullmatch(c.FOLDER_REGEX, f) is not None
        if is_dir and is_valid_story_dir:
            name, story_id = f.rsplit('_', 1)
            urls.append(f'{c.ROOT_URL}{story_id}/1/{name}')

    return sort_urls(urls)


def sort_urls(urls: list) -> (list):
    """
    Sorts the given *urls* by name. Assumes

    Args:
        urls (list): the list of urls to sort.

    Returns:
        A `list` of the urls sorted alphabetically by name (if two names are
        the same, they are then sorted by id)

    Example:
        >>> sort_urls(["https://www.fanfiction.net/s/10851640/1/2nd-Generation",
                       "https://www.fanfiction.net/s/3468944/1/100-Moments-to-Live-For",
                       "https://www.fanfiction.net/s/3401052/1/A-Black-Comedy"]
                      )
        ["https://www.fanfiction.net/s/3468944/1/100-Moments-to-Live-For",
         "https://www.fanfiction.net/s/10851640/1/2nd-Generation",
         "https://www.fanfiction.net/s/3401052/1/A-Black-Comedy",]
    """

    dic = dict()

    for url in urls:
        url_split = url.split('/')
        num_id = url_split[4]
        if url_split[6]:
            text_id = url_split[6]
        else:
            st = st.Story(url)
            text_id = st.ifs['t_id']
            del st

        dic[f'{text_id}_{num_id}'] = f'{c.ROOT_URL}{num_id}/1/{text_id}'

    return list(dic[key] for key in sorted(dic.keys()))


def clean(text: str) -> str:
    """
    Handles non-ascii characters (for Story.ifs['t_id'] for example).

    Args:
        text (str): the text to translate

    Returns:
        A `str`: the text transformed.

    Example:
    >>> clean('Shengc%C3%BAn')
    Shengcun
    """

    in_char = 'àäâáãåāéèëêęėēìïîíįīòöôóøōúùüûūÿñç'
    out_char = 'aaaaaaaeeeeeeeiiiiiioooooouuuuuync'

    trans = str.maketrans(in_char + in_char.upper(),
                          out_char + out_char.upper())
    return urllib.parse.unquote(text, errors='strict').translate(trans)
