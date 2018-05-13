from bs4 import BeautifulSoup
import requests


def get_index_url():
    urls = []
    host_url = 'http://bj.ganji.com'
    url = 'http://bj.ganji.com/wu/'
    wb_data = requests.get(url,timeout=6)
    soup = BeautifulSoup(wb_data.text,'lxml')
    links = soup.select('dl.fenlei > dt > a')
    for link in links:
        pre_url = host_url + link.get('href')
        wb_data = requests.get(pre_url,timeout=6)
        soup = BeautifulSoup(wb_data.text,'lxml')
        type_lists = soup.select('dl.secitem > dd > a')
        for type_list in type_lists:
            urls.append(host_url + type_list.get('href'))
    return urls
all_link = get_index_url()
#拼接各类目链接