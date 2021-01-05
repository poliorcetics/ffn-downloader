__version__ = '2018.06.28'
__author__ = 'Alexis BOURGET'

# Mark the beginning of the informations
INFORMATIONS_BEGINNING = ('<main id="content" role="main" class="px0">'
                          '<table border="1" class="mb3">')

# Mark the end of the informations
INFORMATIONS_END = '</table></main>'

# Get all the informations about the story via a single regex
RE_INFORMATIONS = (
    r"<a class='blue' href='(.*?)'>(.*?)</a> - (.*)\n ?<br />\n ?(\d*) "
    r"words / (Timeline: .*?)<br />\[(.*?) \]<br />([\n-…]+)</td></tr>"
)

# To cut the html by deleting what's before the chapter itself.
CHAP_BEGINNING = (r"<h1 class='center'>.* - .*</h1>"
                  r"<h2 class='center'>Chapter \d+</h2>.*?<div>")

# To cut at the end of the chapter by deleting what comes after it
CHAP_END = r"</div><span class='.*?'><a href='.*?'>"
