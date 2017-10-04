# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 19:18:55 2017

@author: Maria Mokbel
"""

import requests
from bs4 import BeautifulSoup


url = 'http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=056&dep=075&type=BPS&param=5&exercice='
number_class='montantpetit G'
number_A_eu=1
number_A_moy=2
number_B_eu=4
number_B_moy=5
number_C_eu=10
number_C_moy=11
number_D_eu=13
number_D_moy=14


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

def getNumber(url, classname,num):
  soup = getSoupFromURL(url)
  if soup:

    all_bold_numbers = soup.find_all(class_=classname)
    return all_bold_numbers[num].text.strip()

for i in range (2010,2016):
    print('Résultats des comptes de la ville de Paris pour les exercices',i)
    print('A: ', getNumber(url+str(i),number_class,number_A_eu), 'Euros par habitant')
    print('A: ', getNumber(url+str(i),number_class,number_A_moy), 'Moyenne de la strate')
    print('B: ', getNumber(url+(str(i)),number_class,number_B_eu), 'Euros par habitant')
    print('B: ', getNumber(url+str(i),number_class,number_B_moy), 'Moyenne de la strate')
    print('C: ', getNumber(url+str(i),number_class,number_C_eu), 'Euros par habitant')
    print('C: ', getNumber(url+str(i),number_class,number_C_moy), 'Moyenne de la strate')
    print('D: ', getNumber(url+str(i),number_class,number_D_eu), 'Euros par habitant')
    print('D: ', getNumber(url+str(i),number_class,number_D_moy), 'Moyenne de la strate')
