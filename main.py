import requests
import time
import dic
import get_comment
import get_info
import emo
from bs4 import BeautifulSoup
from random import randint
import csv
import random


headers ={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/54.0.2840.99 Safari/537.36"
}

if __name__ == '__main__':
    # 使用函数
    for key in dic.film_id_name:
        print("要开始获取"+dic.film_id_name[key]+"的信息了喵！好激动！")
        #用于存放统计评论属地数据
        loc_arr = [0 for i in range(36)]
        locationinfo = []
        locationinfo.append(dic.film_id_name[key])

        #获取电影信息
        url1 = "https://movie.douban.com/subject/{id}".format(id=key)
        get_info.getfilminfo(url1,headers)
        print(dic.film_id_name[key]+"的基础信息获取完成了喵！接下来要开始获取评论和属地了喵！")

        for n in range(10):
        #一页100条 每次爬取完翻页
            url2 = "https://movie.douban.com/subject/{id}/comments?start={page}&limit=100&status=P&sort=time".format(id=key,page=n*100)

        # 获取评论
            comments = get_comment.get_comments(url2,headers,loc_arr)
            #if comments:
            #    get_comment.save_comments(comments, f'./information/{dic.film_id_name[key]}_comments.csv')
            print(f"正在获取第{n+1}页的数据")
            crawl_interval = random.randint(2,4) 
            time.sleep(crawl_interval)
        print(dic.film_id_name[key]+"的评论获取完成了喵！接下来要开始获取属地了喵！")


        # 获取评论归属地信息
        for i in range(1, 36):
            locationinfo.append(loc_arr[i])
        filepath = './information/comment_loc.xlsx'
        get_comment.get_excel(filepath, locationinfo)
        print(dic.film_id_name[key]+"的获取完成了喵！接下来要开始获取下一部电影了喵！")
    print("全部获取完成了喵！主人可以用数据来分析了喵！")


      