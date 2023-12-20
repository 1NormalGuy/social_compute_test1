import requests
import time

headers = {
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36",
}

tunnel = "y525.kdltps.com:15818"

# 用户名密码方式
username = "t10306954173313"
password = "ucdxints"
proxies = {
    "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel},
    "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel}
}

def get_html(url):
    while True:
        response = requests.get(url,proxies=proxies)
        if response.status_code == 200:
            return response.text
        else:
            print(f"请求失败，状态码：{response.status_code}")
            print("等待2秒后重试...")
            time.sleep(2)
          

def save_html(html, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)


if __name__ == '__main__':
    url = "https://movie.douban.com/subject/1292052/"  
    html = get_html(url)
    if html:
        save_html(html,'output.html')
    print("获取完成了喵！")      


