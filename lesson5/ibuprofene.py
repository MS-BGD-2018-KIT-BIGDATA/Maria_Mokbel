# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 19:18:55 2017

@author: Maria Mokbel
"""

import requests
import re

url_api = 'https://www.open-medicaments.fr/api/v1/medicaments?query=ibuprofene'
url_med = "https://www.open-medicaments.fr/api/v1/medicaments/"


def getAllIbuprofene(url):
    res=requests.get(url)
    res_json=res.json()
    ids=[]
    for cis in res_json:
        ids.append(cis["codeCIS"])
    return ids

def getMedInfos(url_api,url_med):
  ids=getAllIbuprofene(url_api) 
  meds=[]
  for id in ids:
      res = requests.get(url_med+id)
      med = res.json()
      nom = med["denomination"]
      labo = med["titulaires"][0]
      qte =re.search("\d+",nom)        
      meds.append([nom,labo,qte.group(0)])
  return meds
  
print(getMedInfos(url_api,url_med))