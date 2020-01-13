# coding=utf-8
from bs4 import BeautifulSoup
import urllib.request
import re
import string

def ChooseRandomPage():
    req = urllib.request.Request(url="https://fr.wikipedia.org/wiki/Special:Page_au_hasard",
                                headers={'User-Agent': ' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'})
    handler = urllib.request.urlopen(req)
    with handler as response:
        webpage = response.read().decode('utf-8','ignore')
        soup = BeautifulSoup(webpage, 'html.parser')
        for anchor in soup.find_all("h1",{"id":"firstHeading"}):
            result = str(anchor.contents[0])
    
    result = result.replace('<i>','')
    result = result.replace('</i>','')

    return result

def GetUrl(pageActuelle):
    req = urllib.request.Request(url="https://fr.wikipedia.org/wiki/"+pageActuelle,
                                headers={'User-Agent': ' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'})
    handler = urllib.request.urlopen(req)
    with handler as response:
        webpage = response.read().decode('utf-8','ignore')
        soup = BeautifulSoup(webpage, 'html.parser')
        soup = Decompose(soup)
        my_list = FindAllLinks(soup)

    return my_list

def Decompose(soup):
    for anchor in soup.find_all("table",{"class":"infobox"}):
        anchor.decompose()
    for anchor in soup.find_all("table",{"class":"infobox_v2"}):
        anchor.decompose()
    for anchor in soup.find_all("table",{"class":"infobox_v3"}):
        anchor.decompose()
    for anchor in soup.find_all("div",{"id":"toc"}):
        anchor.decompose()
    for anchor in soup.find_all("div",{"id":"mw-navigation"}):
        anchor.decompose()
    for anchor in soup.find_all("div",{"id":"mw-page-base"}):
        anchor.decompose()
    for anchor in soup.find_all("div",{"id":"mw-head-base"}):
        anchor.decompose()
    
    return soup

def FindAllLinks(soup):
    my_list = []

    for anchor in soup.find_all("a"):
        if 'href="/wiki/' in str(anchor):
            x = re.search("^.{15,50}[:]", str(anchor))
            if x == None:
                y = re.search("^.{15,100}[#]", str(anchor))
                if y == None:
                    if anchor.contents:
                        element = anchor.contents[0]
                        if element not in my_list:
                            my_list.append(element)
    
    return my_list

pageDepart = ChooseRandomPage()
pageCible = ChooseRandomPage()
pageActuelle = pageDepart.replace(' ','_')
isFind = False
tour = 0
while isFind == False:
    tour += 1
    page = 1
    choice = None
    print("********** WikiGame ********** Tour n°{}".format(tour))
    print("Départ : "+pageDepart)
    print("Cible : "+pageCible)
    print("Actuellement : "+pageActuelle)
    myList = GetUrl(pageActuelle)
    while choice == 0 or choice == 99 or choice == None: 
        if len(myList) < 20:
            mini = 0
            maxi = len(myList)
        else:
            mini = (page-1)*20
            maxi = page*20

        for i in range(mini,maxi):
            number = i+1
            if number < 10:
                print("0{} : {}".format(number,myList[i]))
            else:
                print("{} : {}".format(number,myList[i]))
        choice = 1
    isFind = True