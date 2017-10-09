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

def getCarInfos(url):
  soup = getSoupFromURL(url)
  if soup:
    df = pd.DataFrame(columns=['Titre','Version','Année','Prix','Kilométrage','Tel','Pro'])
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
        df.loc[-1]=[titre,version,int(annee),int(prix),int(km),tel,pro]
        df.index = df.index + 1  # shifting index
    return df.sort_index()
        
print(getCarInfos(urlRenault))
