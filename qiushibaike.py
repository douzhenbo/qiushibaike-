import requests
from bs4 import BeautifulSoup
import pymongo


def get_page(url):
    headers={'User-Agent':'Mozilla/5.0'}
    r=requests.get(url,headers=headers)
    if r.status_code==200:
        print('爬取成功')
        return r.text
    else:
        print('爬取失败')

def save_to_mongo(string):
    client=pymongo.MongoClient(host='localhost')
    db=client.qiushi
    table=db.xiaohua
    xiaohua={'xiaohua':string}
    table.insert_one(xiaohua)

def get_information(html):
    soup=BeautifulSoup(html,'lxml')
    items=soup.find_all(attrs={'class':'content'})
    for item in items:
        link=item.find_all('span')
        if link[0].string is not None:
            save_to_mongo(link[0].string)



def show_from_mongo():
    client = pymongo.MongoClient(host='localhost')
    db = client.qiushi
    table = db.xiaohua
    informations=table.find()
    for information in informations:
        print(information.get('xiaohua'))

def main():
    for offset in range(1,20):
        url = 'https://www.qiushibaike.com/8hr/page/str(offset)/'
        html=get_page(url)
        get_information(html)
        show_from_mongo()

main()