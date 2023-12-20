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
from tqdm import tqdm



headers ={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/54.0.2840.99 Safari/537.36"
}

if __name__ == '__main__':
    # 使用函数
    for key in dic.film_id_name:
        print(dic.film_id_name[key])

        #获取电影信息
        url1 = "https://movie.douban.com/subject/{id}".format(id=key)
        get_info.getfilminfo(url1,headers)
        print(dic.film_id_name[key]+"基础信息获取完成,接下来获取粉丝属地及评论")

        for n in range(10):
            #一页40条 每次爬取完翻页
            url2 = "https://movie.douban.com/subject/{id}/comments?start={page}&limit=40&status=P&sort=new_score".format(id=key,page=n*40)
            
            # 获取评论归属地信息
            loc_arr=[0 for i in range(36)]
            get_comment.get_locations(url2, headers,loc_arr)
            locationinfo=[]
            locationinfo.append(dic.film_id_name[key])
            for i in range(1,36):
                locationinfo.append(loc_arr[i])
            filepath = './information/comment_loc.xlsx'
            get_comment.get_excel(filepath, locationinfo)
            crawl_interval = random.randint(2,4)  
            time.sleep(crawl_interval)

        print(dic.film_id_name[key]+"粉丝属地获取完成")
            
        for i in tqdm(range(10)):
            # 获取评论
            url3 = "https://movie.douban.com/subject/{id}/comments?start={page}&limit=40&status=P&sort=new_score".format(id=key,page=i*40)

            comments = get_comment.get_comments(url3,headers)
            if comments:
                 get_comment.save_comments(comments, f'./information/{dic.film_id_name[key]}_comments.csv')
            print(dic.film_id_name[key]+"评论获取完成")

            crawl_interval = random.randint(2,4)     
            time.sleep(crawl_interval)
            