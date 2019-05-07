import requests
from bs4 import BeautifulSoup
import urllib
import os

url = 'https://www.doutula.com/photo/list/?page=1'
response = requests.get(url)
soup = BeautifulSoup(response.content,'lxml')
img_list = soup.find_all('img',attrs={'class':'img-responsive lazy image_dta'})
i=0
for img in img_list:
    print (img['data-original'])
    src = img['data-original']
    #src = '//ws1.sinaimg.cn/bmiddle/9150e4e5ly1fjlv8kgzr0g20ae08j74p.gif'
    if not src.startswith('http'):
        src= 'http:'+src
    filename = src.split('/').pop()
    fileextra = filename.split('.').pop()
    filestring = i+'.'+fileextra
    path = os.path.join('images',filestring)
    # 下载图片
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.235'
    }
    #urllib.request.urlretrieve(url,path,header)
    req = s(url=src, headers=headers)
    cont = urllib.request.urlopen(req).read()
    root = r""+path+""
    f=open(root,'wb')
    f.write(cont)
    f.close
    i += 1

