import urllib.request
from html.parser import HTMLParser

def getHTML(link):
    # TODO: implement
    pass

def parseHTML(content):
    # TODO: implement
    pass

def getLink():

    url = "https://en.wikipedia.org/wiki/Special:Random"

    with urllib.request.urlopen(url) as response:
        htmlContent = response.read().decode('utf-8')

    link = parseHTML(htmlContent)
    return link

def generateMarkdown(link, saveToVault=False):
    # TODO: implement
    pass

def main():
    wikiLink = "https://en.wikipedia.org/wiki/Special:Random"
    getLink()
    htmlContent = getHTML(wikiLink)
    headers = parseHTML(htmlContent)
    generateMarkdown(wikiLink)

if __name__ == "__main__":
    main()
