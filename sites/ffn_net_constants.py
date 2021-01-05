__version__ = '2018.06.28'
__author__ = 'Alexis BOURGET'

# Constants for the ffn_net.FFN class

# To get the story author.
RE_AUTHOR = r'By:</span> <a .*?>(.*?)</a>'

# To get the author's ID
RE_AUTHOR_ID = r'/u/(\d*)/'

# To get the story universe.
RE_UNIVERSE = r'<title>.*, a(n)? (.*) fanfic \| FanFiction</title>'

# To get the story text-ID.
RE_TEXT_ID = r'href="//www.fanfiction.net/s/\d*/\d*/(.*)">'

# To get the story title.
RE_STORY_TITLE = r'<b class=\'xcontrast_txt\'>(.*)</b>'

# To get the story summary.
RE_SUMMARY = r'<div style=\'margin-top:2px\' class=\'xcontrast_txt\'>(.*)</'

# To get the tokens in their basic form.
RE_TOKENS = r'<span class=\'xgray xcontrast_txt\'>(.*)</span>'

# To delete the tokens html parts.
RE_HTML_FROM_TOKENS = r'<.*?>'

# To get the number of chapters.
RE_CHAPTER_COUNT = r'- Chapters: (.*?) -'

# To get the number of words.
RE_WORD_COUNT = r'- Words: (.*?) -'

# To get the story status.
RE_STATUS = r'- Status: Complete -'

# To get the chapters titles.
RE_CHAPTERS = r'option value=\d* .*?>(.*?)<'

# To cut the html by deleting what's before the chapter itself.
CHAP_BEGINNING = "<div class='storytext xcontrast_txt nocopy' id='storytext'>"

# To cut at the end of the html for a story with multiple chapters.
CHAP_END_MANY = ("</div><div style='height:5px'></div>"
                 "<div style='clear:both;text-align:right;'>")

# To cut at the end of the html for one chapter.
CHAP_END_ONE = "</div><div style='height:5px'></div>\n<script>"
