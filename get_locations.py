import requests
import time
import dic
import get_comment
import os
from bs4 import BeautifulSoup
from openpyxl import Workbook, load_workbook
from random import randint
import csv




#request
def get_html(url,headers):
    # 使用requests.get获取网页内容
   # proxy = proxies
    response = requests.get(url, headers=headers)

    # 检查请求是否成功（状态码为200）
    if response.status_code == 200:
        return response.text
    else:
        return None

def get_comments(url,headers,arr):
    # 使用requests.get获取网页内容
    html=get_html(url,headers)
    if html:
        soup = BeautifulSoup(html, 'lxml')
        locations = []
        locations_divs = soup.find_all('span', {'class': 'comment-location'})
        for locations_div in locations_divs:
            if locations_div:
                locations.append(locations_div.text)

        for ip in locations:
            if ip:
                if ip not in dic.comment_location:
                    ip = '海外'
                arr[dic.comment_location[ip]] = arr[dic.comment_location[ip]] + 1

def start(url,headers,key):
    loc_arr = [0 for i in range(36)]
     # 获取评论归属地信息
    get_comments(url, headers, loc_arr)

    locationinfo = []
    locationinfo.append(dic.film_id_name[key])
    for i in range(1, 36):
        locationinfo.append(loc_arr[i])
    filepath = './information/comment_loc.xlsx'
    get_comment.get_excel(filepath, locationinfo)

if __name__ == "__main__":
    url = "https://movie.douban.com/subject/{id}/comments?start={page}&limit=100&status=P&sort=new_score"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    for key in dic.film_id_name.keys():
        print(f"正在获取{dic.film_id_name[key]}的评论属地喵！")
        for n in range(10):  # 一页100条 每次爬取完翻页
            url2 = url.format(id=key, page=n*100)
            start(url2, headers, key)
            print(f"已经获取到第{n+1}页")
            crawl_interval = randint(2, 5)
            time.sleep(crawl_interval)
        print(f"{dic.film_id_name[key]}的评论属地获取完成了喵！")
