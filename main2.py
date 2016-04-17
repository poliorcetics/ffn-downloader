# -*- coding : utf-8 -*-

""" -- main2.py

author: Poliorcetics

Version 2 of the FFN-DOWNLOADER.

Contains all the functions needed to handle download and file management of the
story.
"""

from urllib import request as rq
import re
import os
import constants as c


def get_story_infos(url: str) -> (int, int, str):
    """Gather the basics infos about the story to use them later."""

    url = url.split('/')

    story_id = url[-3]
    chapter = url[-2]
    story_title = url[-1]

    return int(story_id), int(chapter), story_title


def delete_external_parts(page: str, story_id: int,
                          chap: int, story_title: str) -> (str):
    """Delete the useless external parts contained in the html. There are
after the process still useless parts in the middle, between the chapters and
story but they'll used to get the chapters so they're not deleted now."""

    to_part = """<SELECT id=chap_select title="Chapter Navigation" Name=\
chapter onChange="self.location = '/s/%s/'+ this.options[this.selectedIndex].\
value + '/%s';">""" % (story_id, story_title)

    page = page.partition(to_part)[2]

    if chap == 1:
        to_part = """</div></div><div style='height:5px'></div><div style='\
clear:both;text-align:right;'> """ + to_part
    else:
        to_part = """</div></div><div style='height:5px'></div><div style='cle\
ar:both;text-align:right;'><button class=btn TYPE=BUTTON  onClick="self.locati\
on='/s/%s/%s/%s'">&lt; Prev""" % (story_id, chap - 1, story_title)

    page = page.partition(to_part)[0]

    return page


def format_chapters(chapters: list) -> (list):
    """Format the chapters to insert 0s when needed"""

    # Get the number of chapters
    chap_nb = len(chapters)
    # To find the numero of the chapter
    chap_num_regex = re.compile(r'\d*. ')

    for chapter in chapters:
        # Find the numero of the chapter and delete the non-digit part
        chap_num = chap_num_regex.findall(chapter)[0]
        chap_num = chap_num.replace('. ', '')

        # Insert 0s if needed
        if len(chap_num) < len(str(chap_nb)):
            chapters[int(chap_num) - 1] = "0" * (len(str(chap_nb)) -
                                                 len(chap_num)) + chapter

    return chapters


def format_story(story_html: str) -> (str):
    """Format the story by replacing elements by they wanted counterpart."""

    # Elements which need to be replaced
    to_replace = {
        '<p': '\n<p',
        'align=center': '',
        '0.5em': '0',
    }

    for key, value in to_replace.items():
        story_html = story_html.replace(key, value)

    return story_html


def insert_title(story_html: str, chapters: list, chapter: int) -> (str):

    return '\n<br />\n<br />\n<br />\n<hr size=1 noshade>\n<h1>%s</h1>\n%s\n' \
        % (chapters[chapter - 1], story_html)


def insert_header(full_story_html: str) -> (str):

    return c.HEADER + full_story_html + '</body>\n</html>'


def get_list_of_chapters(chapters_html: str) -> (list):
    """Gather a list of the chapters of the story and format them.
The entry must be only the html part containing the chapters, else you'll
have problems."""

    # Get only the meaningful content
    chapters_html = chapters_html.partition('</select>')[0]
    # Prepare the deletion of the useless parts
    chapter_regex = re.compile(r'(<option  value=\d* (?:selected)?>)')

    # Get the useless parts and replace them by '\n'
    for sep in chapter_regex.findall(chapters_html):
        chapters_html = chapters_html.replace(sep, '\n')

    # Get a list of the chapters and delete the first element of the list
    # because it will always be empty
    chapters = chapters_html.split('\n')
    del chapters[0]

    return format_chapters(chapters)


def get_chapters_and_story(page: str, story_id: int,
                           chap: int, story_title: str) -> (list, str):
    """Gather a list of the chapters and the story itself in the given page."""

    # A little formatting to ease the process.
    page = page.replace('\n', '')

    # Delete the useless external parts
    page = delete_external_parts(page, story_id, chap, story_title)

    # Get the chapters in html form and sort them into a list
    chapters = get_list_of_chapters(page.partition("</script>")[0])

    # Get the story in html form
    story = page.partition("</script>")[2] + '</div></div>'

    return chapters, story


def main(url=None) -> (bool):
    """Main function, do the real work.

 Parameter
- url=None          - str - the url to use if you don't want to type it or use
                            the function into another program.

 Return
- True              - No error,
- False             - There was an unexpected error, please file a bug report.
"""

    if not (url is None):
        print(c.INTRO)

        # Get the url of the first chapter
        print(c.ASK_URL)
        try:
            url = input('> ')
        except Exception as e:
            print('\nThere was an error:\n%s' % e)
            return False

    # Gather the useful informations about the story.
    story_id, chapter, story_title = get_story_infos(url)

    # Open and read the first page
    first_page = rq.urlopen(url)
    first_page = first_page.read().decode('utf-8')

    # Gather the chapters
    chapters = get_chapters_and_story(first_page, story_id,
                                      chapter, story_title)[0]

    full_story = ""

    # Display the current directory and create a new one to save the story
    print('\nCurrent working directory: %s\n' % os.getcwd())
    try:
        os.mkdir("%s_%s" % (story_id, story_title))
    except:
        os.system('rm -rf %s' % story_title)
        os.mkdir(story_title)

    for chap_num in range(1, len(chapters) + 1):

        url = "%s/s/%s/%s/%s" % (c.ROOT_URL, story_id, chap_num, story_title)

        # Open and read the current page
        page = rq.urlopen(url)
        page = page.read().decode('utf-8')

        # Get the story of the current page
        story = get_chapters_and_story(page, story_id,
                                       chap_num, story_title)[1]

        # Insert the title
        story = insert_title(story, chapters, chap_num)

        # Write the chapter
        chapter_file = open('%s%s%s.html' % (story_title, os.sep,
                                             chapters[chap_num - 1]),
                            'w', encoding='utf-8')
        chapter_file.write(insert_header(format_story(story)))
        chapter_file.close()

        print('DONE -- %s.html' % chapters[chap_num - 1])

        # Add the chapter to the full story
        full_story += story

    # Open the file used to gather the full story and write it
    full_file = open('%s_%s%s%s.html' % (story_id, story_title,
                                         os.sep, story_title),
                     'w', encoding='utf-8')
    full_file.write(insert_header(format_story(full_story)))
    full_file.close()

    print('DONE -- %s.html' % story_title)

    return True


if __name__ == '__main__':
    main()
