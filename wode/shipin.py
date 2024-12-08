import re
import os
import requests
from DrissionPage import ChromiumPage, ChromiumOptions
browser = ChromiumPage()
browser.get('https://aibpkr97623.aikeqa51517ai.cc:18988/#/ai-tab5')
browser.wait(3)
# browser.ele('@class:q-tab relative-position self-stretch flex flex-center text-center q-tab--inactive q-focusable q-hoverable cursor-pointer custom-tab custom-inactive-tab').click(by_js=type)
a = browser.ele('@class:list-wrap').html
# print(a)
res = re.findall(r'<img.*?src="https://ai2-res.s3.ap-southeast-1.amazonaws.com/uploads/(.*?)\..*?" style=', a, re.DOTALL)
list = []
for j in range(3000):
    list.append(j)
for i, l in zip(res, list):
    try:
        response = requests.get('https://ai2-res.s3.ap-southeast-1.amazonaws.com/uploads/' + str(i) + '.gif', stream=True)
        if response.status_code == 200:
            # 打开一个本地文件用于写入
            with open('pic\\' + str(l) + '.mp4', 'wb') as file:
                # 写入视频数据
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print('视频下载完成,https://ai2-res.s3.ap-southeast-1.amazonaws.com/uploads/' + str(i) + '.gif')
        else:
            print('视频下载失败，状态码：', response.status_code)
    except:
        print(l, 'https://ai2-res.s3.ap-southeast-1.amazonaws.com/uploads/' + str(i) + '.gif')
        continue