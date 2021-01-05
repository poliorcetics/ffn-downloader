__version__ = '2018.06.30'
__author__ = 'Alexis BOURGET'

import re
import logging
import urllib.request
import urllib.parse
import tkinter as tk
import tkinter.filedialog as fd

import utilities.constants as cst


def setup_logging(name: str, start_application=False) -> logging.Logger:

    logger = logging.getLogger('')
    if start_application:
        # Create the logger
        logger.setLevel(cst.LOG_LEVEL)
        # Create a file handler
        fh = logging.FileHandler(cst.LOGFILE_NAME)
        fh.setLevel(cst.LOG_LEVEL)
        # Create a console handler
        ch = logging.StreamHandler()
        ch.setLevel(cst.LOG_LEVEL)
        # Create formatter and add it to the handler
        formatter = logging.Formatter(fmt=cst.LOG_FORMAT,
                                      datefmt=cst.LOG_DATE_FORMAT)
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        logger.addHandler(fh)
        logger.addHandler(ch)

    return logger.getChild(name)


def popup_settings(base: tk.Tk or tk.Frame) -> str:
    """
    Opens a pop-up to ask where the stories are supposed to be saved

    :param base: the parent frame for the popup
    :return: the folder
    """
    base.update()
    folder = fd.askdirectory(parent=base,
                             initialdir='/',
                             title='Choose a folder for your stories.')
    base.update()
    return folder


def get_settings() -> list:
    """
    Get the settings
    """
    with open('settings.ffndl', 'r', encoding='utf-8') as f:
        return [line.replace('\n', '') for line in f.readlines()]


def get_page(url: str) -> str:
    """
    Takes an *url* and returns the associated HTML page as a `str`.

    :param url:  the full url to use
    :return: the html page encoded in 'utf-8'
    """
    _logger = setup_logging('tools')
    _logger.info(f'Getting page: "{url}"')
    with urllib.request.urlopen(url, timeout=5) as page:
        # The .replace is for a space that isn't a space
        text = page.read().decode('utf-8').replace(' ', ' ')
        text = re.sub(r' {2,}', ' ', text)
        _logger.debug('Page downloaded')
        # Eliminate double (or more) spaces since it's not conducive to an
        # enjoyable reading experience
        return text


def clean(text: str) -> str:
    """
    Handles non-ascii characters

    :param text: the number to display
    :return: the number displayed

    Example:
    >>> clean('Shengc%C3%BAn')
    Shengcun
    """
    _logger = setup_logging('tools')
    _logger.debug(f'Cleaning text: "{text}"')

    in_char = 'àäâáãåāéèëêęėēìïîíįīòöôóøōúùüûūÿñç'
    out_char = 'aaaaaaaeeeeeeeiiiiiioooooouuuuuync'

    trans = str.maketrans(in_char + in_char.upper(),
                          out_char + out_char.upper())
    text = urllib.parse.unquote(text, errors='strict').translate(trans)
    _logger.debug('Text cleaned')
    return text
