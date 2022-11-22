# coding=utf-8
from bs4 import BeautifulSoup
import requests
import sys
import random
import pymysql
links = []
datas = []
hea = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'
}
urls =[
    "https://www.chinanews.com/china.shtml", #国内
    "https://www.chinanews.com/society.shtml", #社会
    "https://www.chinanews.com/compatriot.shtml",#港澳
    "https://www.chinanews.com/wenhua.shtml",#文化
    "https://www.chinanews.com/world.shtml",#国际
    "https://www.chinanews.com/cj/gd.shtml",#财经
    "https://www.chinanews.com/sports.shtml",#体育
    "https://www.chinanews.com/huaren.shtml"  #华人
]
# 打开数据库连接
db = pymysql.connect(host='127.0.0.1', user='root', password='123456', port=3396, db='news_recommendation_system')
# 使用cursor()方法获取操作游标
cursor = db.cursor()

def main():
    #reload(sys)
    #sys.setdefaultencoding("utf-8")
    #baseurl = 'https://www.chinanews.com/taiwan.shtml'  # 要爬取的网页链接
    baseurl = 'https://www.chinanews.com/taiwan.shtml'  # 要爬取的网页链接
    # deleteDate()
    # 1.爬取主网页获取各个链接
    getLink(baseurl)
    # 2.根据链接爬取内部信息并且保存数据到数据库
    getInformationAndSave()
    # 3.关闭数据库
    db.close()

def getInformationAndSave():
    for link in links:
        data = []
        url = "https://www.chinanews.com" + link[1]
        cur_html = requests.get(url, headers=hea)
        cur_html.encoding = "utf8"
        soup = BeautifulSoup(cur_html.text, 'html.parser')
        # 获取时间
        title = soup.find('h1')
        title = title.text.strip()
        # 获取时间和来源
        tr = soup.find('div', class_='left-t').text.split()
        time = tr[0] + tr[1]
        recourse = tr[2]
        # 获取内容
        cont = soup.find('div', class_="left_zw")
        content = cont.text.strip()
        print(link[0] + "---" + title + "---" + time + "---" + recourse + "---" + url)
        saveDate(title,content,time,recourse,url)

def deleteDate():
    sql = "DELETE FROM news "
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交修改
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()

def saveDate(title,content,time,recourse,url):
    try:
        cursor.execute("INSERT INTO news(news_title, news_content, type_id, news_creatTime, news_recourse,news_link) VALUES ('%s', '%s', '%s', '%s', '%s' ,'%s')" % \
          (title, content, random.randint(1,8), time, recourse,url))
        db.commit()
        print("执行成功")
    except:
        db.rollback()
        print("执行失败")

def getLink(baseurl):
    html = requests.get(baseurl, headers=hea)
    html.encoding = 'utf8'
    soup = BeautifulSoup(html.text, 'html.parser')
    for item in soup.select('div.content_list > ul > li'):
        # 对不符合的数据进行清洗
        if (item.a == None):
            continue
        data = []
        type = item.div.text[1:3]  # 类型
        link = item.div.next_sibling.next_sibling.a['href']
        data.append(type)
        data.append(link)
        links.append(data)

if __name__ == '__main__':
    main()


