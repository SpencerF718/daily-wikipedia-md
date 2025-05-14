import urllib.request
from html.parser import HTMLParser
from datetime import datetime

def getLink():
    randomLink = "https://en.wikipedia.org/wiki/Special:Random"
    req = urllib.request.Request(randomLink, headers={'User-Agent': 'Mozilla/5.0'})

    with urllib.request.urlopen(req) as response:
        redirectedLink = response.geturl()
        
    return redirectedLink


def getHTML(link):
    
    req = urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})

    with urllib.request.urlopen(req) as response:
        htmlContent = response.read().decode('utf-8')

    return htmlContent


def getTitle(htmlContent):

    startIndex = htmlContent.find('<title>') + len('<title>')
    endIndex = htmlContent.find(' - Wikipedia</title>', startIndex)
    title = htmlContent[startIndex:endIndex]

    return title.strip()


def parseHTML(htmlContent):

    headers = []

    disallowedHeaders  = {
        "references",
        "external links",
        "see also",
        "further reading",
        "footnotes",
        "notes",
        "citations",
        "bibliography",
        "sources"
    }

    class wikiHTMLParser(HTMLParser):
        def handle_starttag(self, tag, attrs):
            if tag in ['h2', 'h3', 'h4']:
                self.currentTag = tag

        def handle_endtag(self, tag):
            if tag in ['h2', 'h3', 'h4']:
                self.currentTag = None

        def handle_data(self, data):
            if hasattr(self, 'currentTag'):
                fixedData = data.strip().lower()
                if fixedData and fixedData not in disallowedHeaders:
                    headers.append((self.currentTag, data.strip()))

    parser = wikiHTMLParser()
    parser.feed(htmlContent)

    return headers


def formatMarkdown(headers, link, title):

    currentDateTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    initialFormat = (
        f"{currentDateTime}\n"
        "**Related Topics**:\n"
        f"**Link**: {link}\n"
        f"# {title} #wikipedia\n\n"
    )

    bodyFormat = ""

    for tag, title in headers:
        if tag == "h2":
            bodyFormat += f"## {title}\n\n"
        elif tag == "h3":
            bodyFormat += f"### {title}\n\n"
        elif tag == "h4":
            bodyFormat += f"#### {title}\n\n"

    return initialFormat + bodyFormat


def generateMarkdown(link, headers, title, saveToVault):
    
    mdContent = formatMarkdown(headers, link, title)

    fileName = "Wikipedia_note.md"

    with open(fileName, "w", encoding="utf-8") as file:
        file.write(mdContent)


def main():

    link = getLink()
    htmlContent = getHTML(link)
    title = getTitle(htmlContent)
    headers = parseHTML(htmlContent)

    saveToVault = False

    generateMarkdown(link, headers, title, saveToVault)

if __name__ == "__main__":
    main()
