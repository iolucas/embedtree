import requests

from bs4 import BeautifulSoup

import sys

print getPage(sys.argv[1])

def getPage(page, lang="en"):
    """Function to retrieve a wikipedia page in html form, with its sections"""

    # https://en.wikipedia.org/w/api.php?action=parse&redirects&page=fluid_mechanics

    wikipediaApiUrl = "https://" + lang + ".wikipedia.org/w/api.php"

    pageParams = {
        'action': 'parse', 
        'redirects': True,
        'page': page,
        'format': 'json',
        'prop':'text|displaytitle'
    }

    pageData = requests.get(wikipediaApiUrl, pageParams).json()

    if not 'parse' in pageData:
        raise "Error while getting page " + page

    docHtml = BeautifulSoup(pageData['parse']['text']['*'], 'html.parser')

    


    structPageData = {
        'title': pageData['parse']['title'],
        'pageid': pageData['parse']['pageid'],
        'full': docHtml,
        'sections': docSections
    }

    return structPageData