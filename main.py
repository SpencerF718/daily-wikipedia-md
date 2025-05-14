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

def formatMarkdown(title, headers, link):
    # TODO: implement
    pass

def generateMarkdown(link, saveToVault=False):
    # TODO: implement 
    pass

def main():
    link = getLink()
    print("Random Wikipedia Article:", link)
    generateMarkdown(link)

if __name__ == "__main__":
    main()
