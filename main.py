import urllib.request
from html.parser import HTMLParser
from datetime import datetime
import os

# Fiddle with these values if you are unable to find an article.
MIN_HEADERS = 10
MAX_RETRIES = 15


def getLink():
    """
    Uses Special:Random Wikipedia page and its subsequent redirect to get and store a random Wikipedia article link.
    """

    randomLink = "https://en.wikipedia.org/wiki/Special:Random"
    req = urllib.request.Request(
        randomLink, headers={'User-Agent': 'Mozilla/5.0'})

    with urllib.request.urlopen(req) as response:
        redirectedLink = response.geturl()

    return redirectedLink


def getHtml(link):
    """
    Retrieves the raw HTML data from a given URL.
    """

    req = urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})

    with urllib.request.urlopen(req) as response:
        htmlContent = response.read().decode('utf-8')

    return htmlContent


def getTitle(htmlContent):
    """
    Extracts the title of the Wikipedia article from its HTML content.
    """

    startIndex = htmlContent.find('<title>') + len('<title>')
    endIndex = htmlContent.find(' - Wikipedia</title>', startIndex)
    title = htmlContent[startIndex:endIndex]

    return title.strip()


def parseHtml(htmlContent):
    """
    Parses the HTML content to extract h2, h3, and h4 headers, excluding a predefined list of non-noteworthy sections.
    """

    parser = WikiHtmlParser()
    parser.feed(htmlContent)

    return parser.headers


class WikiHtmlParser(HTMLParser):
    """
    A custom HTML parser designed to extract header tags (h2, h3, h4) and their text content from Wikipedia articles.
    It filters out a list of common, non-noteworthy sections.
    """

    def __init__(self):
        super().__init__()
        self.headers = []
        self.currentTag = None
        self.currentHeaderText = ""

        self.disallowedHeaders = {
            "contents",
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

    def handle_starttag(self, tag, attrs):
        """
        Processes the start of an HTML tag.
        """

        if tag in ['h2', 'h3', 'h4']:
            self.currentTag = tag
            self.currentHeaderText = ""

    def handle_endtag(self, tag):
        """
        Processes the end of an HTML tag.
        """

        if tag in ['h2', 'h3', 'h4'] and self.currentTag == tag:
            fixedData = self.currentHeaderText.strip().lower()
            if fixedData and fixedData not in self.disallowedHeaders:
                self.headers.append(
                    (self.currentTag, self.currentHeaderText.strip()))
            self.currentTag = None
            self.currentHeaderText = ""

    def handle_data(self, data):
        """
        Processes the character data within an HTML tag.
        """

        if self.currentTag:
            self.currentHeaderText += data


def formatMarkdown(headers, link, title):
    """
    Formats the extracted headers, article link, and title into a Markdown string.
    """

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


def generateMarkdown(link, headers, title, filePath, fileName):
    """
    Writes the formatted Markdown content to a file at the specified path.
    """

    mdContent = formatMarkdown(headers, link, title)

    filePath = os.path.join(filePath, fileName)

    with open(filePath, "w", encoding="utf-8") as file:
        file.write(mdContent)


def main():
    """
    Main function to orchestrate the process of fetching a random Wikipedia article,
    parsing its content, and generating a Markdown file.
    """

    foundSuitableArticle = False
    retries = 0

    link, htmlContent, title, headers = None, None, None, None

    while not foundSuitableArticle and retries < MAX_RETRIES:
        print(
            f"Attempting to fetch article (retry {retries + 1}/{MAX_RETRIES})")
        link = getLink()
        htmlContent = getHtml(link)
        title = getTitle(htmlContent)
        headers = parseHtml(htmlContent)

        if len(headers) >= MIN_HEADERS:
            print(
                f"Found suitable article: '{title}' with {len(headers)} headers.")
            foundSuitableArticle = True
        else:
            print(
                f"Article '{title}' has only {len(headers)} headers. Trying again")
            retries += 1

    if not foundSuitableArticle:
        print(
            f"ERROR: Could not find a suitable article after {MAX_RETRIES} attempts. Try again and/or edit MIN_HEADERS or MAX_RETRIES.")
        return

    datePrefix = datetime.now().strftime("%Y-%m-%d")

    # Change the file path and name here:
    # For the file path, "." will save it directly to this project
    # To save it to your Vault or any other folder, do something like:
    # (C:\Users\Name\OneDrive\Documents\Main\Daily\Wikipedia)
    fileName = f"{datePrefix} Wikipedia Note.md"
    filePath = r"."

    generateMarkdown(link, headers, title, filePath, fileName)


if __name__ == "__main__":
    main()
