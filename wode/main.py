
import re
import time
from DrissionPage import ChromiumPage, ChromiumOptions
browser = ChromiumPage()
browser.get('https://caixukun9.vip/image?agentCode=DQ0PG4TK')
browser.ele('@class:btn-close').click(by_js=type)
# for i in range(7):
browser.listen.start('https://htxjy1.com/system/')
# url_list = []
for i in range(200):
    resp = browser.listen.wait()  # 确保listen.wait()是正确的调用方式
    print(resp.url)
    text = resp.response.body
    with open('temp_image' + str(i) + '.jpg', 'wb') as file:
        file.write(text)