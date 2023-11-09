from unicodedata import name
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import urllib.request
import ssl
from dotenv import load_dotenv
import os
import json

from selenium.webdriver.common.by import By
import sys
from sys import exit
from urllib.parse import urlparse, parse_qs
import numpy as np
from selenium.webdriver.chrome.service import Service


load_dotenv()
# Variables de entorno
FACEBOOK_USER = os.getenv("FACEBOOK_USER")
FACEBOOK_PASSWORD = os.getenv("FACEBOOK_PASSWORD")

service = Service('/Users/oktanait/Downloads/chrome117/chromedriver')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# driver = webdriver.Chrome(PATH)
driver.maximize_window()
driver.get("https://www.facebook.com/login/")

ssl._create_default_https_context = ssl._create_unverified_context
textos = []
# login
time.sleep(3)
username = driver.find_element("css selector", "input[name='email']")
password = driver.find_element("css selector", "input[name='pass']")
username.clear()
password.clear()
username.send_keys(FACEBOOK_USER)
password.send_keys(FACEBOOK_PASSWORD)
login = driver.find_element("css selector", "button[type='submit']").click()
time.sleep(6)
name = "Kleiver Lapa Marcelo"
driver.get("https://www.facebook.com/search/people/?q="+name)
time.sleep(2)
# Imagenes de los primero 4 perfiles
torres = driver.find_elements("tag name", "image")
# torres = driver.find_elements("tag name", "image[style='height: 60px; width: 60px;']")
torres = [image.get_attribute('xlink:href') for image in torres]
# arrayData1 = [torres[1],torres[2],torres[3],torres[4]]
secuencia = 0
if len(torres) == 0:
    arrayData1 = []
elif len(torres) <= 2:
    arrayData1 = [torres[1]]
    secuencia = 2
elif len(torres) <= 3:
    arrayData1 = [torres[1], torres[2]]
    secuencia = 3
elif len(torres) <= 4:
    arrayData1 = [torres[1], torres[2], torres[3]]
    secuencia = 4
else:
    arrayData1 = [torres[1], torres[2], torres[3], torres[4]]
    secuencia = 5

# aqui termina las imagenes
arrayData = []
arrayData3 = []
for publ in range(1, secuencia):
    # searchbox1 = driver.find_element(By.XPATH,"//div[contains(@class,'x193iq5w x1xwk8fm')]/div["+str(publ)+"]/div/div/div/div/div/div/div/a").get_attribute('href')
    searchbox1 = driver.find_element(By.XPATH, "//div[contains(@class,'x193iq5w x1xwk8fm')]/div["+str(
        publ)+"]//div[contains(@class,'x1lq5wgf xgqcy7u x30kzoy x9jhf4c x1lliihq')]/div/div/div/a").get_attribute('href')
    arrayData.append(searchbox1)
    # nombre
    searchbox2 = driver.find_element(
        By.XPATH, "//div[contains(@class,'x193iq5w x1xwk8fm')]/div["+str(publ)+"]//div[contains(@class,'xu06os2 x1ok221b')]")
    searchbox2 = searchbox2.text
    arrayData3.append(searchbox2)
    time.sleep(1.5)

arrayData2 = []
for soyu in arrayData:
    if "&__tn__=%3C" and 'profile' in soyu:
        t = urlparse(soyu)
        d = parse_qs(t.query)
        value = d.get("id")
        arrayData2.append(value[0])
        continue
    if "?__tn__" in soyu:
        stringdata = soyu
        data_split = stringdata.split("/")
        data = data_split[3]
        stringdata1 = data
        data_split1 = stringdata1.split("?")
        data1 = data_split1[0]
        arrayData2.append(data1)
        continue
    if "profile" in soyu:
        data = (soyu.split('=')[1])
        arrayData2.append(data)
    else:
        stringdata = soyu
        data_split = stringdata.split("/")
        data = data_split[3]
        arrayData2.append(data[3])

# print(arrayData2)
result = [{"URL": a, "Profile": b, "Username": c, "Nombre": d}
          for a, b, c, d in zip(arrayData, arrayData1, arrayData2, arrayData3)]
res = json.dumps(result)
print(res)
