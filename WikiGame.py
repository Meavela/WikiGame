from bs4 import BeautifulSoup
import urllib.request
import re
import string

def ChooseRandomPage():
    req = urllib.request.Request(url="https://fr.wikipedia.org/wiki/Special:Page_au_hasard",
                                headers={'User-Agent': ' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'})
    handler = urllib.request.urlopen(req)
    with handler as response:
        webpage = response.read()
        soup = BeautifulSoup(webpage, 'html.parser')
        for anchor in soup.find_all("h1",{"id":"firstHeading"}):
            result = str(anchor.contents[0])
    
    result = result.replace('<i>','')
    result = result.replace('</i>','')

    return result;

pageDepart = ChooseRandomPage()
pageCible = ChooseRandomPage()
print("----------")
print(pageDepart)
print(pageCible)