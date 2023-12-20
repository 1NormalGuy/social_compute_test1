import requests
import time
import dic
import os
from bs4 import BeautifulSoup
from openpyxl import Workbook, load_workbook
from random import randint
import csv
import random

tunnel = "y525.kdltps.com:15818"

# 用户名密码方式
username = "t10306954173313"
password = "ucdxints"
proxies = {
    "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel},
    "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel}
}

#request
def get_html(url,headers,flag):
    # 使用requests.get获取网页内容
   # proxy = proxies
    response = requests.get(url, headers=headers,proxies=proxies)

    # 检查请求是否成功（状态码为200）
    if response.status_code == 200:
        if flag==0:
            print(f"请求成功，状态码：{response.status_code}")
        # 返回HTML内容
        return response.text
    else:
        if flag==0:
            print(f"请求失败，状态码：{response.status_code}")
        return None

def get_comments(url,headers):
    # 使用requests.get获取网页内容
    html=get_html(url,headers,0)
    if html:
        get_user_url(html)
        soup = BeautifulSoup(html, 'lxml')
        comments = []
        comment_divs = soup.find_all('p', {'class': 'comment-content'})
        for comment_div in comment_divs:
            comment = comment_div.find('span', {'class': 'short'})
            if comment:
                comments.append(comment.text)

        return comments
    return None


#获取评论用户个人主页url
def get_user_url(html):
    if html:
        soup = BeautifulSoup(html, 'lxml')
        url_list = []

        # 在comment-info中爬取链接 防止爬到无关链接
        links_divs = soup.find_all('span',{'class': 'comment-info'})
        for links_div in links_divs:
            if links_div:
                links=links_div.find_all('a')
                for link in links:
                    url=link.get('href')
                    url_list.append(url)

        #过滤url_list中的无关元素
        url_list = list(filter(lambda url_str: 'http' in url_str, url_list))
        #过滤重复项
        new_url_list = list(dict.fromkeys(url_list))
    return new_url_list


def get_locations(url,headers,arr):
    html = get_html(url, headers,1)
    if html:
        url_list=get_user_url(html)
        for user_url in url_list:
            user_html=get_html(user_url,headers,1)
            if user_html:
                soup = BeautifulSoup(user_html,'lxml')
                user_ip = soup.find('span', {'class': 'ip-location'})
                if user_ip:
                    #分割字符串删掉IP属地： 只保留地区
                    ip = user_ip.text.split('：')[1]
                    if ip not in dic.comment_location:
                        ip = '海外'
                    arr[dic.comment_location[ip]]=arr[dic.comment_location[ip]]+1




def save_comments(comments, filename):
    # 使用'a'模式打开文件，这将会创建一个新的文件或续写已存在的文件
    with open(filename, 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        for comment in comments:
            # 写入一行数据
            writer.writerow([comment])


def get_excel(filepath, allinfo):
    try:
        if not os.path.exists(filepath):
            tableTitle = [" ","河北","山西","辽宁","吉林","黑龙江","江苏","浙江","安徽","福建","江西","山东","河南","湖北","湖南","广东","海南","四川","贵州","云南","陕西","甘肃","青海","台湾"
,"内蒙古","广西","西藏","宁夏","新疆","北京","天津","上海","重庆","香港","澳门",'海外']
            wb = Workbook()
            ws = wb.active
            ws.title = 'sheet1'
            ws.append(tableTitle)
            wb.save(filepath)

            crawl_interval = random.randint(2,4) 
            time.sleep(crawl_interval)

        wb = load_workbook(filepath)
        ws = wb.active
        ws.title = 'sheet1'
        ws.append(allinfo)
        wb.save(filepath)
        return True
    except:
        return False