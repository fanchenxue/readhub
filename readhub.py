import requests
from urllib import parse
import random
import time
from scrapy import Request

url = 'https://api.readhub.cn/news'

headers = {
    'Host': 'api.readhub.cn',
    'Origin': 'https://readhub.cn',
    'Referer': 'https://readhub.cn/news',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36',
    'Cookie': '_ga=GA1.2.1320741995.1536831409; _gid=GA1.2.929719020.1536831409'
}
#解析第一页,获取下一页信息
def parse_first_page():
    response = requests.get(url, headers=headers).json()
    jsons = response.get('data')[-1]
    next_page_time = jsons['publishDate'].split('.')[0].replace('T', ' ')
    next_page = time.mktime(time.strptime(next_page_time, '%Y-%m-%d %H:%M:%S'))
    next_page = (int(next_page) + 28800) * 1000
    return next_page
#解析第二页,获取下一页信息
def parse_next1_page(n_page):
    first_data = {
        'lastCursor': n_page,
        'pageSize': '10'
    }
    base_url = 'https://api.readhub.cn/news?' + parse.urlencode(first_data)
    response = requests.get(base_url, headers=headers).json()
    jsons = response.get('data')[-1]
    next_page_time = jsons['publishDate'].split('.')[0].replace('T', ' ')
    next_page = time.mktime(time.strptime(next_page_time, '%Y-%m-%d %H:%M:%S'))
    next_page = (int(next_page) + 28800) * 1000
    data = {
        'lastCursor': next_page,
        'pageSize': '10'
    }
    full_url = 'https://api.readhub.cn/news?' + parse.urlencode(data)
    return full_url
#回调函数,循环获取下一页与url链接
def parse_next2_page(url):
    # print(url)
    response = requests.get(url, headers=headers).json()
    jsons = response.get('data')[-1]
    next_page_time = jsons['publishDate'].split('.')[0].replace('T', ' ')
    next_page = time.mktime(time.strptime(next_page_time, '%Y-%m-%d %H:%M:%S'))
    next_page = (int(next_page) + 28800) * 1000
    data = {
        'lastCursor': next_page,
        'pageSize': '10'
    }
    full_url = 'https://api.readhub.cn/news?' + parse.urlencode(data)
    return full_url
#解析详情页内容
def parse_info(full_url):
    json_contents = requests.get(full_url, headers=headers).json()
    # print(json_contents.get('data'))
    return json_contents.get('data')
if __name__ == '__main__':
    page = parse_first_page()
    url= parse_next1_page(page)
    print(url)
    full_url = parse_next2_page(url=url)
    print(full_url)
    for i in range(10):
        full_url = parse_next2_page(url=full_url)
        content = parse_info(full_url)
        print(full_url)