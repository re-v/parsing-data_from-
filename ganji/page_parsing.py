import requests
from bs4 import BeautifulSoup
import pymongo
from datetime import datetime

client = pymongo.MongoClient('localhost',27017)
ganji = client['ganji']
url_list = ganji['url_list']
item_info = ganji['item_info']
#pymongo执行代码

def get_link_from(url,times = 0):#传入all_link=url
    if times > 10:#限制重复
        return
    for page in range(1,31):#自增30页
        list_views = '{}o{}'.format(url,page)
        try:
            wb_data = requests.get(list_views,timeout=6)#timeout超时限制
        except:
            return get_link_from(url,times + 1)
        soup = BeautifulSoup(wb_data.text,'lxml')
        if soup.select('div.noinfotishi'):#为空则返回
            return
        else:
            for link in soup.select('td.t > a'):
                item_link = link.get('href')
                if 'zhuanzhuan' in item_link:
                    print(item_link)
                    url_list.insert_one({'url':item_link})#添加数据{'url':'xx'}
#初始链接

def get_item_info_from(url,times = 0):
    if times > 10:
        return
    try:
        wb_data = requests.get(url,timeout = 6)
    except:
        return get_item_info_from(url,times + 1)
    soup = BeautifulSoup(wb_data.text,'lxml')
    item = item_info.find({'url':url})
    if item.count() > 0:
        if soup.select('span.soldout_btn'):
            print('get one!')
            item_info.update({'url':url},{'$set':{'sold_date':str(datetime.now().strftime('%Y,%m,%d'))}})
    else:
        title = soup.select('h1.info_titile')
        price = soup.select('span.price_now > i')
        area = soup.select('div.palce_li > span > i')
        view = soup.select('span.look_time')
        cate = soup.select('span.crb_i > a')
        data = {
            'title':title[0].text if title else None,
            'price':price[0].text if price else 0,
            'area':area[0].text.split('-') if area else None,
            'view':view[0].text if view else None,
            'cate':cate[-1].text.strip() if cate else None,
            'date':str(datetime.now().strftime('%Y,%m,%d')),
            'sold_date':None,
            'url':url,
        }
        #获取商品信息详情!
        print(data)
        item_info.insert_one(data)
