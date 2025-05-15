import urllib.request
from html.parser import HTMLParser
from datetime import datetime
import os


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


def getHTML(link):
    """
    Retrieves the raw HTML data. 

    Parameters:
        link (str): Link to the random Wikipedia article.

    Returns:
        str: The raw HTML data
    """

    req = urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})

    with urllib.request.urlopen(req) as response:
        htmlContent = response.read().decode('utf-8')

    return htmlContent


def getTitle(htmlContent):
    """
    Retrieves the title of the Wikipedia article.

    Parameters: 
        htmlContent (str): The raw HTML data

    Returns:
        str: The Random Wikipedia article title
    """

    startIndex = htmlContent.find('<title>') + len('<title>')
    endIndex = htmlContent.find(' - Wikipedia</title>', startIndex)
    title = htmlContent[startIndex:endIndex]

    return title.strip()


def parseHTML(htmlContent):
    """
    Parses 3 levels of headers, excluding non-noteworthy sections.

    Parameters:
        htmlContent (str): The raw HTML data

    Returns:
        list: A list of tag and text pairs for each header.
    """

    headers = []

    disallowedHeaders = {
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
    """
    Formats headers, title, and link into string to be inserted into the markdown.

    Parameters:
        headers (list): A list of tag and text pairs for each header
        link (str): The link to the random Wikipedia article
        title (str): The title of the Wikipedia article

    Returns:
        str: A string formatted for markdown files
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
    Writes the markdown string into a file at a specified location.

    Parameters:
        link (str): The link to the random Wikipedia article
        headers (list): List of headers from the Wikipedia article
        title (str): Title of the article
        filePath (str): The folder path where the .md file will be saved at
        fileName (str): The name of the .md file that will be created
    """

    mdContent = formatMarkdown(headers, link, title)

    filePath = os.path.join(filePath, fileName)

    with open(filePath, "w", encoding="utf-8") as file:
        file.write(mdContent)


def main():
    """
    Main function. Calls previous functions and included file name and path for easy editability.
    """

    link = getLink()
    htmlContent = getHTML(link)
    title = getTitle(htmlContent)
    headers = parseHTML(htmlContent)

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
