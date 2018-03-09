 #!/usr/bin/env python3
# -*-coding:utf-8-*-
import requests
import xlrd
from bs4 import BeautifulSoup

def start():
    data = xlrd.open_workbook('/root/Desktop/weburl.xlsx')
    table = data.sheets()[0]
    nrows = table.nrows
    for i in range(nrows):
        listexl =table.row_values(i)
        name = listexl[0]
        url = listexl[1]
        try:
            get_http(name, url, header)
        except:
            error_url.append(url)

def get_http(name,url1,header):
    tow_url = []
    res = requests.get(url1,headers = header)
    res.encoding = 'utf-8'
    if res.status_code == 200:
        text = res.text
        bs = BeautifulSoup(text,'lxml')
        for link in bs.find_all('a'):
            if str(link.get('href'))[0:4] == "http":
                if str(link.get('href')) not in succ_url:
                    succ_url.append(link.get('href'))
                    succ_name.append(name+link.get_text())
            else:
                tow_url.append(str(link.get('href')))
    else:
        pass
    for url2 in tow_url:
        url22 = url1 + url2
        res22 = requests.get(url22, headers=header)
        res22.encoding = 'utf-8'
        if res22.status_code == 200:
            text = res.text
            bs = BeautifulSoup(text, 'lxml')
            for link in bs.find_all('a'):
                if str(link.get('href'))[0:4] == "http":
                    succ_url.append(link.get('href'))
                    urlname = link.get_text()
                    urlname2 = urlname.strip('\n').strip('\a').strip('\r')
                    succ_name.append(name+urlname2)
                else:
                    pass
        else:
            pass
    with open('/root/Desktop/urls','a') as f:
        for i in range(len(succ_url)):
            f.write(succ_name[i]+'    '+succ_url[i]+'\n')

if __name__ == '__main__':

    error_url = []
    succ_url = []
    succ_name = []
    header = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,en-GB;q=0.6,en;q=0.4,en-US;q=0.2,ja;q=0.2",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
    }
    start()


