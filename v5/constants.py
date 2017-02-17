"""
File: constants.py
Author: BOURGET Alexis
License: see LICENSE.txt
App version: 5.0.1
File version: 4.0

Contains all the constants needed to make this app works.
"""

###############################################################################
# Following are the constants used to get infos from a fanfiction.net page

# To check if the url does represent a fanfiction.
CORRECT_URL_REGEX = r'https://www.fanfiction.net/s/\d*/\d*/(.*)?'

# To get the story author.
AUTHOR_REGEX = r'By:</span> <a .*?>(.*?)</a>'

# To get the story universe.
UNIVERSE_REGEX = r'<title>.*, a(n)? (.*) fanfic \| FanFiction</title>'

# To get the story text-ID.
TEXT_ID_REGEX = r'href="//www.fanfiction.net/s/\d*/\d*/(.*)">'

# To get the story title.
STORY_TITLE_REGEX = r'<b class=\'xcontrast_txt\'>(.*)</b>'

# To get the story summary.
SUMMARY_REGEX = r'<div style=\'margin-top:2px\' class=\'xcontrast_txt\'>(.*)</'

# To get the tokens in their basic form.
TOKENS_REGEX = r'<span class=\'xgray xcontrast_txt\'>(.*)</span>'

# To delete the tokens html parts.
HTML_FROM_TOKENS_REGEX = r'<.*?>'

# To get the number of chapters.
CHAPTERS_COUNT_REGEX = r'- Chapters: (.*?) -'

# To get the number of words.
WORDS_COUNT_REGEX = r'- Words: (.*?) -'

# To get the date of the last update.
UPDATED_REGEX = r'- (Updated: .*?) -'

# To get the date of the first post.
PUBLISHED_REGEX = r'- (Published: .*?) -'

# To get the story status.
STATUS_REGEX = r'- Status: Complete -'

# To delete multiple spaces.
WRONG_SPACES_REGEX = r' {2,}'

# To cut the html by deleting what's before the chapter itself.
BEGINNING = "<div class='storytext xcontrast_txt nocopy' id='storytext'>"

# To get the chapters titles.
CHAPTERS_REGEX = r'option value=\d* .*?>(.*?)<'

# To cut at the end of the html for a story with multiple chapters.
END_MANY = "</div><div style='height:5px'></div><div style='clear:both;text-align:right;'>"

# To cut at the end of the html for one chapter.
END_ONE = "</div><div style='height:5px'></div>\n<script>"

###############################################################################
# Following are the constants used to process the files created by this app

# To ensure a file is named as a chapter.
CHAPTER_FILE_REGEX = r'(\d*).html'

# To ensure a file is named as a stats file.
STATS_FILE_REGEX = r'(stats_.*\d*-.*?-\d*.html)'

# To ensure a folder is named as a story folder.
FOLDER_REGEX = r'.*_\d*'

# To get the table of contents from one of my file
TOC_REGEX = r'(<br />\n<strong>Table of contents:</strong><br />\n<ul>(<li>.*</li>\n *)* *</ul>)'

# To get the 'previous' link
PREVIOUS_REGEX = r'<a href=\'\d*.html\'>Previous \(\d*/(\d*)\)</a> <em>.*</em>'

# to get the 'next' link
NEXT_REGEX = r'<a href=\'\d*.html\'>Next \(\d*/(\d*)\)</a> <em>.*</em>'

###############################################################################
# Following are some html headers

# The header of each story file written by this program.
STORY_HEADER = """<!DOCTYPE html>
 <html>
 <head>
    <meta charset="utf-8" />
    <style>
        * {
            font-family: "Helvetica";
            font-size: 15px;
            text-align: justify;
        }
        body {
            min-width: 25em;
            max-width: 30em;
        }
        h1 {
            font-size: 26px;
            text-align: left;
        }

        a {
            text-color: blue;
            font-size: 20px;
        }
    </style>
 </head><body>\n"""

STATS_HEADER = """<!DOCTYPE html>
 <html>
 <head>
    <meta charset="utf-8" />
    <style>
        * {
            font-family: "Helvetica";
            font-size: 20px;
            text-align: left;
        }
        h1 { font-size: 26px; }
        a { text-color: blue; }
        div { padding: 0px; }
        .story, .universe {
            width: 100%;
            display: flex;
            flex-wrap: nowrap;
        }
        .universe_name { width: 80%; }
        .universe_count { width: 20%; text-align: center; }
        .s_title {
            width: 50%;
            word-wrap: break-word;
        }
        .s_words, .s_chap, .s_ratio { text-align: center; }
        .s_words { width: 17%; }
        .s_chap { width: 15%; }
        .s_ratio { width: 18%; }
        .s_summary {
            width: 100%;
            word-wrap: break-word;
            font-style: italic;
        }
        em { font-size: 16px; }
    </style>
 </head><body>\n"""

###############################################################################
# Miscellaneous

# The root url to access to fanfiction.net.
ROOT_URL = "https://www.fanfiction.net/s/"
