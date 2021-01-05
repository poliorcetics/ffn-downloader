__version__ = '2018.07.13'
__author__ = 'Alexis BOURGET'

from datetime import datetime
from logging import DEBUG, INFO, ERROR, CRITICAL

################################################################################
# UI PART

# Constants for the app at large
APP_NAME = 'Multi-sites fanfiction downloader'
MIN_SIZE_X = 1000
MIN_SIZE_Y = 600


# Colors
READ_COLOR = 'DarkOliveGreen1'
UNREAD_COLOR = 'coral1'
SERIES_READ_COLOR = 'olive drab'
SERIES_UNREAD_COLOR = 'tomato3'
SELECTED_COLOR = 'MediumPurple1'


# The available sites
# Each site file shall ensure the site is added to this dictionary in the
# "story_writer.py" file
#
# The values should be tuples containing: (site_class, site_identifier)
#
# - The key is what will be used in the statistics and the ComboBox in the UI
# - The first element of the tuple is the access to the class
# - The second is a identifier used to check if a story belongs to the site.
# It should be unique amongst the handled sites (be aware of both mobile and
# desktop urls if they exist), meaning 'fanfiction' and 'fanfiction.net' cannot
# both be identifiers for different sites since the second risk capturing the
# first each time a check is made
# NOTE: The identifier can be equal to the key but it's not required at all
SITES = {}


# The sorting options available for the selectable part (left panel of the UI)
# The number associated is the one to use to access the value for a story found
# in the database and the format-able string is the one used to show the results
SORT_OPTIONS = {
    'Author': (3, '{story[3]} | {story[4]} ({story[5]:,}) {series}'),
    'Chapter count': (5, '{story[5]:,} | {story[4]} {series}'),
    'Language': (8, '{story[8]} | {story[4]} ({story[5]:,}) {series}'),
    'Read': (12, '{story[4]} ({story[5]:,}) {series}'),
    'Series': (13, '{series} {story[4]} ({story[5]:,})'),
    'Status': (7, '{story[7]} | {story[4]} ({story[5]:,}) {series}'),
    'Title': (4, '{story[4]} ({story[5]:,}) {series}'),
    'Universe': (9, '{story[9]} | {story[4]} ({story[5]:,}) {series}'),
    'Url': (0, '{story[0]} | {story[4]} ({story[5]:,}) {series}'),
    'Word count': (6, '{story[6]:,} | {story[4]} ({story[5]:,}) {series}'),
}


################################################################################
# FILE HANDLING AND LOGGING PART

# The non-site folders that still need to exist
FOLDERS = (
    '0/logs',
    '0/data',
    '0/js',
    '0/css',
)

# Name for the file where the logs will be written
# There is one file per day
# Note that if the date pass while the app is used, the file will not be changed
# since it allows for better reading and continuity in the logs
LOGFILE_NAME = f'0/logs/{datetime(1, 1, 1).today().strftime("%Y%m%d")}.log'

# The level of logging to use for the application
LOG_LEVEL = INFO

# The format for the logs
LOG_FORMAT = (
    '%(asctime)s.%(msecs)03d - %(levelname)s - '
    '%(name)s - %(funcName)s - %(message)s'
)

# The date format for (asctime) in LOG_FORMAT
LOG_DATE_FORMAT = '%H:%M:%S'

# The maximum number of logfiles saved at anytime
MAX_LOG_FILE = 2

################################################################################
# SQL PART

# To create the SQL table used to store all the necessary informations for both
# the statistics and the UI
# 0: url, 1: path_to_index, 2: site, 3: author, 4: title, 5: chapter_count
# 6: word_count, 7: status, 8: language, 9: universe, 10: summary,
# 11: curated_tokens, 12: read, 13: series, 14: position
STORIES_TABLE_CREATION = '''CREATE TABLE stories (\
url TEXT PRIMARY KEY, \
path_to_index TEXT, \
site TEXT, \
author TEXT, \
title TEXT, \
chapter_count INT, \
word_count INT, \
status TEXT, \
language TEXT, \
universe TEXT, \
summary TEXT, \
curated_tokens TEXT, \
read INT, \
series TEXT, \
position INT\
)'''


################################################################################
# CHAPTER PART (HTML + CSS)

# Base for the {previous_link}, {index_link}, {next_link} in the
# CHAPTER_TEMPLATE string below
LINK_BASE = "<a class='{}' href='{}.html'>{}</a>"


# The CSS for each story file and the informations file.
# Do not hesitate to change the max-width to suit your needs
CHAPTER_CSS = '''\
body {
    color: #C0C0C0;
    background-color: #303030;
    text-rendering: optimizeLegibility;
    font-family: -apple-system-font, 'Helvetica', Arial, Verdana, sans-serif;
    -webkit-font-smoothing: subpixel-antialiased;
    margin: 0 auto;
    max-width: 600px;
}
article {
    background-color: #505050;
    box-shadow: 12px 0 6px rgba(0, 0, 0, 0.4), -12px 0 6px rgba(0, 0, 0, 0.4);
    padding: 2%;
    margin: 0;
}
p { padding:0.5%; }
.container { display: flex; }
.container a {
    text-decoration: none;
    text-align: center;
    color: #7abac7;
    padding: 1%;
    display: inline-block;
    transition: 0.2s;
}
.previous, .next {
    background-color: #484848;
    width: 31%; /* +1% padding on each side: final width is 33% */
}
.index {
    background-color: #555555;
    width: 32%; /* +1% padding on each side: final width is 34% */
}
.previous, .index { float: left; }
.next { float: right; }
.container a:hover {
    text-decoration: none;
    color: #68f8ff;
}
.previous:hover, .next:hover { background-color: #303030; }
.index:hover { background-color: #797979; }
'''


# The template for each story file written by this program.
# NOTE: This is a 'format-able' string.
# How to format the {*_link} ?
# The base format is that: <a class='{}' href='{}.html'>{}</a>
#     - with class in [previous, next, index]
#     - when no link exists (first and last chapters), remove the href part:
#       the link should then looks like: <a class='{}'>Nothing more this way</a>
#     - {page_title}, {chapter_title}, {chapter_text} are exactly what they
#       indicate
CHAPTER_TEMPLATE = '''\
<!DOCTYPE html>
<html>

<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta name="viewport" content="initial-scale=1">
    <base>
    <title>{page_title}</title>
    <link rel="stylesheet" href="../../0/css/chapter_style.css">
</head>

<body>

<!-- Hopefully allows the browsers to launch its reader mode if it exists -->
<article class='main content'>

<!-- The links to navigate the story -->
<div class='container'>
{previous_link}
{index_link}
{next_link}
</div>

<hr size=1 noshade/>

<h1 class='title'>{chapter_title}</h1>
<hr size='1' noshade/>

<span class='text'>
{chapter_text}
</span>

<hr size=1 noshade/>

<!-- The links to navigate the story -->
<div class='container'>
{previous_link}
{index_link}
{next_link}
</div>

</article>

</body>
</html>
'''


###############################################################################
# INFORMATIONS PART (HTML + CSS)

# The CSS for each informations file
# Do not hesitate to change the max-width to suit your needs
INFORMATIONS_CSS = '''\
body {
    text-align: justify;
    word-wrap: break-word;
    color: #C0C0C0;
    background-color: #303030;
    text-rendering: optimizeLegibility;
    font-family: -apple-system-font, 'Helvetica', Arial, Verdana, sans-serif;
    -webkit-font-smoothing: subpixel-antialiased;
    margin: 0 auto;
    max-width: 600px;
}
article {
    background-color: #505050;
    box-shadow: 12px 0 6px rgba(0, 0, 0, 0.4), -12px 0 6px rgba(0, 0, 0, 0.4);
    padding: 2%;
    margin: 0;
}
h1 {
    color: #FFFFFF;
    text-align: center;
}
.container { display: flex; }
a {
    text-decoration: none;
    display: inline-block;
    color: #7abac7;
    transition: 0.2s;
}
.infos {
    text-align: center;
    background-color: #454545;
    padding: 1.2%;
    display: inline-block;
    width: 49%;
    transition: 0.2s;
}
.url {
    text-align: center;
    padding: 1.2%;
    width: 97.6%;
    background-color: #454545;
}
.chapter {
    padding: 1.2%;
    width: 97.6%;
}
.infos:hover {
    text-decoration: none;
    background-color: #303030;
}
a:hover, .chapter:hover {
    color: #68f8ff;
    text-decoration: none;
    background-color: #303030;
}
'''


# The template for each informations file written by this program.
# NOTE: This is a 'format-able' string.
# - {story_title}, {story_url}, {universe}, {summary}, {chapter_count}
#   are exactly what their names indicate
# - {author} can be a valid html link to the author's page
# - {writing_date} should be a date formatted like '%H:%M - %d %B %Y'
# - {tokens_formatted} and {table_of_contents} should be html-lists of either
#   the tokens or the chapters (without the <ul> and </ul> markers)
# It is used when writing the informations for a story in the StoryWriter class
# (see utilities/story_writer.py)
INFORMATIONS_TEMPLATE = '''\
<!DOCTYPE html>
<html>

<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta name="viewport" content="initial-scale=1">
    <base>
    <title>{story_title} | Informations</title>
    <link rel="stylesheet" href="../../0/css/informations_style.css">
</head>

<body>

<article>

<div class='container'>
<a class='infos' href="../../{site}_statistics.html">Statistics for {site}</a>
<span class='infos'>{writing_date}</span>
</div>

<hr size=1 noshade/>
<h1>{story_title}</h1>
<hr size=1 noshade/>

<div class='container'>
<span class='infos'>{author}</span>
<span class='infos'>{universe}</span>
</div>

<hr size=1 noshade/>

<a class='url' href='{url}'>{url}</a>

<hr size=1 noshade/>

<p>{summary}</p>

<p><em>{tokens}</em></p>

<hr size=1 noshade/>

<p><strong>Chapters ({chapter_count:,}):</strong></p>

{table_of_contents}

</article>

</body>
</html>
'''


################################################################################
# STATISTICS PART

SITE_STATISTICS_TR_TEMPLATE = '''
<tr>
    <td onclick="sortTable(0)">
        <strong>{story[4]}</strong>
        <a href="{story[1]}">Informations & Index</a>
        <hr size=1 noshade/>
        <a href="{story[0]}">Webpage</a>
        <p><em>(N° {num})</em> {story[10]}</p>
    </td>
    <td onclick="sortTable(1)">{read}</td>
    <td onclick="sortTable(2)">{story[3]}</td>
    <td onclick="sortTable(3)">{story[9]}</td>
    <td onclick="sortTable(4)">{status}</td>
    <td onclick="sortTable(5)">{story[5]:,} chapter(s)</td>
    <td onclick="sortTable(6)">{story[6]:,} words</td>
    <td onclick="sortTable(7)">{story[11]}</td>
    <td onclick="sortTable(8)">{series}</td>
    <!-- The missing 9 is only present when doing the general statistics,
    regardless of the site from which the story was taken -->
</tr>
'''


SITE_STATISTICS_TEMPLATE = '''
<!DOCTYPE html>
<html>

<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta name="viewport" content="initial-scale=1">
    <base>
    <title>Statistics | {site}</title>
    <link rel="stylesheet" href="0/css/statistics_style.css">
</head>
<body>

<script src="0/js/sorting.js"></script>

<div class="general">
    <h1>Statistics | {site}</h1>
    <p>Authors: {authors:,} -  Universes: {universes:,} - Chapters: \
{chapters:,} - Words: {words:,} - Stories: {stories:,} - Read: {read:,} - \
Unread: {unread:,} - Series: {series:,}</p>
</div>
<hr size=1 noshade/>

<table id="stories-table">
<thead>
<tr>
    <th onclick="sortTable(0)">Title</th>
    <th onclick="sortTable(1)">Read</th>
    <th onclick="sortTable(2)">Author</th>
    <th onclick="sortTable(3)">Universe</th>
    <th onclick="sortTable(4)">Status</th>
    <th onclick="sortTable(5)">Chapters</th>
    <th onclick="sortTable(6)">Words</th>
    <th onclick="sortTable(7)">Tokens</th>
    <th onclick="sortTable(8)">Series</th>
    <!-- The missing 9 is only present when doing the general statistics,
    regardless of the site from which the story was taken -->
</tr>
</thead>
<tbody>
{content}
</tbody>
</table>
</body>
</html>
'''


# If the statistics are not properly displayed on your phone/tablet, modify
# the pixel value in this constant
STATISTICS_CSS = '''
/* Generic Styling, for Desktops/Laptops */
body {
    color: #C0C0C0;
    background-color: #505050;
    max-width: 100%;
    text-align: center;
    text-rendering: optimizeLegibility;
    font-family: -apple-system-font, 'Helvetica', Arial, Verdana, sans-serif;
}
.general > p { text-align: center; }
strong {
    padding-bottom: 1.5%;
    display: inline-block;
    color: #FFFFFF;
}
.read, .complete { background-color: #346b35; }
.unread, .progress { background-color: #961010; }
table { border-collapse: collapse; }
th {
    background: #393939;
    font-weight: bold;
}
td, th { border: 1px solid #ccc; }
td {
    text-decoration: none;
    padding-top: 0.5%;
    padding-bottom: 0.5%;
    transition: 0.2s;
}
th:hover {
    text-decoration: none;
    color: #FFFFFF;
    background-color: #191919;
}
td:hover {
    text-decoration: none;
    color: #FFFFFF;
    background-color: #797979;
}
a {
    text-decoration: none;
    color: #7abac7;
    background-color: #454545;
    padding: 1%;
    width: 95%;
    display: inline-block;
    transition: 0.2s
}
a:hover {
    text-decoration: none;
    color: #68f8ff;
    background-color: #393939;
}
p {
    padding-top: -4%;
    text-align: left;
}
/*
Max width before this table gets nasty
This query will take effect for any screen smaller than 760px
THIS VALUE OF 760px (by default) SHOULD BE MODIFIED ACCORDINGLY TO YOUR USAGE
*/
@media only screen and (max-width: 760px) {
    /* Force table to not be like tables anymore */
    table, thead, tbody, th, td, tr {
        display: block;
        width: 100%;
    }
    /* Hide table headers (but not "display: none;" for accessibility) */
    thead tr {
        position: absolute;
        top: -9999px;
        left: -9999px;
    }
    tr { border-bottom: 1px solid #A9A9A9; }
    td {
        /* Behave  like a "row" */
        border: none;
        position: relative;
    }
}
'''


STATISTICS_JS = '''
// Each columns has its asc associated: 1 means ascendant, -1 means descendant.
// The default sort is by title so when clicking on sorting by title,
// the user will expect a reverse sort, meaning it needs to be -1 at first.
var asc = [-1, 1, 1, 1, 1, 1, 1, 1, 1, 1];

function sortTable(n) {

    // The needed variables
    storiesTable = document.getElementById("stories-table");
    storiesTbody = storiesTable.getElementsByTagName("tbody")[0];
    storiesRows = storiesTbody.getElementsByTagName("tr");
    rowsList = new Array();

    tableLength = storiesRows.length

    // Fill the rowsList
    for (i=0; i < tableLength; i++) {
        elements = storiesRows[i].getElementsByTagName("td");
        rowsList[i] = [];
        for (j=0; j < elements.length; j++) {
            rowsList[i][j] = elements[j].innerHTML;
        }
    }

    // Sort (if n=5 or n=6, it's a numerical sort, else it's just a text sort
    if ((n == 5) || (n == 6)) {
        rowsList.sort(function(x, y) {
            // Conversion to numerical values
            a = 1 * x[n].toLowerCase().split(' ')[0].replace(/,/g, '');
            b = 1 * y[n].toLowerCase().split(' ')[0].replace(/,/g, '');
            // Comparison
            if (asc[n] > 0) { return a - b; }
            else { return b - a; }
        });
    } else {
        rowsList.sort(function(x, y) {
            // Getting the relevant values
            a = x[n].toLowerCase();
            b = y[n].toLowerCase();
            // Comparison
            if (asc[n] > 0) {
                if (a == b) { return 0; }
                else if (a < b) { return -1; }
                else { return 1; }
            } else {
                if (a == b) { return 0; }
                else if (a > b) { return -1; }
                else { return 1; }
            }
        });
    }

    // Rebuilding the table
    text = ''
    cellLength = rowsList[0].length;

    for (i=0; i < tableLength; i++) {
        text = '';
        for (j=0; j < cellLength; j++) {
            text += '<td onclick="sortTable(' + j + ')">' + rowsList[i][j];
            text += "</td>";
        }
        rowsList[i] = text;
    }

    // Updating the content
    storiesTbody.innerHTML = "<tr>" + rowsList.join("</tr><tr>") + "</tr>";

    // Updating the sort state for this column
    asc[n] *= -1;

    // Ensuring the memory is cleaned of the now unused variables
    delete storiesTable;
    delete storiesTbody;
    delete storiesRows;
    delete rowsList;
    delete tableLength;
    delete elements;
    delete i;
    delete j;
    delete a;
    delete b;
    delete text;
    delete cellLength;
}
'''
