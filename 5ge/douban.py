import re
import time
from DrissionPage import ChromiumPage, ChromiumOptions
from bs4 import BeautifulSoup
import pandas as pd
import re
co = ChromiumOptions().set_paths()
co.headless(True)
browser = ChromiumPage(co)

browser.get('https://movie.douban.com/subject/26849758/reviews?start=3920')
url = []
usernames = []
comment_times = []
comment_locations = []
comment_contents = []
res = browser.html
soup = BeautifulSoup(browser.html, 'lxml')
aa = browser.ele('@class:next').html
a = re.findall(r'<link rel="next" href="(.*?)">', str(aa), re.DOTALL)[0]
url.append(f'https://movie.douban.com/subject/26849758/reviews{a}')
print(f'https://movie.douban.com/subject/26849758/reviews{a}')
time.sleep(1)
soup = BeautifulSoup(browser.html, 'lxml')
ac = soup.find(attrs={'class': 'review-list'})
jj = re.findall(r'data-cid="(.*?)"', str(ac), re.DOTALL)
for i in jj:
    browser.ele(f'@id:toggle-{i}-copy').click(by_js=type)
    ll = browser.ele(f'@id:link-report-{i}').html
    pp = re.findall(r'class="review-content clearfix".*?>(.*?)</div>', ll, re.DOTALL)[0]
    soup1 = BeautifulSoup(pp, 'lxml')
    print(soup1.text.strip())
for i in range(10000):
    try:
        browser.ele('x://a[text()="后页>"]').click(by_js=type)
        time.sleep(1)
    except:
        print('jieshu')
        break
    res = browser.html
    soup = BeautifulSoup(browser.html, 'lxml')
    aa = browser.ele('@class:next').html
    try:
        a = re.findall(r'<link rel="next" href="(.*?)">', str(aa), re.DOTALL)[0]
    except:
        print('jie')
        continue
    url.append(f'https://movie.douban.com/subject/26849758/reviews{a}')
    print(f'https://movie.douban.com/subject/26849758/reviews{a}')
    time.sleep(1)
    soup = BeautifulSoup(browser.html, 'lxml')
    ac = soup.find(attrs={'class': 'review-list'})
    jj = re.findall(r'data-cid="(.*?)"', str(ac), re.DOTALL)
    for i in jj:
        browser.ele(f'@id:toggle-{i}-copy').click(by_js=type)
        ll = browser.ele(f'@id:link-report-{i}').html
        pp = re.findall(r'class="review-content clearfix".*?>(.*?)</div>', ll, re.DOTALL)[0]
        soup1 = BeautifulSoup(pp, 'lxml')
        comment_contents.append(soup1.text.strip())
        url.append(f'https://movie.douban.com/subject/26849758/reviews{a}')
        print(soup1.text.strip())


# df_shuju = pd.DataFrame(columns=["评论"])

# 将数据添加到DataFrame中
df_shuju = pd.DataFrame()  # 初始化一个空的DataFrame
for l in range(len(comment_contents)):
    row = {"content": comment_contents[l], "url": url[l]}
    df_shuju = pd.concat([df_shuju, pd.DataFrame([row])], ignore_index=True)

# 使用ExcelWriter以追加模式写入Excel文件
with pd.ExcelWriter("豆瓣.xlsx", mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
    # 如果Excel文件中已经存在DataFrame的sheet，则overlay选项会将新数据追加到现有sheet的下一行
    df_shuju.to_excel(writer, index=False, sheet_name='Sheet1', startrow=writer.sheets['Sheet1'].max_row)