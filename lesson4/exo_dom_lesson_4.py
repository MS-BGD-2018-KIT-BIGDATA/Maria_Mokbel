# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 19:18:55 2017

@author: Maria Mokbel
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

urlRenault = 'https://www.leboncoin.fr/voitures/offres/ile_de_france/?o=1&it=1&brd=Renault&mdl=Zoe'
urlRenaultCote = 'https://www.lacentrale.fr/cote-voitures-renault-zoe--2013-.html'

def getSoupFromURL(url, method='get', data={}):
  if method == 'get':
    res = requests.get(url)
  elif method == 'post':
    res = requests.post(url, data=data)
  else:
    return None

  if res.status_code == 200:
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup
  else:
    return None

def getCoteMoyenne(url,version):
    soup = getSoupFromURL(url)
    if soup:
        all_versions = soup.find_all(class_="listingResultLine")
        if (version == "intens"):
            soup2 = getSoupFromURL("https://www.lacentrale.fr/"+all_versions[0].find("a")['href'])
            return soup2.find(class_="jsRefinedQuot").text
        elif (version == "intens type 2"):
            soup2 = getSoupFromURL("https://www.lacentrale.fr/"+all_versions[1].find("a")['href'])
            return soup2.find(class_="jsRefinedQuot").text
        elif (version == "life"):
            soup2 = getSoupFromURL("https://www.lacentrale.fr/"+all_versions[2].find("a")['href'])
            #print("https://www.lacentrale.fr/"+all_versions[2].find("a")['href'])
            return soup2.find(class_="jsRefinedQuot").text
        elif (version == "life type 2"):
            soup2 = getSoupFromURL("https://www.lacentrale.fr/"+all_versions[3].find("a")['href'])
            return soup2.find(class_="jsRefinedQuot").text
        elif (version == "zen"):
            soup2 = getSoupFromURL("https://www.lacentrale.fr/"+all_versions[4].find("a")['href'])
            return soup2.find(class_="jsRefinedQuot").text
        elif (version == "zen type 2"):
            soup2 = getSoupFromURL("https://www.lacentrale.fr/"+all_versions[5].find("a")['href'])
            return soup2.find(class_="jsRefinedQuot").text
        else:
            return ""

        
def getCarInfos(url):
  soup = getSoupFromURL(url)
  if soup:
    df = pd.DataFrame(columns=['Titre','Version','Année','Prix','Kilométrage','Tel','Pro','Cote'])
    all_cars = soup.find_all(class_="list_item")
    for c in all_cars:
        soup2 = getSoupFromURL("https:"+c['href'])
        titre = re.sub(" |\n|\t","",soup2.find("h1").text)
        if (re.search("zen",titre,re.IGNORECASE)):
            version = "zen"
        elif (re.search("intens",titre,re.IGNORECASE)):
            version = "intens"
        elif (re.search("life",titre,re.IGNORECASE)):
            version = "life"
        else:
            version = "unknown"
        if (re.search("type2|type 2",titre,re.IGNORECASE)):
            version+=" type 2"
        cote = getCoteMoyenne(urlRenaultCote,version)
        values = soup2.find_all(class_="value")
        annee = re.sub(" |\n|\t","",values[4].text)
        prix = re.sub(" |\n|\t|€","",values[0].text)
        km = re.sub(" |\n|\t|KM","",values[5].text)
        if (len(soup2.find_all(class_="phone_number"))==0):
            tel = 0
        else:
            tel = soup2.find_all(class_="phone_number")[0].find("a").text
        if (soup2.find(class_="ispro")):
            pro = "Oui"
        else:
            pro = "Non"
        df.loc[-1]=[titre,version,int(annee),int(prix),int(km),tel,pro,cote]
        df.index = df.index + 1  # shifting index
    return df.sort_index()
        
getCarInfos(urlRenault).to_csv("C:/Users/Maria Mokbel/Desktop/prixRenault.csv")
