# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 19:18:55 2017

@author: Maria Mokbel
"""

import requests
import json
from bs4 import BeautifulSoup

GITHUB_API = 'https://api.github.com'
url = 'https://gist.github.com/paulmillr/2657075'
token = "d480eea032f8da2e733f0a5365009ca1a88fb26d"

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

    
def getBestContributors(url):
  soup = getSoupFromURL(url)
  if soup:

    best_contributors = soup.find("tbody").find_all("tr")
    return best_contributors

def getStars(url, username,token):
    res=requests.get(url+"/users/"+username+"/repos?access_token="+token)
    res_json=res.json()
    stars=0
    if len(res_json) != 0:
        for repo in res_json:
            stars+=repo["stargazers_count"]
        return stars/len(res_json)
    else:
        return 0
l=[]
for bc in getBestContributors(url):
    l.append((bc.find("td").find("a").text,getStars(GITHUB_API,bc.find("td").find("a").text,token)))


lSorted=sorted(l,key=lambda x:x[1],reverse=True)

for user in lSorted:
    print(user)

