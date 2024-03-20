import requests

# data bank: https://api.bilibili.com/x/space/wbi/arc/search?
# send request
# retrieve
# decode data
# save data

#1 send request:
# mimic browser, request site, send request

headers = {
    'Cookie': "buvid3=F3C5B539-8C3C-080D-D2DD-7FF8F219DB0E84360infoc; b_nut=1709726484; b_lsid=79587846_18E13A3CC38; _uuid=71041012AE-D1019-D77D-4B8F-1643647A26D285569infoc; buvid4=44BE78E1-D598-6BDD-A636-B9CFB0CE43CB85482-024030612-7R2wxhHKeTm9GiNyV7r7jQ%3D%3D; SESSDATA=2db2457d%2C1725278671%2C436db%2A31CjCv0whKk3dBMmptuoI9jDIe6W0LqVVSrWJb6ToIdR3s-GmIK51jsFSxQ3X-8IZYmuwSVmNndUpyT1NuMXdSdDM4bjl2cXFLSTR1UUFfQ0tmODJyQmt5VU9aZGhkUk8xazlVdHQweEs5QVdlTUFNT1JwVXVFbUJWdmhReUs1Q040UmppVXN4T0RnIIEC; bili_jct=2abadeb3d64a4e60c725f0e0cffc0d6b; DedeUserID=3537114876611270; DedeUserID__ckMd5=045d6db1038a9617; fingerprint=03bc2633e888116274abaa7f374b1884; buvid_fp_plain=undefined; CURRENT_FNVAL=4048; buvid_fp=03bc2633e888116274abaa7f374b1884; rpdid=|(umm~YY)Rk|0J'u~|m~k~J)J; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDk5ODgwMjMsImlhdCI6MTcwOTcyODc2MywicGx0IjotMX0.wuwPS0pJMstdhKJVjA8T8nyAhNaI7ol4_dKFkIkCtcM; bili_ticket_expires=1709987963; sid=7d73ng8f",
    # User-Agent: browser information
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

# request url
url = f'https://api.bilibili.com/x/space/wbi/arc/search'
# request data
data = {
    "mid": "50101698",
    "pn": "1",
    "ps": "25",
    "index": "1",
    "order": "pubdate",
    "order_avoided": "true",
    "platform": "web",
    "web_location": "1550101",
    "dm_img_list": '''[{"x":754,"y":-137,"z":0,"timestamp":12,"k":112,"type":0},{"x":833,"y":15,"z":67,"timestamp":99,"k":60,"type":0},{"x":859,"y":26,"z":23,"timestamp":425,"k":124,"type":0},{"x":1033,"y":311,"z":163,"timestamp":568,"k":62,"type":0},{"x":889,"y":198,"z":18,"timestamp":674,"k":97,"type":0}]''',
    "dm_img_str": "V2ViR0wgMS4wIChPcGVuR0wgRVMgMi4wIENocm9taXVtKQ",
    "dm_cover_img_str": "QU5HTEUgKE5WSURJQSwgTlZJRElBIEdlRm9yY2UgUlRYIDQwNjAgKDB4MDAwMDI4ODIpIERpcmVjdDNEMTEgdnNfNV8wIHBzXzVfMCwgRDNEMTEpR29vZ2xlIEluYy4gKE5WSURJQS",
    "dm_img_inter": '''{"ds":[{"t":0,"c":"","p":[183,61,61],"s":[256,6505,7044]}],"wh":[4581,7477,67],"of":[338,676,338]}''',
    "w_rid": "75ed34e63650dcedcd58a94deba2f49b",
    "wts": "1709728886",
}

response = requests.get(url=url, params=data, headers=headers)
if response.status_code == 200:
    json = response.json()
    print(json)
