import requests
from bs4 import BeautifulSoup
import urllib
import os
FACE_URL_LIST = [1,2,3,4,5,6]
i=0
while True:
    if len(FACE_URL_LIST) == 0:
        i=i+1
        if(i>1):
            break
        continue
    else:
        res = FACE_URL_LIST.pop()
        print(res)