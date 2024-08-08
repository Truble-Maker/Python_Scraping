# 线程池: 一次性开辟一些进程，用户直接给线程池提交任务，线程任务的调度交给线程池来完成
# from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
#
# def fn(name):
#     for i in range(1000):
#         print(name, i)
#
# if __name__ == '__main__':
#     # 创建线程池
#     with ThreadPoolExecutor(50) as t: # 创建一个有50个进程的线程池
#         for i in range(100):
#             t.submit(fn, name=f"线程{i}")
#     # 等待线程池中的任务全部执行完毕，才继续执行，该行为被称为守护
#     print("123")


# 本程序利用多线程爬取菜价

import csv
import threading

import requests
from lxml import etree
from concurrent.futures import ThreadPoolExecutor

f = open("菜价plus.csv", "w", encoding="utf-8")
cs_witer = csv.writer(f)

headers = {
    "referer":"http://price.cnveg.com/2024/",
"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0"
    }

lock = threading.Lock()

def download_one_page(url):
    resp = requests.get(url, headers=headers)
    resp.encoding = "utf-8"
    html = etree.HTML(resp.text)
    table = html.xpath("/html/body/div/table[6]/tr/td[2]/table[2]/tr[2]/td/table/tr[2]/td/table")[0]
    # 获取到每页的各种蔬菜的信息栏
    trs = table.xpath("./tr")
    with lock:
        for tr in trs:
            title1 = tr.xpath("./td/a/text()")[:2][0]
            title2 = tr.xpath("./td/a/text()")[:2][1]
            index = tr.xpath("./td/text()")
            low_price = tr.xpath("./td/text()")[0].strip("￥")
            hight_price = index[1].strip("￥")
            average_price = index[2].strip("￥")
            time = index[3].strip("￥")
            cs_witer.writerow([title1, title2,low_price,hight_price,average_price,time])
        print(url + "提取完成!")

if __name__ == '__main__':
    with ThreadPoolExecutor(50) as t:
        for i in range(1,6349):
            url = f"http://price.cnveg.com/2024/all/m7d-1cta-1by-1p{i}.html"
            t.submit(download_one_page, url)
    print("全部提取完毕!")

