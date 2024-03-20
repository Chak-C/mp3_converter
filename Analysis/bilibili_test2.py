import requests, json
from bs4 import BeautifulSoup

table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
tr = {}
for i in range(58):
    tr[table[i]] = i
s = [11, 10, 3, 8, 4, 6]
xor = 177451812
add = 8728348608

def bv2av(x):
    r = 0
    for i in range(6):
        r += tr[x[s[i]]] * 58 ** i
    return (r - add) ^ xor

def get_aid(bvid):
    if 'BV' in bvid:
        return bv2av(bvid)
    else:
        return bvid
    
print(get_aid('BV1gm4y1G74K'))

def get_title_time_tag(bvid):
    tag_lst = []
    url = f'https://www.bilibili.com/video/{bvid}'
    content = requests.get(url).content
    soup = BeautifulSoup(content, 'html.parser')
    print(soup)
    tags = soup.find_all('a',class_='tag-link')
    title_lst = soup.find_all('title')
    title = title_lst[0].text.split('_')[0]
    time_lst = soup.find_all(itemprop='uploadDate')
    time = time_lst[0]['content'].split(' ')[0]
    for tag in tags:
        tag_lst.append(tag.text.strip())
    return title,time,set(tag_lst)

print(get_title_time_tag('BV1gm4y1G74Kid'))
url = f'https://www.bilibili.com/video/BV1gm4y1G74Kid'
content = requests.get(url).content
soup = BeautifulSoup(content, 'html.parser')
print(soup)
print(content)