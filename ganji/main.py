from multiprocessing import Pool
from channel_extract import all_link
from page_parsing import get_link_from,get_item_info_from,url_list

if __name__ == '__main__':
    pool = Pool()
    # pool.map(get_link_from,all_link)#添加链接
    pool.map(get_item_info_from,[i['url']for i in url_list.find()])
    pool.close()
    pool.join()