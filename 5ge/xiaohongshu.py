import time
from DrissionPage import ChromiumPage, ChromiumOptions
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
from tqdm import tqdm
co = ChromiumOptions().set_paths()
co.set_local_port(9357)
# co.headless()
browser = ChromiumPage(co)

browser.get("https://www.zhihu.com/")

list = [

]
value = []
pinglun = []
browser.get('https://www.xiaohongshu.com/search_result?keyword=%25E9%2595%25BF%25E5%25AE%2589%25E5%258D%2581%25E4%25BA%258C%25E6%2597%25B6%25E8%25BE%25B0&source=unknown&type=51')
time.sleep(5)
for i in range(3000):
    try:
        try:
            browser.scroll.to_bottom()
        except:
            print("url结束")
            break
        aa = browser.ele('@class:feeds-container').html
        soup = BeautifulSoup(aa, 'lxml')
        b = soup.findAll(attrs={"data-v-30d73e1a": ""})
        i = re.findall(r'<a data-v-30d73e1a="" href="(.*?)"', str(b), re.DOTALL)
        from collections import OrderedDict
        unique_urls = list(OrderedDict.fromkeys(i))

        # 打印去重后的URL列表
        print(unique_urls)
        for ll in unique_urls:
            tag = browser.new_tab(f'https://www.xiaohongshu.com{ll}')
            try:
                kk = tag.ele('@class:note-text').html
                soup6 = BeautifulSoup(kk, 'lxml')
                print(soup6.text)
                jj = tag.ele('@class:comments-container').html
                soup7 = BeautifulSoup(jj, 'lxml')
                con = re.findall(r'<div class="content" data-v-58b5f025="">(.*?)</div>', str(soup7), re.DOTALL)
                pinglun.append(soup6.text)
                for p in con:
                    soup8 = BeautifulSoup(p, 'lxml')
                    pinglun.append(soup8.text)

                    print(soup8.text)
                tag.close()
                continue
            except:
                tag.close()
                break
    except:
        break


# 将数据添加到DataFrame中
df_shuju = pd.DataFrame()  # 初始化一个空的DataFrame
for l in range(len(value)):
    row = {"url": value[l], "正文": pinglun[l]}
    df_shuju = pd.concat([df_shuju, pd.DataFrame([row])], ignore_index=True)

# 使用ExcelWriter以追加模式写入Excel文件
with pd.ExcelWriter("小红书.xlsx", mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
    # 如果Excel文件中已经存在DataFrame的sheet，则overlay选项会将新数据追加到现有sheet的下一行
    df_shuju.to_excel(writer, index=False, sheet_name='Sheet1', startrow=writer.sheets['Sheet1'].max_row)