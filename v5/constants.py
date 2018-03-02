"""
File: constants.py
Author: BOURGET Alexis
License: see LICENSE.txt
App version: 5.3.0
File version: 4.1.0

Contains all the constants needed to make this app works.
"""

###############################################################################
# Following are the constants used to get infos from a fanfiction.net page

# To check if the url does represent a fanfiction.
CORRECT_URL_REGEX = r'https://www.fanfiction.net/s/\d*/\d*/(.*)?'

# To check if the url is a 'mobile' one
MOBILE_URL_REGEX = r'https://m.fanfiction.net/s/\d*/\d*/(.*)?'

# To get the story author.
AUTHOR_REGEX = r'By:</span> <a .*?>(.*?)</a>'

# To get the author's ID
AUTHOR_ID_REGEX = r'/u/(\d*)/'

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
# Following are some css stylesheet and html headers

# The CSS for each story file and the infos file.
STORY_CSS = """\
*, body {
    border: 0;
    margin: 0;
    padding: 0;
    font-size: 1.0em;
    font-family : 'Helvetica', Arial, Verdana, sans-serif;
    text-rendering: optimizeLegibility;
    -webkit-text-size-adjust: none;
    line-height: normal;
    word-wrap: break-word;
    background-color: #dfdfdf;
    text-align: justify;
    min-width: 25em;
    max-width: 30em;
}
strong { font-weight: bold }
em { font-style: italic }
h1 {
    font-size: 1.5em;
    text-align: left;
}
a {
    color: #005b96;
    font-size: 1.25em;
}
.content {
    margin: 0.2em 0.5em 0.8em 0.5em;
    padding:0 0.5em 0 0.5em;
}
"""

# The header of each story file and infos file written by this program.
# NOTE: This is a 'format-able' string.
STORY_HEADER = """<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8" />
    <title>{ttl}</title>
    <link rel="stylesheet" href="style.css">
</head>

<body>
<div role='main' class='content' id='storytext' align=center>
"""

STATS_HEADER = """<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8" />
    <style>
        * {
            font-family : 'Helvetica', Arial, Verdana, sans-serif;
            font-size: 1.0em;
            text-align: left;
            background-color: #dfdfdf;
        }
        h1 { font-size: 1.5em; }
        a { color: #005b96; }
        div { padding: 0; }
        em { font-size: 0.95em; }
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
        .inprogress { color: #bf0000; font-size: 0.95em; }
        .complete { color: #008000; font-size: 0.95em; }
        .uni_clr { color:#660066; font-size: 0.95em; }
        .counts_clr { color:#009688; }
    </style>
</head>

<body>
"""

###############################################################################
# Miscellaneous

# The root url to access to fanfiction.net stories.
ROOT_URL = "https://www.fanfiction.net/s/"

# The root url to access to fanfiction.net authors.
AUTH_URL = "https://www.fanfiction.net/u/"
