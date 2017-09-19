import requests
from tools import GetHeaders
from bs4 import BeautifulSoup
from selenium import webdriver
import time
headers=GetHeaders().getHeaders()
#PROXY = "113.107.166.246:8bsObj.findAll('td',{'data-title':'IP'})08"


web=webdriver.PhantomJS(executable_path='/media/lys/ubuntu数据盘/软件/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
web.get('http://www.kuaidaili.com/free/inha/1/')
time.sleep(1)
bsObj=BeautifulSoup(web.page_source,'lxml')
ips=bsObj.findAll('td',{'data-title':'IP'})
ports=bsObj.findAll('td',{'data-title':'PORT'})

for ip,port in zip(ips,ports):
    print(ip.text.strip()+':'+port.text.strip())

