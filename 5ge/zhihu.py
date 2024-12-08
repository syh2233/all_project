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
for e, no5 in zip(list, tqdm(range(len(list)), desc="线程1爬取进度")):
    try:
        browser.ele("@class:Input i7cW1UcwT6ThdhTakqFm").clear()
    except:
        browser.quit()
        co = ChromiumOptions().set_paths()
        co.set_local_port(9338)
        # co.headless()
        browser = ChromiumPage(co)
        browser.get("https://www.zhihu.com/")
        browser.ele("@class:Input i7cW1UcwT6ThdhTakqFm").clear()
    browser.ele("@class:Input i7cW1UcwT6ThdhTakqFm").input(e)
    try:
        browser.ele("@class:ZDI ZDI--Search24 SearchBar-searchIcon isFocus hasValue css-1dlt5yv").click(by_js=False)
    except:
        browser.ele("@class:Button SearchBar-searchButton FEfUrdfMIKpQDJDqkjte Button--primary Button--blue epMJl0lFQuYbC7jrwr_o JmYzaky7MEPMFcJDLNMG").click(by_js=False)

    list1 = []
    time.sleep(2)
    aaa = None
    for i in range(300):
        try:
            browser.ele('x://button[text()="阅读全文"]').click(by_js=False)
            browser.scroll.to_bottom()
        except:
            print("yijishu")
            break
    while 1 < 2:
        try:
            soup = BeautifulSoup(browser.html, 'lxml')
            break
        except:
            browser.quit()
            co = ChromiumOptions().set_paths()
            co.set_local_port(9357)
            # co.headless()
            browser = ChromiumPage(co)
            browser.get("https://www.zhihu.com/")
            browser.ele("@class:Input i7cW1UcwT6ThdhTakqFm").clear()
            browser.ele("@class:Input i7cW1UcwT6ThdhTakqFm").input(e)
            try:
                browser.ele("@class:ZDI ZDI--Search24 SearchBar-searchIcon isFocus hasValue css-1dlt5yv").click(
                    by_js=False)
            except:
                browser.ele(
                    "@class:Button SearchBar-searchButton FEfUrdfMIKpQDJDqkjte Button--primary Button--blue epMJl0lFQuYbC7jrwr_o JmYzaky7MEPMFcJDLNMG").click(
                    by_js=False)
            for i in range(300):
                try:
                    browser.ele('x://button[text()="阅读全文"]').click(by_js=False)

                except:
                    print("yijishu")
                    break
            continue
    table = re.findall(r'data-za-detail-view-id="(.*?)"', browser.html, re.DOTALL)
    aa = soup.findAll(attrs={'data-za-detail-view-id': f'{table[1]}'})
    bb = soup.findAll(attrs={'class': 'Highlight'})
    soup1 = BeautifulSoup(str(aa), 'lxml')
    # print(soup1.text)
    text = browser.ele('@class:ListShortcut').html
    soup3 = BeautifulSoup(text, 'lxml')
    text1 = soup3.findAll(attrs={'itemprop': 'text'})
    for pp, jj in zip(text1, bb):
        soup5 = BeautifulSoup(str(jj), 'lxml')
        list1.append(f'{soup5.text}: {pp.text.lstrip(" ")}')
        print(f'{soup5.text}: {pp.text.lstrip(" ")}')
    soup = BeautifulSoup(browser.html, 'lxml')
    a = soup.findAll(attrs={
        'class': 'Button ContentItem-action FEfUrdfMIKpQDJDqkjte Button--plain Button--withIcon Button--withLabel fEPKGkUK5jyc4fUuT0QP B46v1Ak6Gj5sL2JTS4PY RuuQ6TOh2cRzJr6WlyQp'})

    for o, no in zip(a, tqdm(range(len(a)), desc=f"{e}爬取进度")):
        AA = re.findall(r'</span>(.*?)</button>', str(o), re.DOTALL)
        if AA[0] == '收藏' or AA[0] == '喜欢' or AA[0] == '添加评论' or AA[0] == '写回答':
            continue
        print(AA)
        try:
            browser.ele(f'text={AA[0]}').click(by_js=True)
        except:
            continue
        try:
            browser.ele('text:点击查看全部评论').click(by_js=False)
        except:
            time.sleep(0.3)
        for j in range(30):
            try:
                browser.ele('@class:css-34podr').scroll.to_bottom()
                time.sleep(1)
            except:
                break
        while 1 < 2:
            try:
                soup = BeautifulSoup(browser.html, 'lxml')
                break
            except:
                browser.quit()
                co = ChromiumOptions().set_paths()
                co.set_local_port(9357)
                # co.headless()
                browser = ChromiumPage(co)
                browser.get("https://www.zhihu.com/")
                browser.ele("@class:Input i7cW1UcwT6ThdhTakqFm").clear()
                browser.ele("@class:Input i7cW1UcwT6ThdhTakqFm").input(e)
                try:
                    browser.ele("@class:ZDI ZDI--Search24 SearchBar-searchIcon isFocus hasValue css-1dlt5yv").click(
                        by_js=False)
                except:
                    browser.ele(
                        "@class:Button SearchBar-searchButton FEfUrdfMIKpQDJDqkjte Button--primary Button--blue epMJl0lFQuYbC7jrwr_o JmYzaky7MEPMFcJDLNMG").click(
                        by_js=False)
                for i in range(300):
                    try:
                        browser.ele('x://button[text()="阅读全文"]').click(by_js=False)

                    except:
                        print("yijishu")
                        break
                continue
        cont = soup.findAll(attrs={'class': 'CommentContent css-1jpzztt'})
        for u in cont:
            print(f"{u.text}")
            list1.append(u.text)
        # time.sleep(1)
        try:
            browser.ele('@class:Zi Zi--Close css-k6n6wr').click(by_js=False)
        except:
            time.sleep(0.3)
        try:
            browser.ele('x://button[text()="收起评论"]').click(by_js=True)
        except:
            time.sleep(0.3)

    list2 = []
    t = 0
    for t in range(len(list1)):
        t += 1
        list2.append(str(t))

    file_path_1 = F'TOC/{e}.xlsx'
    os.makedirs(os.path.dirname(file_path_1), exist_ok=True)
    dfs_empty = pd.DataFrame()
    dfs_empty.to_excel(file_path_1, index=False, header=False)
    # 将数据添加到DataFrame中
    df_shuju = pd.DataFrame()  # 初始化一个空的DataFrame
    for l in range(len(list1)):
        row = {"序号": list2[l], "正文": list1[l]}
        df_shuju = pd.concat([df_shuju, pd.DataFrame([row])], ignore_index=True)

    # 使用ExcelWriter以追加模式写入Excel文件
    with pd.ExcelWriter(f"TOC/{e}.xlsx", mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
        # 如果Excel文件中已经存在DataFrame的sheet，则overlay选项会将新数据追加到现有sheet的下一行
        df_shuju.to_excel(writer, index=False, sheet_name='Sheet1', startrow=writer.sheets['Sheet1'].max_row)
