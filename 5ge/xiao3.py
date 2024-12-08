import time
from DrissionPage import ChromiumPage, ChromiumOptions
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
from tqdm import tqdm
import proxy2
co = ChromiumOptions().set_paths()
co.set_local_port(9733)
# co.headless()
browser = ChromiumPage(co)
list1 = [
]
list3 = []
nj = 1
nl = 1
for kh, p_1 in zip(list1, tqdm(range(len(list1)), desc="线程1爬取进度")):
    browser.get("https://www.xiaohongshu.com/explore")
    try:
        browser.ele("@id:search-input").clear()
    except:
        while 1 < 2:
            if browser.ele('@class:active'):
                print("已过")
                break
            else:
                time.sleep(60)
                continue
    browser.ele("@id:search-input").input(kh)
    browser.ele("@class:search-icon").click(by_js=False)
    pinglun = []
    time.sleep(5)
    fg = 1
    for i in tqdm(range(50), desc=f"{kh}全爬取进度"):
        fg = fg + 1
        try:
            try:
                browser.scroll.to_bottom()
                time.sleep(0.3)
            except:
                print("url结束")
                break
            aa = browser.ele('@class:feeds-container').html
            soup = BeautifulSoup(aa, 'lxml')
            b = soup.findAll(attrs={"data-v-30d73e1a": ""})
            # print(b)
            ipl = re.findall(r'<a data-v-.*?="" href="(.*?)"', str(b), re.DOTALL)
            from collections import OrderedDict
            unique_urls = list(OrderedDict.fromkeys(ipl))

            difference1 = [x for x in unique_urls if x not in list3]
            # 打印去重后的URL列表
            # print(unique_urls)
            for ll, ou in zip(difference1, tqdm(range(len(difference1)), desc=f"{kh}爬取进度")):
                tag1 = browser.new_tab(f'https://www.xiaohongshu.com{ll}')
                try:
                    nl = 1
                    kk = tag1.ele('@class:note-text').html
                    soup6 = BeautifulSoup(kk, 'lxml')
                    print(soup6.text)
                    pinglun.append(soup6.text)
                    if tag1.ele('@class:no-comments-text'):
                        tag1.close()
                        continue
                    for i in range(500):
                        try:
                            tag1.ele('@class:note-scroller').scroll.to_bottom()
                        except:
                            break
                    jj = tag1.ele('@class:comments-container').html
                    soup7 = BeautifulSoup(jj, 'lxml')
                    con = re.findall(r'<div class="content" data-v-.*?="">(.*?)</div>', str(soup7), re.DOTALL)

                    for p in con:
                        soup8 = BeautifulSoup(p, 'lxml')
                        pinglun.append(soup8.text)
                        print(soup8.text)
                    list3.append(ll)
                    tag1.close()
                except:
                    nl = nl + 1
                    if nl % 5 == 0:
                        print('超过5')
                        time.sleep(600)
                    if tag1.ele('@class:text').text == '访问频次异常，请勿频繁操作':
                        browser.quit()
                        # proxy2.main()
                        co = ChromiumOptions().set_paths()
                        if nj == 1:
                            co.set_local_port(9734)
                            nj = 2
                        elif nj == 2:
                            co.set_local_port(9733)
                            nj = 3
                        else:
                            co.set_local_port(9732)
                            nj = 1
                        # co.headless()
                        browser = ChromiumPage(co)
                        browser.get("https://www.xiaohongshu.com/explore")
                        browser.ele("@id:search-input").clear()
                        browser.ele("@id:search-input").input(kh)
                        browser.ele("@class:search-icon").click(by_js=False)
                        print(f'第{fg}次循环')
                        for ml in range(fg):
                            try:
                                browser.scroll.to_bottom()
                                time.sleep(0.3)
                            except:
                                print("url结束")
                        continue
                    else:
                        tag1.close()
                        continue
        except:
            nj = 1
            while 1 < 2:
                browser.quit()
                co = ChromiumOptions().set_paths()
                if nj == 1:
                    co.set_local_port(9734)
                    nj = 2
                elif nj == 2:
                    co.set_local_port(9733)
                    nj = 3
                else:
                    co.set_local_port(9732)
                    nj = 1
                # co.headless()
                browser = ChromiumPage(co)
                browser.get("https://www.xiaohongshu.com/explore")
                try:
                    browser.ele("@id:search-input").clear()
                except:
                    if browser.ele('@class:active'):
                        print("已过")
                    else:
                        time.sleep(60)
                        continue
                browser.ele("@id:search-input").input(kh)
                browser.ele("@class:search-icon").click(by_js=False)
                break

    list2 = []
    t = 0
    for t in range(len(pinglun)):
        t += 1
        list2.append(str(t))

    file_path_1 = F'TOC/{kh}.xlsx'
    os.makedirs(os.path.dirname(file_path_1), exist_ok=True)
    dfs_empty = pd.DataFrame()
    dfs_empty.to_excel(file_path_1, index=False, header=False)
    # 将数据添加到DataFrame中
    df_shuju = pd.DataFrame()  # 初始化一个空的DataFrame
    for llp in range(len(pinglun)):
        row = {"序号": list2[llp], "正文": pinglun[llp]}
        df_shuju = pd.concat([df_shuju, pd.DataFrame([row])], ignore_index=True)

    # 使用ExcelWriter以追加模式写入Excel文件
    with pd.ExcelWriter(f"TOC/{kh}.xlsx", mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
        # 如果Excel文件中已经存在DataFrame的sheet，则overlay选项会将新数据追加到现有sheet的下一行
        df_shuju.to_excel(writer, index=False, sheet_name='Sheet1', startrow=writer.sheets['Sheet1'].max_row)