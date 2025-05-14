import urllib.request

def getHtml(link):
    #TODO: implement
    pass

def getLink():
    randomLink = "https://en.wikipedia.org/wiki/Special:Random"
    req = urllib.request.Request(randomLink, headers={'User-Agent': 'Mozilla/5.0'})

    with urllib.request.urlopen(req) as response:
        redirectedLink = response.geturl()
        
    return redirectedLink

def formatMarkdown(headers, link):

    initialFormat = (
        "{{date}} {{time}}\n"
        "**Related Topics**:\n"
        f"**Link**: {link}\n"
        "# {{title}} #wikipedia\n\n"
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

def generateMarkdown(link, headers, saveToVault):
    
    mdContent = formatMarkdown(headers, link)

    fileName = "Wikipedia_note.md"

    with open(fileName, "w", encoding="utf-8") as file:
        file.write(mdContent)

def main():
    link = getLink()
    print("Random Wikipedia Article:", link)
    saveToVault = False
    dummyHeaders = [("h2", "testh2"), ("h3", "testh3"), ("h2", "testh2n2")]
    generateMarkdown(link, dummyHeaders, saveToVault)

if __name__ == "__main__":
    main()
