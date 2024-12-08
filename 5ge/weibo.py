import time

from DrissionPage import ChromiumPage, ChromiumOptions
from bs4 import BeautifulSoup
import pandas as pd
co = ChromiumOptions().set_paths()
co.headless(True)
co.set_local_port(9333)
co.add_extension(r'C:\Users\沈家\Downloads\proxy_switchyomega-2.5.20-an+fx')
browser = ChromiumPage(co)
value = []
browser.get('https://s.weibo.com/weibo?q=%E9%95%BF%E5%AE%89%E5%8D%81%E4%BA%8C%E6%97%B6%E8%BE%B0')
a = browser.html
soup = BeautifulSoup(a, 'lxml')
t = soup.findAll(attrs={'node-type': 'feed_list_content'})
b = soup.findAll(attrs={'node-type': 'feed_list_content_full'})
for i, j in zip(t, b):
    print(i.text)
    print(j.text)
    value.append(i.text)
    value.append(j.text)


for url in range(50000):
    try:
        time.sleep(2)
        browser.ele('x://a[text()="下一页"]').click(by_js=type)
    except:
        print("结束")
        break
    try:
        soup = BeautifulSoup(browser.html, 'lxml')
        t = soup.findAll(attrs={'node-type': 'feed_list_content'})
        b = soup.findAll(attrs={'node-type': 'feed_list_content_full'})
        for i, j in zip(t, b):
            print(i.text.strip())
            print(j.text.strip())
            value.append(i.text.strip())
            value.append(j.text.strip())
    except:
        print("结束")
        continue


df_shuju = pd.DataFrame(columns=["评论"])

# 将数据添加到DataFrame中
# df_shuju = pd.DataFrame()  # 初始化一个空的DataFrame
for l in range(len(value)):
    row = {"评论": value[l]}
    df_shuju = pd.concat([df_shuju, pd.DataFrame([row])], ignore_index=True)

# 使用ExcelWriter以追加模式写入Excel文件
with pd.ExcelWriter("微博.xlsx", mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
    # 如果Excel文件中已经存在DataFrame的sheet，则overlay选项会将新数据追加到现有sheet的下一行
    df_shuju.to_excel(writer, index=False, sheet_name='Sheet1', startrow=writer.sheets['Sheet1'].max_row)