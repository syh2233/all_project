import re
import os
import requests
from bs4 import BeautifulSoup
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
        }
all_url=[

"https://www.aiweifulishe.net/dress/weddingdress/90341.html",
"https://www.aiweifulishe.net/cosplay/58298.html",
"https://www.aiweifulishe.net/cosplay/42524.html",
"https://www.aiweifulishe.net/dress/silkstocking/whitesilkstocking/84287.html",
"https://www.aiweifulishe.net/cosplay/game-cosplay/azurlane/80911.html",
"https://www.aiweifulishe.net/cosplay/comic-cosplay/fate/80266.html",
"https://www.aiweifulishe.net/dress/jk/79979.html",
"https://www.aiweifulishe.net/dress/silkstocking/whitesilkstocking/74631.html",
"https://www.aiweifulishe.net/cosplay/game-cosplay/azurlane/73806.html",
"https://www.aiweifulishe.net/dress/silkstocking/whitesilkstocking/73596.html",
"https://www.aiweifulishe.net/cosplay/game-cosplay/azurlane/71541.html",
"https://www.aiweifulishe.net/cosplay/70939.html",
"https://www.aiweifulishe.net/dress/silkstocking/whitesilkstocking/70631.html",
"https://www.aiweifulishe.net/cosplay/comic-cosplay/fate/70494.html",
"https://www.aiweifulishe.net/dress/weddingdress/67514.html",
"https://www.aiweifulishe.net/dress/silkstocking/whitesilkstocking/62897.html",
"https://www.aiweifulishe.net/dress/silkstocking/whitesilkstocking/62650.html",
"https://www.aiweifulishe.net/dress/weddingdress/62506.html",
"https://www.aiweifulishe.net/cosplay/61635.html",
"https://www.aiweifulishe.net/dress/weddingdress/60777.html",
"https://www.aiweifulishe.net/cosplay/comic-cosplay/fate/59860.html",
"https://www.aiweifulishe.net/cosplay/comic-cosplay/fate/59678.html",
"https://www.aiweifulishe.net/dress/weddingdress/58104.html",
"https://www.aiweifulishe.net/cosplay/game-cosplay/azurlane/57648.html",
"https://www.aiweifulishe.net/cosplay/game-cosplay/girlsfrontline/56839.html",
"https://www.aiweifulishe.net/cosplay/game-cosplay/azurlane/56764.html",
"https://www.aiweifulishe.net/cosplay/game-cosplay/arknights/55140.html",
"https://www.aiweifulishe.net/cosplay/53984.html",
"https://www.aiweifulishe.net/dress/silkstocking/whitesilkstocking/51927.html",
"https://www.aiweifulishe.net/dress/weddingdress/50524.html",
"https://www.aiweifulishe.net/cosplay/game-cosplay/azurlane/48395.html",
"https://www.aiweifulishe.net/dress/weddingdress/48038.html",
"https://www.aiweifulishe.net/dress/weddingdress/47666.html",
"https://www.aiweifulishe.net/dress/weddingdress/47284.html",
"https://www.aiweifulishe.net/dress/silkstocking/whitesilkstocking/47282.html",
"https://www.aiweifulishe.net/dress/weddingdress/46303.html",
"https://www.aiweifulishe.net/dress/weddingdress/45253.html",
"https://www.aiweifulishe.net/cosplay/game-cosplay/kancolle/44316.html",
"https://www.aiweifulishe.net/whfl/43845.html",
"https://www.aiweifulishe.net/dress/silkstocking/blacksilkstocking/43778.html",
"https://www.aiweifulishe.net/whfl/43419.html",
"https://www.aiweifulishe.net/whfl/42245.html",
"https://www.aiweifulishe.net/whfl/41941.html",
"https://www.aiweifulishe.net/whfl/41697.html",
]
list = []
for j in range(5000):
    list.append(j)
for kk, l in zip(all_url, list):
    con = requests.get(kk, headers=headers)
    img = re.findall(r'<img decoding="async".*?src="(.*?)"', con.text, re.DOTALL)
    for i, p in zip(img, list):
        try:
            response = requests.get(i, headers=headers)
            file_path = f'E:/AI/video_new/{l}_{p}.jpg'
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            if response.status_code == 200:
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                print(f'图片下载完成,{i}')
            else:
                print('图片下载失败，状态码：', response.status_code)
        except:
            print(l, f'{i}')
            continue