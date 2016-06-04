# -*- coding : utf-8 -*-

""" -- constants.py

author: Poliorcetics
3rd version of the ffn_downloader.

Contains all the constants needed to make the main3 program works."""

# Get the text ID of the story (.*? matches as few text as possible)
_TEXT_ID_REGEX = r'//www.fanfiction.net/s/\d*/\d/(.*?)" .*>'
# Get the numeric ID of the story
_NUM_ID_REGEX = r'var storyid = (\d*);'
# Get the title
_TITLE_REGEX = r'<b class="xcontrast_txt">\n *(.*)'
# Get the author name
_AUTHOR_REGEX = r'By:\n *</span>\n *<a .*>\n *(.*)'
# Get the summary
_SUMMARY_REGEX = r'<div class="xcontrast_txt" style="margin-top:2px">\n *(.*)'
# Gather the chapters
_CHAPTERS_REGEX = r'<option (selected="" )?value="\d*">\n *(.*)'

# The root url to access to ffn
ROOT_URL = "https://www.fanfiction.net/s/"

# The header of each file downloaded by this program.
HEADER = """<!DOCTYPE html>
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
</head>
<body>
"""
