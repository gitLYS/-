import requests
from lxml import etree
from bs4 import BeautifulSoup
from tools import GetHeaders
from mysql import connector
import settings
import time
from selenium import webdriver

class GetProxy():
    def getproxy(self):
        #xici
        xici_urls=['http://www.xicidaili.com/nn/',
                   'http://www.xicidaili.com/nt/',
                   'http://www.xicidaili.com/wn/',
                   'http://www.xicidaili.com/wt/']

        header=GetHeaders().getHeaders()
        proxies=[]
        i=0
        for i in range(0,len(xici_urls)):
            try:
                s = requests.get(xici_urls[i],headers=header)
                html=etree.HTML(s.text)
                ips=html.xpath('//*[@class="country"][1]/following-sibling::td[1]/text()')
                ports=html.xpath('//*[@class="country"][1]/following-sibling::td[2]/text()')
                i=i+1
                time.sleep(3)
            except:
                continue

            for i in range(0,len(ips)):
                proxies.append(ips[i]+':'+ports[i])


        #快代理
        kuai_urls=['http://www.kuaidaili.com/free/inha/1/',
                   'http://www.kuaidaili.com/free/inha/2/',
                   'http://www.kuaidaili.com/free/inha/3/'
                   ]
        for url in kuai_urls:
            try:
                web=webdriver.PhantomJS(executable_path='/media/lys/ubuntu数据盘/软件/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
                web.get(url)
                time.sleep(2)
                bsObj=BeautifulSoup(web.page_source,'lxml')
                ips=bsObj.findAll('td',{'data-title':'IP'})
                ports=bsObj.findAll('td',{'data-title':'PORT'})
            except:
                continue

            for ip,port in zip(ips,ports):
                proxies.append(ip.text.strip()+':'+port.text.strip())

            time.sleep(3)




        #测试
        proxies_useful=[]
        for proxy in proxies:
            proxy_http={
                        'http':"http://"+proxy,
                        'https':"http://"+proxy,
                    }
            title='hh'
            try:
                s=requests.get('http://music.163.com/',headers=header,proxies=proxy_http,timeout=2)
                title=BeautifulSoup(s.text,'lxml').h1.text
                if title.strip()=='网易云音乐':
                    print('correct:'+proxy)
                    proxies_useful.append(proxy)
            except Exception as e:
                print('error:'+proxy)
                continue

        proxy_list=[]
        conn=connector.connect(**settings.mysql_config)
        cur=conn.cursor()
        for proxy in proxies_useful:
            proxy_http={
                        'http':"http://"+proxy,
                        'https':"http://"+proxy,
                    }
            proxy_list.append(proxy_http)

            #insert into mysql
            sql='insert proxies values(\'%s\',\'1\')' % proxy
            try:
                cur.execute(sql)
            except:
                pass
        conn.commit()
        cur.close()
        conn.close()

        print('getProxy ok!!!')
        return proxy_list


    def checkProxy(self):
        conn=connector.connect(**settings.mysql_config)
        cur=conn.cursor()

        cur.execute('select proxy from proxies')
        proxy_list_fromsql=cur.fetchall()
        cur.close()
        conn.close()


        header=GetHeaders().getHeaders()
        proxy_list={}

        for proxy_tuple in proxy_list_fromsql:
            proxy=proxy_tuple[0]
            proxy_http={
                        'http':"http://"+proxy,
                        'https':"http://"+proxy,
                    }
            title='hh'
            try:
                s=requests.get('http://music.163.com/',headers=header,proxies=proxy_http,timeout=2)
                title=BeautifulSoup(s.text,'lxml').h1.text
                if title.strip()=='网易云音乐':
                    print('correct:'+proxy)
                    proxy_list[proxy]='1'
                else:
                    proxy_list[proxy]='0'
            except Exception as e:
                proxy_list[proxy]='0'
                print('error:'+proxy)
                continue
        #test and insert into mysql
        conn=connector.connect(**settings.mysql_config)
        cur=conn.cursor()
        for proxy in proxy_list.keys():
            if proxy_list[proxy]=='0':

                sql='update proxies set is_useful=\'0\' where proxy=\'%s\'' % proxy
                try:
                    cur.execute(sql)
                    conn.commit()
                except:
                    continue
            else:

                sql='insert proxies values(\'%s\',\'1\')' % proxy
                try:
                    cur.execute(sql)
                    conn.commit()
                except:
                    continue

        cur.execute('delete from proxies where is_useful=\'0\'')
        conn.commit()
        cur.close()
        conn.close()

        print('checkProxy ok!!')
        time.sleep(600)

if __name__ == '__main__':
    while True:
        GetProxy().getproxy()
        GetProxy().checkProxy()
