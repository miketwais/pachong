import requests
from bs4 import BeautifulSoup
import urllib
import os
import datetime
import threading
import time

i = 0
FACE_URL_LIST = []
URL_LIST = []
base_url = 'https://www.doutula.com/photo/list/?page='
for x in range(1,100):
    url = base_url+str(x)
    URL_LIST.append(url)
#初始化锁
gLock = threading.Lock()

#生产者，负责从页面中提取表情图片的url
class producer(threading.Thread):
    def run(self):
        while len(URL_LIST)>0:
            #访问时需要加锁
            gLock.acquire()
            cur_url = URL_LIST.pop()
            #使用完后及时释放锁，方便其他线程使用
            gLock.release()
            response = requests.get(cur_url)
            soup = BeautifulSoup(response.content, 'lxml')
            img_list = soup.find_all('img', attrs={'class': 'img-responsive lazy image_dta'})
            gLock.acquire()
            for img in img_list:  # 一页上的图片
                print(img['data-original'])
                src = img['data-original']
                if not src.startswith('http'):
                    src = 'http:' + src
                FACE_URL_LIST.append(src)
            gLock.release()
            time.sleep(0.5)


#消费者，负责从FACE_URL_LIST中取出url，下载图片
class consumer(threading.Thread):
    def run(self):
        global i
        j=0
        print ('%s is running' % threading.current_thread)
        while True:
            #上锁
            gLock.acquire()
            if len(FACE_URL_LIST) == 0:
                #释放锁
                gLock.release()
                j = j + 1
                if (j > 1):
                    break
                continue
            else:
                #从FACE_URL_LIST中取出url，下载图片
                face_url = FACE_URL_LIST.pop()
                gLock.release()
                filename = face_url.split('/').pop()
                fileextra = filename.split('.').pop()
                filestring = str(i) + '.' + fileextra
                path = os.path.join('images', filename)
                #path = os.path.join('images', filestring)
                # 下载图片
                headers = {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Encoding': 'gzip, deflate, sdch',
                    'Accept-Language': 'zh-CN,zh;q=0.8',
                    'Connection': 'keep-alive',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.235'
                }
                # urllib.request.urlretrieve(url,path,header)
                req = urllib.request.Request(url=face_url, headers=headers)
                cont = urllib.request.urlopen(req).read()
                root = r"" + path + ""
                f = open(root, 'wb')
                f.write(cont)
                f.close
                print(i)
                i += 1



if __name__ == '__main__': #在本文件内运行
    # begin
    print(datetime.datetime.now())
    #2个生产者线程从页面抓取表情链接
    for x in range(2):
        producer().start()

    #5个消费者线程从FACE_URL_LIST中提取下载链接，然后下载
    for x in range(5):
        consumer().start()
    #end
    print (datetime.datetime.now())