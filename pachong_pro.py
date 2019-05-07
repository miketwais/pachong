import requests
from bs4 import BeautifulSoup
import urllib
import os
import datetime
#begin
print (datetime.datetime.now())
URL_LIST = []
base_url = 'https://www.doutula.com/photo/list/?page='
for x in range(1,3):
    url = base_url+str(x)
    URL_LIST.append(url)
i = 0
for page_url in URL_LIST:
        response = requests.get(page_url)
        soup = BeautifulSoup(response.content,'lxml')
        img_list = soup.find_all('img',attrs={'class':'img-responsive lazy image_dta'})
        for img in img_list: #一页上的图片
            print (img['data-original'])
            src = img['data-original']
            if not src.startswith('http'):
                src= 'http:'+src
            filename = src.split('/').pop()
            fileextra = filename.split('.').pop()
            filestring = str(i)+'.'+fileextra
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
            req = urllib.request.Request(url=src, headers=headers)
            cont = urllib.request.urlopen(req).read()
            root = r""+path+""
            f=open(root,'wb')
            f.write(cont)
            f.close
            i += 1
#end
print (datetime.datetime.now())
