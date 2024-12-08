import time
from collections import OrderedDict
from DrissionPage import ChromiumPage, ChromiumOptions
from bs4 import BeautifulSoup
import re

def convert_time_to_seconds(time_str):
    minutes, seconds = map(int, time_str.split(':'))
    return minutes * 60 + seconds

list3 = []
co = ChromiumOptions().set_paths()
co.set_local_port(9521)
browser = ChromiumPage(co)
# browser.get("https://www.google.com/ncr")
browser.get("https://www.xiaohongshu.com/explore")
for j in range(30):
    soup = BeautifulSoup(browser.html, 'lxml')
    b = soup.findAll(attrs={"class": "title"})
    aa = re.findall(r'<span data-v-.*?="" data-v-.*?="">(.*?)</span>', str(b), re.DOTALL)
    print(aa)
    unique_urls = list(OrderedDict.fromkeys(aa))
    difference1 = [x for x in unique_urls if x not in list3]
    for i in difference1:
        time.sleep(1)
        list3.append(i)
        print(i)
        if '<img src=' in str(i):
            continue
        else:
            browser.ele(f'x://span[text()="{i}"]').click(by_js=True)
            if browser.ele('@class:no-comments-text'):
                browser.ele('@class:close-box').click(by_js=True)
                continue
            try:
                kk = re.findall(r'<span class="xgplayer-time-current">.*?</span><span>(.*?)</span>',
                                str(browser.ele('@class:xgplayer-time').html), re.DOTALL)
                print(convert_time_to_seconds(kk[0]))
            except:
                kk = ['00:00']
            if j % 1 == 0:
                try:
                    browser.ele('x://span[text()="关注"]').click(by_js=True)
                    try:
                        browser.ele('x://span[text()="说点什么..."]').input('受教了，谢谢美女')
                        browser.ele('x://button[text()="发送"]').click(by_js=True)
                    except:
                        print("未完成评论")
                    browser.ele('@@class:like-lottie@@style:width: 24px; height: 24px;').click(
                        by_js=True)
                except:
                    print('已关注')
            for k in range(300):
                browser.ele('@class:note-scroller').scroll.to_bottom()
                if browser.ele('@class:end-container'):
                    break
            time.sleep(convert_time_to_seconds(kk[0]))
            try:
                browser.ele('@class:close-box').click(by_js=True)
            except:
                continue
    browser.scroll.to_bottom()
    time.sleep(0.3)

