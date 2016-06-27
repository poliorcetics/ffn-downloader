#!/usr/bin/env python3
# -*- coding : utf-8 -*-

""" -- constants.py

author: Poliorcetics

Contains all the constants used in the second version of the FFN-DOWNLOADER.

 - INTRO
 - ASK_URL
 - ROOT_URL
 - HEADER
"""


INTRO = """ -- FFN-DOWNLOADER --

    This program will compile any story coming from https://www.fanfiction.net/
in multiples html files.

Files created:
    - one .hmtl file per chapter, named as following: [number]. [chapter_\
title].html
    - one .html file for the full story, named as following: [story_title].html

    Each file will get a header to include some CSS and formatting to make it
easier to read. If you're not content with what I choosed, just edit the
default parameters of the constant 'HEADER'."""


ASK_URL = """
    Please enter the URL of the first chapter of the wanted story.
The URL should have the following format:
    -> https://www.fanfiction.net/s/[STORY_ID]/1/[NAME]
Like in this:
    -> https://www.fanfiction.net/s/4641394/1/The-Substitute
For the [NAME], replace spaces ' ' by '-' if needed."""


ROOT_URL = "https://www.fanfiction.net"


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
    </style>
</head>
<body>
"""
