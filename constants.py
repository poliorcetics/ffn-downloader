# -*- coding : utf-8 -*-

""" -- constants.py

author: Poliorcetics

Contains all the constants used in the second version of the FFN-DOWNLOADER.

 - INTRO
 - ROOT_URL
 - HEADER
"""

INTRO = """ -- FFN-DOWNLOADER --

This program will compile any story coming from https://www.fanfiction.net/ in
multiples html files.

Files created:
 - one .hmtl file per chapter, named as following: [number]. [chapter_title]\
.html
 - one .html file for the full story, named as following: [story_title].html

Each file will get a header to include some CSS and formatting to make it
easier to read. If you're not content with what I choosed, just edit the
default parameters of the constant 'HEADER'."""

ROOT_URL = "https://www.fanfiction.net/"

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
