# coding=utf-8
from __future__ import print_function, unicode_literals
from pprint import pprint
from bs4 import BeautifulSoup
from PyInquirer import prompt, print_json
import urllib.request
import re
import string
import os

def ChooseRandomPage():
    req = urllib.request.Request(url="https://fr.wikipedia.org/wiki/Special:Page_au_hasard",
                                headers={'User-Agent': ' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'})

    handler = urllib.request.urlopen(req)
    with handler as response:
        webpage = response.read().decode('utf-8','ignore')
        soup = BeautifulSoup(webpage, 'html.parser')
        for anchor in soup.find_all("h1",{"id":"firstHeading"}):
            result = str(anchor.contents[0])
    
    # print(result)
    # print("----")

    result = Replace(result)

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

def Replace(result):
    result = result.replace('<i>','')
    result = result.replace('</i>','')
    result = result.replace('<sub>','')
    result = result.replace('</sub>','')
    result = re.sub('[<][a][b][b][r].{1,40}[>]', '', result)
    result = re.sub('[<].{1,30}[>]', '', result)
    result = re.sub('[<][\/].{1,10}[>]', '', result)

    return result

def Decompose(soup):
    for anchor in soup.find_all(True, {"class":["infobox","infobox_v2","infobox_v3","mw-indicators mw-body-content"]}):
        anchor.decompose()
    for anchor in soup.find_all(True, {"id":["toc","mw-navigation","mw-page-base","mw-head-base","footer"]}):
        anchor.decompose()
    
    # print(soup)
    return soup

def FindAllLinks(soup):
    my_list = []

    for anchor in soup.find_all("a"):
        if 'href="/wiki/' in str(anchor):
            x = re.search("^.{15,50}[:]", str(anchor))
            if x == None:
                y = re.search("^.{15,100}[#]", str(anchor))
                if y == None:
                    if "<img" not in str(anchor):
                        if anchor.contents:
                            z = re.findall('href="\/wiki\/(.{1,100})" title="(.{1,100})">', str(anchor))
                            if len(z) != 0:
                                if z[0] not in my_list:
                                    my_list.append(z[0])
    
    return my_list

pageDepart = ChooseRandomPage()
pageCible = ChooseRandomPage()
pageActuelle = pageDepart.replace(' ','_')
lastPage = []
lastPage.append(pageActuelle)
isFind = False
tour = 0
while isFind == False:
    os.system('cls' if os.name == 'nt' else 'clear')
    tour += 1
    page = 1
    choice = None
    print("********** WikiGame ********** Tour n°{}".format(tour))
    print("Départ : "+pageDepart)
    print("-----> https://fr.wikipedia.org/wiki/"+pageDepart.replace(' ','_'))
    print("Cible : "+pageCible)
    print("-----> https://fr.wikipedia.org/wiki/"+pageCible.replace(' ','_'))
    
    while choice == 0 or choice == -1 or choice == -2 or choice == None: 
        print("Actuellement : "+pageActuelle)
        myList = GetUrl(pageActuelle)
        choices = []
        if len(myList) < 20:
            mini = 0
            maxi = len(myList)
        else:
            mini = (page-1)*20
            if len(myList) < page*20:
                maxi = len(myList)
            else:
                maxi = page*20

        if len(lastPage) != 1:
            choices.append("00: Retour")
        
        for i in range(mini,maxi):
            number = i+1
            if number < 10:
                choices.append("0{}: {}".format(number,myList[i][1]))
            else:
                choices.append("{}: {}".format(number,myList[i][1]))
        if page != 1:
            choices.append("-2: Voir les liens précédents")

        if len(myList) > (20*page):
            choices.append("-1: Voir les liens suivants")

        questions = [
            {
                'type':'list',
                'name':'choices',
                'message':'Votre choix : ',
                'choices':choices
            }
        ]
        answers = prompt(questions)
        print(int(answers['choices'].split(':')[0]))
        choice = int(answers['choices'].split(':')[0])

        if choice == 0:
            page = 1
            lastPage.pop()
            pageActuelle = lastPage[len(lastPage)-1]
        elif choice == -1:
            page += 1
        elif choice == -2:
            page -= 1
        else:
            pageActuelle = myList[choice-1][0]
            lastPage.append(pageActuelle)
    # isFind = True