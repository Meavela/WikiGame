# coding=utf-8
from bs4 import BeautifulSoup
import urllib.request
import re
import string
import requests


class Proccessus():
    def __init__(self):
        super().__init__()

    # récupère une page aléatoire
    def ChooseRandomPage(self):
        data = requests.request("GET", "https://fr.wikipedia.org/wiki/Special:Page_au_hasard")
        url = data.url

        req = urllib.request.Request(url=url,
                                    headers={'User-Agent': ' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'})

        handler = urllib.request.urlopen(req)
        with handler as response:
            webpage = response.read().decode('utf-8','ignore')
            soup = BeautifulSoup(webpage, 'html.parser')
            for anchor in soup.find_all("h1",{"id":"firstHeading"}):
                result = str(anchor.contents[0])

        result = self.Replace(result)

        href = url.split("/")[4]
        title = result

        return (href,result)

    # récupère toutes les urls
    def GetUrl(self,pageActuelle):
        req = urllib.request.Request(url="https://fr.wikipedia.org/wiki/"+pageActuelle,
                                    headers={'User-Agent': ' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'})
        handler = urllib.request.urlopen(req)
        with handler as response:
            webpage = response.read().decode('utf-8','ignore')
            soup = BeautifulSoup(webpage, 'html.parser')
            soup = self.Decompose(soup)
            my_list = self.FindAllLinks(soup)

        return my_list

    # remplace le résultat
    def Replace(self,result):
        result = result.replace('<i>','')
        result = result.replace('</i>','')
        result = result.replace('<sub>','')
        result = result.replace('</sub>','')
        result = re.sub('[<][a][b][b][r].{1,40}[>]', '', result)
        result = re.sub('[<].{1,30}[>]', '', result)
        result = re.sub('[<][\/].{1,10}[>]', '', result)

        return result

    # enlève les class et id non voulus
    def Decompose(self,soup):
        for anchor in soup.find_all(True, {"class":["infobox","infobox_v2","infobox_v3","mw-indicators mw-body-content"]}):
            anchor.decompose()
        for anchor in soup.find_all(True, {"id":["toc","mw-navigation","mw-page-base","mw-head-base","footer"]}):
            anchor.decompose()
        
        return soup

    # tri les liens non voulus
    def FindAllLinks(self,soup):
        my_list = []

        for anchor in soup.find_all("a"):
            if 'href="/wiki/' in str(anchor):
                x = re.search("^.{15,50}[:]", str(anchor))
                if x == None:
                    y = re.search("^.{15,100}[#]", str(anchor))
                    if y == None:
                        if "<img" not in str(anchor):
                            if anchor.contents:
                                # Récupérer le href
                                href = anchor.get('href').replace('/wiki/','')
                                # Récupérer le content
                                title = anchor.get('title')

                                if title not in my_list:
                                    my_list.append((href,title))
                                
        
        return my_list