 #!/usr/bin/env python3
#-*-utf-8-*-
import requests
from bs4 import BeautifulSoup
import re
head={
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, sdch',
'Accept-Language':'zh-CN,zh;q=0.8,en-GB;q=0.6,en;q=0.4,en-US;q=0.2,ja;q=0.2',
'Host':'www.xicidaili.com',
'Referer':'http://www.xicidaili.com/wt/',
'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
}
def find():
    source={}
    for i in ['nn','nt','wn','wt']:
        url = 'http://www.xicidaili.com/'+i
        respon = requests.get(url=url,headers=head)
        soup = BeautifulSoup(respon.text,'lxml')
        #print(soup)
        datas = soup.find_all(name='tr',attrs={'class':re.compile('|[^odd]')})
        #print(datas)
        for data in datas:
            proxy_concat = BeautifulSoup(str(data),'lxml')
            #print(proxy_concat)
            proxys = proxy_concat.find_all(name='td')
            #print(proxys)
            ip = str(proxys[1].string)
            port = str(proxys[2].string)
            print('%s:%s'%(ip,port))

if __name__ == '__main__':
    find()

