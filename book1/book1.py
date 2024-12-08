import re
import os
import time

from tqdm import tqdm
from bs4 import BeautifulSoup
from DrissionPage import ChromiumPage, ChromiumOptions
import proxy
import pandas as pd
import proxy2

def name(df):
    with pd.ExcelWriter('name.xlsx', engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
        if 'Sheet1' in writer.sheets:
            startrow = writer.sheets['Sheet1'].max_row + 1
        else:
            startrow = 0  # 如果工作表不存在，从第0行开始写入
        df.to_excel(writer, index=False, header=False, sheet_name='Sheet1', startrow=startrow)

def shujia(df, file_path):
    with pd.ExcelWriter(f'线程书架/{file_path}', engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
        if 'Sheet1' in writer.sheets:
            startrow = writer.sheets['Sheet1'].max_row + 1
        else:
            startrow = 0  # 如果工作表不存在，从第0行开始写入
        df.to_excel(writer, columns=['Column2'], index=False, header=False, sheet_name='Sheet1', startrow=startrow)

def book(url):
    url, colist = url.split("|")
    colist = int(colist)
    co = ChromiumOptions().set_paths()
    # co.headless()
    co.set_argument('--window-size', '80,60')
    co.set_timeouts(6, 6, 6)
    if colist == 1:
        co.set_local_port(9345)
        co.add_extension(r'proxy_switchyomega-2.5.20-an+fx')
        proxy.browser1 = ChromiumPage(co)
    elif colist == 2:
        co.set_local_port(9334)
        co.add_extension(r'proxy_switchyomega-2.5.20-an+fx')
        proxy.browser2 = ChromiumPage(co)
    elif colist == 3:
        co.set_local_port(9335)
        co.add_extension(r'proxy_switchyomega-2.5.20-an+fx')
        proxy.browser3 = ChromiumPage(co)
    elif colist == 4:
        co.set_local_port(9336)
        co.add_extension(r'proxy_switchyomega-2.5.20-an+fx')
        proxy.browser4 = ChromiumPage(co)
    elif colist == 5:
        co.set_local_port(9337)
        co.add_extension(r'proxy_switchyomega-2.5.20-an+fx')
        proxy.browser5 = ChromiumPage(co)
    elif colist == 6:
        co.set_local_port(9338)
        co.add_extension(r'proxy_switchyomega-2.5.20-an+fx')
        proxy.browser6 = ChromiumPage(co)
    elif colist == 7:
        co.set_local_port(9339)
        co.add_extension(r'proxy_switchyomega-2.5.20-an+fx')
        proxy.browser7 = ChromiumPage(co)
    elif colist == 8:
        co.set_local_port(9340)
        co.add_extension(r'proxy_switchyomega-2.5.20-an+fx')
        proxy.browser8 = ChromiumPage(co)
    elif colist == 9:
        co.set_local_port(9341)
        co.add_extension(r'proxy_switchyomega-2.5.20-an+fx')
        proxy.browser9 = ChromiumPage(co)
    elif colist == 10:
        co.set_local_port(9342)
        co.set_argument('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36')
        # co.set_argument('--no-sandbox')
        co.add_extension(r'proxy_switchyomega-2.5.20-an+fx')
        proxy.browser10 = ChromiumPage(co)

    if colist == 1:
        proxy.browser1.get(url, retry=1)
        proxy.browser1.wait(30)
        for i in range(15):
            if proxy.browser1.ele('x//*[text="确认您是真人"]'):
                proxy.browser1.ele('x//*[text="确认您是真人"]').click()
            elif proxy.browser1.ele('x//input[@value="Verify you are human"]'):
                proxy.browser1.ele('x//input[@value="Verify you are human"]').click()
            else:
                break
        proxy.browser1.wait(5)
        max1 = 50
        mini1 = 1
        while mini1 < max1:
            book_url1 = re.findall(r'class="in-lable trans-bg-black"><a href="(.*?)">', proxy.browser1.html, re.DOTALL)
            if book_url1 == []:
                print(book_url1)
                proxy.browser1.quit()
                co.set_argument('--window-size', '80,60')
                co.set_local_port(9345)
                co.add_extension(r'proxy_switchyomega-2.5.20-an+fx')
                proxy.browser1 = ChromiumPage(co)
                proxy2.main()
                proxy.browser1.get(url, retry=1)
                proxy.browser1.wait(30)
                for i in range(15):
                    if proxy.browser1.ele('x//*[text="确认您是真人"]'):
                        proxy.browser1.ele('x//*[text="确认您是真人"]').click()
                    elif proxy.browser1.ele('x//input[@value="Verify you are human"]'):
                        proxy.browser1.ele('x//input[@value="Verify you are human"]').click()
                    else:
                        break
                proxy.browser1.wait(2)
            else:
                break
        dfs1 = pd.read_excel('线程书架/线程1.xlsx', usecols=[0], header=None)
        try:
            url_list1 = dfs1.iloc[:, 0].tolist()
            difference1 = [x for x in book_url1 if x not in url_list1]
        except:
            difference1 = book_url1
        for i_1, no1 in zip(difference1, tqdm(range(len(difference1)), desc="线程1爬取进度")):
            tab1 = proxy.browser1.new_tab()
            while 1 < 5:
                tab1.get(i_1)
                soup1 = BeautifulSoup(tab1.html, 'lxml')
                book_temp1 = soup1.find(attrs={'class': 'list-body'})
                book_name_url1 = re.findall(r'href="(.*?)"', str(book_temp1), re.DOTALL)
                book_name1 = soup1.find(attrs={'style': 'font-size:20px'})
                if book_name1 is None:
                    proxy2.main()
                    proxy.browser1.wait(8)
                    continue
                else:
                    df1 = pd.DataFrame({
                        'Column1': [book_name1.text.strip()],
                        'Column2': [i_1]
                    })
                    print(book_name1.text.strip())
                    break
            file_path_1 = f'TOC/{book_name1.text.replace(":", ".").replace("?", "").replace("？", "").replace("?", "").strip()}.xlsx'
            if os.path.exists(file_path_1):
                try:
                    dfs_1 = pd.read_excel(file_path_1, usecols=[0], header=None)
                except:
                    pass
            else:
                os.makedirs(os.path.dirname(file_path_1), exist_ok=True)
                dfs_empty = pd.DataFrame()
                dfs_empty.to_excel(file_path_1, index=False, header=False)
            try:
                url_list_1 = dfs_1.iloc[:, 0].tolist()
                print(url_list_1)
                difference_1 = [x for x in book_name_url1 if x not in url_list_1]
                if len(difference_1) == len(book_name_url1):
                    difference_1 = []
                else:
                    print(difference_1)
            except:
                difference_1 = book_name_url1
            for j_1 in difference_1:
                while mini1 < max1:
                    try:
                        tab1 = proxy.browser1.new_tab()
                        tab1.get(j_1)
                        soup_1 = BeautifulSoup(tab1.html, 'lxml')
                        book_temp_1 = soup_1.find(attrs={'itemprop': 'articleBody'})
                        book_name_con1 = soup_1.find(attrs={'class': 'toon-title'})
                        if book_name_con1 is None:
                            proxy2.main()
                            continue
                        else:
                            aname_1 = book_name_con1.text.replace("/", ".").replace(":", ".").replace("?", "").replace(
                                "<", "").strip()
                            tab1.close()
                            print(aname_1)
                        book_con1 = \
                            re.findall('<div class="view-img">\n</div>\n<div class=".*?">(.*?)</div>', str(book_temp_1),
                                       re.DOTALL)[
                                0]
                        soup__1 = BeautifulSoup(book_con1, 'lxml')
                        soup__1_ = soup__1.find_all('p')
                        break
                    except:
                        proxy.browser1.quit()
                        co.set_argument('--window-size', '80,60')
                        co.set_local_port(9345)
                        co.add_extension(r'proxy_switchyomega-2.5.20-an+fx')
                        proxy.browser1 = ChromiumPage(co)
                        proxy2.main()
                        proxy.browser1.get(url, retry=1)
                        proxy.browser1.wait(30)
                        for i in range(15):
                            if proxy.browser1.ele('x//*[text="确认您是真人"]'):
                                proxy.browser1.ele('x//*[text="确认您是真人"]').click()
                            elif proxy.browser1.ele('x//input[@value="Verify you are human"]'):
                                proxy.browser1.ele('x//input[@value="Verify you are human"]').click()
                            else:
                                break
                        proxy.browser1.wait(5)

                file_path1 = f'book_all/{book_name1.text.replace(":", ".").replace("?", "").replace("？", "").strip()}/{aname_1}.txt'
                os.makedirs(os.path.dirname(file_path1), exist_ok=True)
                with open(file_path1, 'a', encoding='utf-8') as file:
                    for soup2_1 in soup__1_:
                        file.write(f'{soup2_1.get_text()}\n')
                dfsj1 = pd.DataFrame({
                    'Column1': [j_1],
                    'Column2': [aname_1]
                })
                with pd.ExcelWriter(file_path_1, engine='openpyxl', mode='a',
                                    if_sheet_exists='overlay') as writer:
                    if 'Sheet1' in writer.sheets:
                        startrow = writer.sheets['Sheet1'].max_row + 1
                    else:
                        startrow = 0  # 如果工作表不存在，从第0行开始写入
                    dfsj1.to_excel(writer, index=False, header=False, engine='openpyxl', sheet_name='Sheet1', startrow=startrow)
                print(f'book_all/{book_name1.text.replace(":", ".").replace("?", "").replace("？", "").strip()}/{aname_1}.txt,已下载')
            name(df=df1)
            shujia(df1, file_path='线程1.xlsx')
            tab1.close()
    elif colist == 2:
        proxy.browser2.get(url, retry=1)
        proxy.browser2.wait(30)
        for i in range(15):
            if proxy.browser2.ele('x//*[text="确认您是真人"]'):
                proxy.browser2.ele('x//*[text="确认您是真人"]').click()
                print('q')
            elif proxy.browser2.ele('x//input[@value="Verify you are human"]'):
                proxy.browser2.ele('x//input[@value="Verify you are human"]').click
                print('h')
            else:
                break
        proxy.browser2.wait(5)
        max2 = 100
        mini2 = 1
        while mini2 < max2:
            try:
                book_url2 = re.findall(r'class="in-lable trans-bg-black"><a href="(.*?)">', proxy.browser2.html,
                                       re.DOTALL)
                if book_url2 == []:
                    print(book_url2)
                    proxy.browser2.quit()
                    co.set_argument('--window-size', '80,60')
                    co.set_local_port(9339)
                    co.add_extension(r'proxy_switchyomega-2.5.20-an+fx')
                    proxy.browser2 = ChromiumPage(co)

                    proxy.browser2.get(url, retry=1)
                    proxy.browser2.wait(30)
                    for i in range(15):
                        if proxy.browser8.ele('x//*[text="确认您是真人"]'):
                            proxy.browser8.ele('x//*[text="确认您是真人"]').click()
                            print('q')
                        elif proxy.browser8.ele('x//input[@value="Verify you are human"]'):
                            proxy.browser8.ele('x//input[@value="Verify you are human"]').click
                            print('h')
                        else:
                            break
                    proxy.browser2.wait(5)
                else:
                    break
            except:
                proxy.browser2.quit()
                co.set_argument('--window-size', '80,60')
                co.set_local_port(9339)
                co.add_extension(r'proxy_switchyomega-2.5.20-an+fx')
                proxy.browser2 = ChromiumPage(co)

                proxy.browser2.get(url, retry=1)
                proxy.browser2.wait(30)
                for i in range(15):
                    if proxy.browser2.ele('x//*[text="确认您是真人"]'):
                        proxy.browser2.ele('x//*[text="确认您是真人"]').click()
                        print('q')
                    elif proxy.browser2.ele('x//input[@value="Verify you are human"]'):
                        proxy.browser2.ele('x//input[@value="Verify you are human"]').click
                        print('h')
                    else:
                        break
                proxy.browser2.wait(5)
        dfs2 = pd.read_excel('线程书架/线程2.xlsx', usecols=[0], header=None)
        try:
            url_list2 = dfs2.iloc[:, 0].tolist()
            difference2 = [x for x in book_url2 if x not in url_list2]
        except:
            difference2 = book_url2
        for i2, no2 in zip(difference2, tqdm(range(len(difference2)), desc="线程2爬取进度")):
            tab2 = proxy.browser2.new_tab()
            while 1 < 2:
                tab2.get(i2)
                soup2 = BeautifulSoup(tab2.html, 'lxml')
                book_temp2 = soup2.find(attrs={'class': 'list-body'})
                book_name_url2 = re.findall(r'href="(.*?)"', str(book_temp2), re.DOTALL)
                book_name2 = soup2.find(attrs={'style': 'font-size:20px'})
                if book_name2 is None:
                    tab2.wait(10)
                    continue
                else:
                    df2 = pd.DataFrame({
                        'Column1': [book_name2.text.strip()],
                        'Column2': [i2]
                    })

                    print(book_name2.text.strip())
                    break
            file_path_2 = f'TOC/{book_name2.text.replace(":", ".").replace("?", "").replace("？", "").replace("?", "").strip()}.xlsx'
            if os.path.exists(file_path_2):
                try:
                    dfs_2 = pd.read_excel(file_path_2, usecols=[0], header=None)
                except:
                    pass
            else:
                os.makedirs(os.path.dirname(file_path_2), exist_ok=True)
                dfs_empty = pd.DataFrame()
                dfs_empty.to_excel(file_path_2, index=False, header=False)
            try:
                url_list_2 = dfs_2.iloc[:, 0].tolist()
                print(url_list_2)
                difference_2 = [x for x in book_name_url2 if x not in url_list_2]
                if len(difference_2) == len(book_name_url2):
                    difference_2 = []
                else:
                    print(difference_2)
            except:
                difference_2 = book_name_url2
            for j2 in difference_2:
                while mini2 < max2:
                    try:
                        tab2 = proxy.browser2.new_tab()
                        tab2.get(j2)
                        soup12 = BeautifulSoup(tab2.html, 'lxml')
                        book_temp12 = soup12.find(attrs={'itemprop': 'articleBody'})
                        book_name_con2 = soup12.find(attrs={'class': 'toon-title'})
                        aname2 = book_name_con2.text.replace("/", ".").replace(":", ".").replace("?", "").replace(
                            "<",
                            "").strip()
                        tab2.close()
                        print(aname2)
                        book_con2 = \
                            re.findall('<div class="view-img">\n</div>\n<div class=".*?">(.*?)</div>',
                                       str(book_temp12),
                                       re.DOTALL)[0]
                        soup22 = BeautifulSoup(book_con2, 'lxml')
                        soup22_ = soup22.find_all('p')
                        break
                    except:
                        proxy.browser2.quit()
                        co.set_argument('--window-size', '80,60')
                        co.set_local_port(9339)
                        co.add_extension(r'proxy_switchyomega-2.5.20-an+fx')
                        proxy.browser2 = ChromiumPage(co)

                        proxy.browser2.get(url, retry=1)
                        proxy.browser2.wait(30)
                        for i in range(15):
                            if proxy.browser2.ele('x//*[text="确认您是真人"]'):
                                proxy.browser2.ele('x//*[text="确认您是真人"]').click()
                                print('q')
                            elif proxy.browser2.ele('x//input[@value="Verify you are human"]'):
                                proxy.browser2.ele('x//input[@value="Verify you are human"]').click
                                print('h')
                            else:
                                break
                        proxy.browser2.wait(30)
                file_path2 = f'book_all/{book_name2.text.replace(":", ".").replace("?", "").replace("？", "").strip()}/{aname2}.txt'
                os.makedirs(os.path.dirname(file_path2), exist_ok=True)
                with open(file_path2, 'a', encoding='utf-8') as file:
                    for soup2_2 in soup22_:
                        file.write(f'{soup2_2.get_text()}\n')
                dfsj2 = pd.DataFrame({
                    'Column1': [j2],
                    'Column2': [aname2]
                })
                with pd.ExcelWriter(file_path_2, engine='openpyxl', mode='a',
                                    if_sheet_exists='overlay') as writer:
                    if 'Sheet1' in writer.sheets:
                        startrow = writer.sheets['Sheet1'].max_row + 2
                    else:
                        startrow = 0  # 如果工作表不存在，从第0行开始写入
                    dfsj2.to_excel(writer, index=False, header=False, engine='openpyxl', sheet_name='Sheet1',
                                   startrow=startrow)
                print(f'book_all/{book_name2.text.replace(":", ".").replace("?", "").replace("？", "").replace(":", ".").strip()}/{aname2}.txt,已下载')
            name(df=df2)
            shujia(df2, file_path='线程2.xlsx')
            tab2.close()
    elif colist == 3:
        proxy.browser3.get(url, retry=1)
        proxy.browser3.wait(30)
        for i in range(15):
            if proxy.browser3.ele('x//*[text="确认您是真人"]'):
                proxy.browser3.ele('x//*[text="确认您是真人"]').click()
            elif proxy.browser3.ele('x//input[@value="Verify you are human"]'):
                proxy.browser3.ele('x//input[@value="Verify you are human"]').click()
            else:
                break
        proxy.browser3.wait(5)
        max3 = 50
        mini3 = 1
        while mini3 < max3:
            try:
                book_url3 = re.findall(r'class="in-lable trans-bg-black"><a href="(.*?)">', proxy.browser3.html, re.DOTALL)
                if book_url3 == []:
                    print(book_url3)
                    proxy.browser3.quit()
                    co.set_argument('--window-size', '80,60')
                    co.set_local_port(9335)
                    co.add_extension(r'proxy_switchyomega-2.5.20-an+fx')
                    proxy.browser3 = ChromiumPage(co)
                    
                    proxy.browser3.get(url, retry=1)
                    proxy.browser3.wait(30)
                    for i in range(15):
                        if proxy.browser3.ele('x//*[text="确认您是真人"]'):
                            proxy.browser3.ele('x//*[text="确认您是真人"]').click()
                        elif proxy.browser3.ele('x//input[@value="Verify you are human"]'):
                            proxy.browser3.ele('x//input[@value="Verify you are human"]').click()
                        else:
                            break
                    proxy.browser3.wait(5)
                else:
                    break
            except:
                proxy.browser3.wait(30)
                for i in range(15):
                    if proxy.browser3.ele('x//*[text="确认您是真人"]'):
                        proxy.browser3.ele('x//*[text="确认您是真人"]').click()
                    elif proxy.browser3.ele('x//input[@value="Verify you are human"]'):
                        proxy.browser3.ele('x//input[@value="Verify you are human"]').click()
                    else:
                        break
                proxy.browser3.wait(5)
        dfs3 = pd.read_excel('线程书架/线程3.xlsx', usecols=[0], header=None)
        try:
            url_list3 = dfs3.iloc[:, 0].tolist()
            difference3 = [x for x in book_url3 if x not in url_list3]
        except:
            difference3 = book_url3
        for i_3, no3 in zip(difference3, tqdm(range(len(difference3)), desc="线程3爬取进度")):
            tab3 = proxy.browser3.new_tab()
            while 1 < 2:
                tab3.get(i_3)
                soup3 = BeautifulSoup(tab3.html, 'lxml')
                book_temp3 = soup3.find(attrs={'class': 'list-body'})
                book_name_url3 = re.findall(r'href="(.*?)"', str(book_temp3), re.DOTALL)
                book_name3 = soup3.find(attrs={'style': 'font-size:20px'})
                if book_name3 is None:
                    tab3.wait(10)
                    continue
                else:
                    df3 = pd.DataFrame({
                        'Column1': [book_name3.text.strip()],
                        'Column2': [i_3]
                    })

                    print(book_name3.text.strip())
                    break
            file_path_3 = f'TOC/{book_name3.text.replace(":", ".").replace("?", "").replace("？", "").replace("?", "").strip()}.xlsx'
            if os.path.exists(file_path_3):
                try:
                    dfs_3 = pd.read_excel(file_path_3, usecols=[0], header=None)
                except:
                    pass
            else:
                os.makedirs(os.path.dirname(file_path_3), exist_ok=True)
                dfs_empty = pd.DataFrame()
                dfs_empty.to_excel(file_path_3, index=False, header=False)
            try:
                url_list_3 = dfs_3.iloc[:, 0].tolist()
                print(url_list_3)
                difference_3 = [x for x in book_name_url3 if x not in url_list_3]
                if len(difference_3) == len(book_name_url3):
                    difference_3 = []
                else:
                    print(difference_3)
            except:
                difference_3 = book_name_url3
            for j_3 in difference_3:
                while mini3 < max3:
                    try:
                        tab3 = proxy.browser3.new_tab()
                        tab3.get(j_3)
                        soup_3 = BeautifulSoup(tab3.html, 'lxml')
                        book_temp_3 = soup_3.find(attrs={'itemprop': 'articleBody'})
                        book_name_con3 = soup_3.find(attrs={'class': 'toon-title'})
                        aname3 = book_name_con3.text.replace("/", ".").replace(":", ".").replace("?", "").replace("<", "").strip()
                        tab3.close()
                        print(aname3)
                        book_con = \
                            re.findall('<div class="view-img">\n</div>\n<div class=".*?">(.*?)</div>', str(book_temp_3),
                                       re.DOTALL)[0]
                        soup__3 = BeautifulSoup(book_con, 'lxml')
                        soup__3_ = soup__3.find_all('p')
                        break
                    except:
                        proxy.browser3.quit()
                        co.set_argument('--window-size', '80,60')
                        co.set_local_port(9335)
                        co.add_extension(r'proxy_switchyomega-2.5.20-an+fx')
                        proxy.browser3 = ChromiumPage(co)
                        
                        proxy.browser3.get(url, retry=1)
                        proxy.browser3.wait(30)
                        for i in range(15):
                            if proxy.browser3.ele('x//*[text="确认您是真人"]'):
                                proxy.browser3.ele('x//*[text="确认您是真人"]').click()
                            elif proxy.browser3.ele('x//input[@value="Verify you are human"]'):
                                proxy.browser3.ele('x//input[@value="Verify you are human"]').click()
                            else:
                                break
                        proxy.browser3.wait(5)

                file_path3 = f'book_all/{book_name3.text.replace(":", ".").replace("?", "").replace("？", "").strip()}/{aname3}.txt'
                os.makedirs(os.path.dirname(file_path3), exist_ok=True)
                with open(file_path3, 'a', encoding='utf-8') as file:
                    for soup2_3 in soup__3_:
                        file.write(f'{soup2_3.get_text()}\n')
                dfsj3 = pd.DataFrame({
                    'Column1': [j_3],
                    'Column2': [aname3]
                })
                with pd.ExcelWriter(file_path_3, engine='openpyxl', mode='a',
                                    if_sheet_exists='overlay') as writer:
                    if 'Sheet1' in writer.sheets:
                        startrow = writer.sheets['Sheet1'].max_row + 2
                    else:
                        startrow = 0  # 如果工作表不存在，从第0行开始写入
                    dfsj3.to_excel(writer, index=False, header=False, engine='openpyxl', sheet_name='Sheet1',
                                   startrow=startrow)
                print(f'book_all/{book_name3.text.replace(":", ".").replace("?", "").replace("？", "").replace(":", ".").strip()}/{aname3}.txt,已下载')
            name(df=df3)
            shujia(df3, file_path='线程3.xlsx')
            tab3.close()
    elif colist == 4:
        proxy.browser4.get(url, retry=1)
        proxy.browser4.wait(30)
        for i in range(15):
            if proxy.browser4.ele('x//*[text="确认您是真人"]'):
                proxy.browser4.ele('x//*[text="确认您是真人"]').click()
            elif proxy.browser4.ele('x//input[@value="Verify you are human"]'):
                proxy.browser4.ele('x//input[@value="Verify you are human"]').click()
            else:
                break
        proxy.browser4.wait(5)
        max4 = 50
        mini4 = 1
        while mini4 < max4:
            try:
                book_url4 = re.findall(r'class="in-lable trans-bg-black"><a href="(.*?)">', proxy.browser4.html, re.DOTALL)
                if book_url4 == []:
                    print(book_url4)
                    proxy.browser4.quit()
                    co.set_argument('--window-size', '80,60')
                    co.set_local_port(9336)
                    co.add_extension(r'proxy_switchyomega-2.5.20-an+fx')
                    proxy.browser4 = ChromiumPage(co)
                    
                    proxy.browser4.get(url, retry=1)
                    proxy.browser4.wait(30)
                    for i in range(15):
                        if proxy.browser4.ele('x//*[text="确认您是真人"]'):
                            proxy.browser4.ele('x//*[text="确认您是真人"]').click()
                        elif proxy.browser4.ele('x//input[@value="Verify you are human"]'):
                            proxy.browser4.ele('x//input[@value="Verify you are human"]').click()
                        else:
                            break
                    proxy.browser4.wait(5)
                else:
                    break
            except:
                proxy.browser4.quit()
                co.set_argument('--window-size', '80,60')
                co.set_local_port(9336)
                co.add_extension(r'proxy_switchyomega-2.5.20-an+fx')
                proxy.browser4 = ChromiumPage(co)
                
                proxy.browser4.get(url, retry=1)
                proxy.browser4.wait(30)
                for i in range(15):
                    if proxy.browser4.ele('x//*[text="确认您是真人"]'):
                        proxy.browser4.ele('x//*[text="确认您是真人"]').click()
                    elif proxy.browser4.ele('x//input[@value="Verify you are human"]'):
                        proxy.browser4.ele('x//input[@value="Verify you are human"]').click()
                    else:
                        break
                proxy.browser4.wait(5)
        dfs4 = pd.read_excel('线程书架/线程4.xlsx', usecols=[0], header=None)
        try:
            url_list4 = dfs4.iloc[:, 0].tolist()
            difference4 = [x for x in book_url4 if x not in url_list4]
        except:
            difference4 = book_url4
        for i_4, no4 in zip(difference4, tqdm(range(len(difference4)), desc="线程4爬取进度")):
            tab4 = proxy.browser4.new_tab()
            while 1 < 2:
                tab4.get(i_4)
                soup4 = BeautifulSoup(tab4.html, 'lxml')
                book_temp4 = soup4.find(attrs={'class': 'list-body'})
                book_name_url4 = re.findall(r'href="(.*?)"', str(book_temp4), re.DOTALL)
                book_name4 = soup4.find(attrs={'style': 'font-size:20px'})
                if book_name4 is None:
                    tab4.wait(10)
                    continue
                else:
                    df4 = pd.DataFrame({
                        'Column1': [book_name4.text.strip()],
                        'Column2': [i_4]
                    })

                    print(book_name4.text.strip())
                    break
            file_path_4 = f'TOC/{book_name4.text.replace(":", ".").replace("?", "").replace("？", "").replace("?", "").strip()}.xlsx'
            if os.path.exists(file_path_4):
                try:
                    dfs_4 = pd.read_excel(file_path_4, usecols=[0], header=None)
                except:
                    pass
            else:
                os.makedirs(os.path.dirname(file_path_4), exist_ok=True)
                dfs_empty = pd.DataFrame()
                dfs_empty.to_excel(file_path_4, index=False, header=False)
            try:
                url_list_4 = dfs_4.iloc[:, 0].tolist()
                print(url_list_4)
                difference_4 = [x for x in book_name_url4 if x not in url_list_4]
                if len(difference_4) == len(book_name_url4):
                    difference_4 = []
                else:
                    print(difference_4)
            except:
                difference_4 = book_name_url4
            for j_4 in difference_4:
                while mini4 < max4:
                    try:
                        tab4 = proxy.browser4.new_tab()
                        tab4.get(j_4)
                        soup_4 = BeautifulSoup(tab4.html, 'lxml')
                        book_temp_4 = soup_4.find(attrs={'itemprop': 'articleBody'})
                        book_name_con4 = soup_4.find(attrs={'class': 'toon-title'})
                        aname4 = book_name_con4.text.replace("/", ".").replace(":", ".").replace("?", "").replace("<", "").strip()
                        tab4.close()
                        print(aname4)
                        book_con = \
                            re.findall('<div class="view-img">\n</div>\n<div class=".*?">(.*?)</div>', str(book_temp_4),
                                       re.DOTALL)[0]
                        soup__4 = BeautifulSoup(book_con, 'lxml')
                        soup__4_ = soup__4.find_all('p')
                        break
                    except:
                        proxy.browser4.quit()
                        co.set_argument('--window-size', '80,60')
                        co.set_local_port(9336)
                        co.add_extension(r'proxy_switchyomega-2.5.20-an+fx')
                        proxy.browser4 = ChromiumPage(co)
                        
                        proxy.browser4.get(url, retry=1)
                        proxy.browser4.wait(30)
                        for i in range(15):
                            if proxy.browser4.ele('x//*[text="确认您是真人"]'):
                                proxy.browser4.ele('x//*[text="确认您是真人"]').click()
                            elif proxy.browser4.ele('x//input[@value="Verify you are human"]'):
                                proxy.browser4.ele('x//input[@value="Verify you are human"]').click()
                            else:
                                break

                        proxy.browser4.wait(5)

                file_path4 = f'book_all/{book_name4.text.replace(":", ".").replace("?", "").replace("？", "").strip()}/{aname4}.txt'
                os.makedirs(os.path.dirname(file_path4), exist_ok=True)
                with open(file_path4, 'a', encoding='utf-8') as file:
                    for soup2_4 in soup__4_:
                        file.write(f'{soup2_4.get_text()}\n')
                dfsj4 = pd.DataFrame({
                    'Column1': [j_4],
                    'Column2': [aname4]
                })
                with pd.ExcelWriter(file_path_4, engine='openpyxl', mode='a',
                                    if_sheet_exists='overlay') as writer:
                    if 'Sheet1' in writer.sheets:
                        startrow = writer.sheets['Sheet1'].max_row + 2
                    else:
                        startrow = 0  # 如果工作表不存在，从第0行开始写入
                    dfsj4.to_excel(writer, index=False, header=False, engine='openpyxl', sheet_name='Sheet1',
                                   startrow=startrow)
                print(f'book_all/{book_name4.text.replace(":", ".").replace("?", "").replace("？", "").replace(":", ".").strip()}/{aname4}.txt,已下载')
            name(df=df4)
            shujia(df4, file_path='线程4.xlsx')
            tab4.close()
    elif colist == 5:
        proxy.browser5.get(url, retry=1)
        proxy.browser5.wait(30)
        for i in range(15):
            if proxy.browser5.ele('x//*[text="确认您是真人"]'):
                proxy.browser5.ele('x//*[text="确认您是真人"]').click()
                print('q')
            elif proxy.browser5.ele('x//input[@value="Verify you are human"]'):
                proxy.browser5.ele('x//input[@value="Verify you are human"]').click
                print('h')
            else:
                break
        proxy.browser5.wait(5)
        max5 = 50
        mini5 = 1
        while mini5 < max5:
            book_url5 = re.findall(r'class="in-lable trans-bg-black"><a href="(.*?)">', proxy.browser5.html, re.DOTALL)
            if book_url5 == []:
                print(book_url5)
                proxy.browser5.quit()
                co.set_argument('--window-size', '80,60')
                co.set_local_port(9337)
                co.add_extension(r'proxy_switchyomega-2.5.20-an+fx')
                proxy.browser5 = ChromiumPage(co)
                
                proxy.browser5.get(url, retry=1)
                proxy.browser5.wait(30)
                for i in range(15):
                    if proxy.browser5.ele('x//*[text="确认您是真人"]'):
                        proxy.browser5.ele('x//*[text="确认您是真人"]').click()
                        print('q')
                    elif proxy.browser5.ele('x//input[@value="Verify you are human"]'):
                        proxy.browser5.ele('x//input[@value="Verify you are human"]').click()
                        print('h')
                    else:
                        break
                proxy.browser5.wait(5)
            else:
                break
        dfs5 = pd.read_excel('线程书架/线程5.xlsx', usecols=[0], header=None)
        try:
            url_list5 = dfs5.iloc[:, 0].tolist()
            difference5 = [x for x in book_url5 if x not in url_list5]
        except:
            difference5 = book_url5
        for i_5, no5 in zip(difference5, tqdm(range(len(difference5)), desc="线程5爬取进度")):
            tab5 = proxy.browser5.new_tab()
            while 1 < 2:
                tab5.get(i_5)
                soup5 = BeautifulSoup(tab5.html, 'lxml')
                book_temp5 = soup5.find(attrs={'class': 'list-body'})
                book_name_url5 = re.findall(r'href="(.*?)"', str(book_temp5), re.DOTALL)
                book_name5 = soup5.find(attrs={'style': 'font-size:20px'})
                if book_name5 is None:
                    tab5.wait(10)
                    continue
                else:
                    df5 = pd.DataFrame({
                        'Column1': [book_name5.text.replace("?", "").replace("？", "").strip()],
                        'Column2': [i_5]
                    })

                    print(book_name5.text.strip())
                    break
            file_path_5 = f'TOC/{book_name5.text.replace("?", "").replace("？", "").strip()}.xlsx'
            if os.path.exists(file_path_5):
                try:
                    dfs_5 = pd.read_excel(file_path_5, usecols=[0], header=None)
                except:
                    pass
            else:
                os.makedirs(os.path.dirname(file_path_5), exist_ok=True)
                dfs_empty = pd.DataFrame()
                dfs_empty.to_excel(file_path_5, index=False, header=False)
            try:
                url_list_5 = dfs_5.iloc[:, 0].tolist()
                print(url_list_5)
                difference_5 = [x for x in book_name_url5 if x not in url_list_5]
                if len(difference_5) == len(book_name_url5):
                    difference_5 = []
                else:
                    print(difference_5)
            except:
                difference_5 = book_name_url5

            for j_5 in difference_5:
                while mini5 < max5:
                    try:
                        tab5 = proxy.browser5.new_tab()
                        tab5.get(j_5)
                        soup_5 = BeautifulSoup(tab5.html, 'lxml')
                        book_temp_5 = soup_5.find(attrs={'itemprop': 'articleBody'})
                        book_name_con5 = soup_5.find(attrs={'class': 'toon-title'})
                        aname5 = book_name_con5.text.replace("/", ".").replace(":", ".").replace("?", "").replace("<", "").strip()
                        tab5.close()
                        print(aname5)
                        book_con5 = \
                            re.findall('<div class="view-img">\n</div>\n<div class=".*?">(.*?)</div>', str(book_temp_5),
                                       re.DOTALL)[0]
                        soup__5 = BeautifulSoup(book_con5, 'lxml')
                        soup__5_ = soup__5.find_all('p')
                        break
                    except:
                        proxy.browser5.quit()
                        co.set_argument('--window-size', '80,60')
                        co.set_local_port(9337)
                        co.add_extension(r'proxy_switchyomega-2.5.20-an+fx')
                        proxy.browser5 = ChromiumPage(co)
                        
                        proxy.browser5.get(url, retry=1)
                        proxy.browser5.wait(30)
                        for i in range(15):
                            if proxy.browser5.ele('x//*[text="确认您是真人"]'):
                                proxy.browser5.ele('x//*[text="确认您是真人"]').click()
                                print('q')
                            elif proxy.browser5.ele('x//input[@value="Verify you are human"]'):
                                proxy.browser5.ele('x//input[@value="Verify you are human"]').click
                                print('h')
                            else:
                                break
                        proxy.browser5.wait(5)

                file_path5 = f'book_all/{book_name5.text.replace("?", "").replace("？", "").strip()}/{aname5}.txt'
                os.makedirs(os.path.dirname(file_path5), exist_ok=True)
                with open(file_path5, 'a', encoding='utf-8') as file:
                    for soup2_5 in soup__5_:
                        file.write(f'{soup2_5.get_text()}\n')
                dfsj5 = pd.DataFrame({
                    'Column1': [j_5],
                    'Column2': [aname5]
                })
                with pd.ExcelWriter(file_path_5, engine='openpyxl', mode='a',
                                    if_sheet_exists='overlay') as writer:
                    if 'Sheet1' in writer.sheets:
                        startrow = writer.sheets['Sheet1'].max_row + 2
                    else:
                        startrow = 0  # 如果工作表不存在，从第0行开始写入
                    dfsj5.to_excel(writer, index=False, header=False, engine='openpyxl', sheet_name='Sheet1',
                                   startrow=startrow)
                print(f'book_all/{book_name5.text.replace(":", ".").replace("?", "").replace("？", "").strip()}/{aname5}.txt,已下载')
            name(df=df5)
            shujia(df5, file_path='线程5.xlsx')
            tab5.close()
    elif colist == 6:
        proxy.browser6.get(url, retry=1)
        proxy.browser6.wait(30)
        for i in range(15):
            if proxy.browser6.ele('x//*[text="确认您是真人"]'):
                proxy.browser6.ele('x//*[text="确认您是真人"]').click()
                print('q')
            elif proxy.browser6.ele('x//input[@value="Verify you are human"]'):
                proxy.browser6.ele('x//input[@value="Verify you are human"]').click()
                print('h')
            else:
                break
        proxy.browser6.wait(5)
        max6 = 50
        mini6 = 1
        while mini6 < max6:
            try:
                book_url6 = re.findall(r'class="in-lable trans-bg-black"><a href="(.*?)">', proxy.browser6.html, re.DOTALL)
                if book_url6 == []:
                    print(book_url6)
                    proxy.browser6.quit()
                    co.set_argument('--window-size', '80,60')
                    co.set_local_port(9338)
                    co.add_extension(r'proxy_switchyomega-2.5.20-an+fx')
                    proxy.browser6 = ChromiumPage(co)
                    
                    proxy.browser6.get(url, retry=1)
                    proxy.browser6.wait(30)
                    for i in range(15):
                        if proxy.browser6.ele('x//*[text="确认您是真人"]'):
                            proxy.browser6.ele('x//*[text="确认您是真人"]').click()
                            print('q')
                        elif proxy.browser6.ele('x//input[@value="Verify you are human"]'):
                            proxy.browser6.ele('x//input[@value="Verify you are human"]').click
                            print('h')
                        else:
                            break
                    proxy.browser6.wait(5)
                else:
                    break
            except:
                proxy.browser6.quit()
                co.set_argument('--window-size', '80,60')
                co.set_local_port(9338)
                co.add_extension(r'proxy_switchyomega-2.5.20-an+fx')
                proxy.browser6 = ChromiumPage(co)
                
                proxy.browser6.get(url, retry=1)
                proxy.browser6.wait(30)
                for i in range(15):
                    if proxy.browser6.ele('x//*[text="确认您是真人"]'):
                        proxy.browser6.ele('x//*[text="确认您是真人"]').click()
                        print('q')
                    elif proxy.browser6.ele('x//input[@value="Verify you are human"]'):
                        proxy.browser6.ele('x//input[@value="Verify you are human"]').click
                        print('h')
                    else:
                        break
                proxy.browser6.wait(5)
        dfs6 = pd.read_excel('线程书架/线程6.xlsx', usecols=[0], header=None)
        try:
            url_list6 = dfs6.iloc[:, 0].tolist()
            difference6 = [x for x in book_url6 if x not in url_list6]
        except:
            difference6 = book_url6
        for i6, no6 in zip(difference6, tqdm(range(len(difference6)), desc="线程6爬取进度")):
            tab6 = proxy.browser6.new_tab()
            while 1 < 2:
                tab6.get(i6)
                soup6 = BeautifulSoup(tab6.html, 'lxml')
                book_temp6 = soup6.find(attrs={'class': 'list-body'})
                book_name_url6 = re.findall(r'href="(.*?)"', str(book_temp6), re.DOTALL)
                book_name6 = soup6.find(attrs={'style': 'font-size:20px'})
                if book_name6 is None:
                    tab6.wait(10)
                    continue
                else:
                    df6 = pd.DataFrame({
                        'Column1': [book_name6.text.strip()],
                        'Column2': [i6]
                    })

                    print(book_name6.text.strip())
                    break
            file_path_6 = f'TOC/{book_name6.text.replace("?", "").strip()}.xlsx'
            if os.path.exists(file_path_6):
                try:
                    dfs_6 = pd.read_excel(file_path_6, usecols=[0], header=None)
                except:
                    pass
            else:
                os.makedirs(os.path.dirname(file_path_6), exist_ok=True)
                dfs_empty = pd.DataFrame()
                dfs_empty.to_excel(file_path_6, index=False, header=False)
            try:
                url_list_6 = dfs_6.iloc[:, 0].tolist()
                print(url_list_6)
                difference_6 = [x for x in book_name_url6 if x not in url_list_6]
                if len(difference_6) == len(book_name_url6):
                    difference_6 = []
                else:
                    print(difference_6)
            except:
                difference_6 = book_name_url6

            for j6 in difference_6:
                while mini6 < max6:
                    try:
                        tab6 = proxy.browser6.new_tab()
                        tab6.get(j6)
                        soup16 = BeautifulSoup(tab6.html, 'lxml')
                        book_temp16 = soup16.find(attrs={'itemprop': 'articleBody'})
                        book_name_con6 = soup16.find(attrs={'class': 'toon-title'})
                        aname6 = book_name_con6.text.replace("/", ".").replace(":", ".").replace("?", "").replace("<", "").strip()
                        tab6.close()
                        print(aname6)
                        book_con6 = \
                            re.findall('<div class="view-img">\n</div>\n<div class=".*?">(.*?)</div>', str(book_temp16),
                                       re.DOTALL)[0]
                        soup26 = BeautifulSoup(book_con6, 'lxml')
                        soup26_ = soup26.find_all('p')
                        break
                    except:
                        proxy.browser6.quit()
                        co.set_argument('--window-size', '80,60')
                        co.set_local_port(9338)
                        co.add_extension(r'proxy_switchyomega-2.5.20-an+fx')
                        proxy.browser6 = ChromiumPage(co)
                        
                        proxy.browser6.get(url, retry=1)
                        proxy.browser6.wait(30)
                        for i in range(15):
                            if proxy.browser6.ele('x//*[text="确认您是真人"]'):
                                proxy.browser6.ele('x//*[text="确认您是真人"]').click()
                                print('q')
                            elif proxy.browser6.ele('x//input[@value="Verify you are human"]'):
                                proxy.browser6.ele('x//input[@value="Verify you are human"]').click
                                print('h')
                            else:
                                break
                        proxy.browser6.wait(5)

                file_path6 = f'book_all/{book_name6.text.strip()}/{aname6}.txt'
                os.makedirs(os.path.dirname(file_path6), exist_ok=True)
                with open(file_path6, 'a', encoding='utf-8') as file:
                    for soup2_6 in soup26_:
                        file.write(f'{soup2_6.get_text()}\n')
                dfsj6 = pd.DataFrame({
                    'Column1': [j6],
                    'Column2': [aname6]
                })
                with pd.ExcelWriter(file_path_6, engine='openpyxl', mode='a',
                                    if_sheet_exists='overlay') as writer:
                    if 'Sheet1' in writer.sheets:
                        startrow = writer.sheets['Sheet1'].max_row + 2
                    else:
                        startrow = 0  # 如果工作表不存在，从第0行开始写入
                    dfsj6.to_excel(writer, index=False, header=False, engine='openpyxl', sheet_name='Sheet1',
                                   startrow=startrow)
                print(f'book_all/{book_name6.text.replace(":", ".").strip()}/{aname6}.txt,已下载')
            name(df=df6)
            shujia(df6, file_path='线程6.xlsx')
            tab6.close()
    elif colist == 7:
        proxy.browser7.get(url, retry=1)
        proxy.browser7.wait(30)
        for i in range(15):
            if proxy.browser7.ele('x//*[text="确认您是真人"]'):
                proxy.browser7.ele('x//*[text="确认您是真人"]').click()
                print('q')
            elif proxy.browser7.ele('x//input[@value="Verify you are human"]'):
                proxy.browser7.ele('x//input[@value="Verify you are human"]').click
                print('h')
            else:
                break
        proxy.browser7.wait(5)
        max7 = 100
        mini7 = 1
        while mini7 < max7:
            try:
                book_url7 = re.findall(r'class="in-lable trans-bg-black"><a href="(.*?)">', proxy.browser7.html, re.DOTALL)
                if book_url7 == []:
                    print(book_url7)
                    proxy.browser7.quit()
                    co.set_argument('--window-size', '80,60')
                    co.set_local_port(9339)
                    co.add_extension(r'proxy_switchyomega-2.5.20-an+fx')
                    proxy.browser7 = ChromiumPage(co)
                    
                    proxy.browser7.get(url, retry=1)
                    proxy.browser7.wait(30)
                    for i in range(15):
                        if proxy.browser8.ele('x//*[text="确认您是真人"]'):
                            proxy.browser8.ele('x//*[text="确认您是真人"]').click()
                            print('q')
                        elif proxy.browser8.ele('x//input[@value="Verify you are human"]'):
                            proxy.browser8.ele('x//input[@value="Verify you are human"]').click
                            print('h')
                        else:
                            break
                    proxy.browser7.wait(5)
                else:
                    break
            except:
                proxy.browser7.quit()
                co.set_argument('--window-size', '80,60')
                co.set_local_port(9339)
                co.add_extension(r'proxy_switchyomega-2.5.20-an+fx')
                proxy.browser7 = ChromiumPage(co)
                
                proxy.browser7.get(url, retry=1)
                proxy.browser7.wait(30)
                for i in range(15):
                    if proxy.browser7.ele('x//*[text="确认您是真人"]'):
                        proxy.browser7.ele('x//*[text="确认您是真人"]').click()
                        print('q')
                    elif proxy.browser7.ele('x//input[@value="Verify you are human"]'):
                        proxy.browser7.ele('x//input[@value="Verify you are human"]').click
                        print('h')
                    else:
                        break
                proxy.browser7.wait(5)
        dfs7 = pd.read_excel('线程书架/线程7.xlsx', usecols=[0], header=None)
        try:
            url_list7 = dfs7.iloc[:, 0].tolist()
            difference7 = [x for x in book_url7 if x not in url_list7]
        except:
            difference7 = book_url7
        for i7, no7 in zip(difference7, tqdm(range(len(difference7)), desc="线程7爬取进度")):
            tab7 = proxy.browser7.new_tab()
            while 1 < 2:
                tab7.get(i7)
                soup7 = BeautifulSoup(tab7.html, 'lxml')
                book_temp7 = soup7.find(attrs={'class': 'list-body'})
                book_name_url7 = re.findall(r'href="(.*?)"', str(book_temp7), re.DOTALL)
                book_name7 = soup7.find(attrs={'style': 'font-size:20px'})
                if book_name7 is None:
                    tab7.wait(10)
                    continue
                else:
                    df7 = pd.DataFrame({
                        'Column1': [book_name7.text.strip()],
                        'Column2': [i7]
                    })

                    print(book_name7.text.strip())
                    break
            file_path_7 = f'TOC/{book_name7.text.replace("?", "").strip()}.xlsx'
            if os.path.exists(file_path_7):
                try:
                    dfs_7 = pd.read_excel(file_path_7, usecols=[0], header=None)
                except:
                    pass
            else:
                os.makedirs(os.path.dirname(file_path_7), exist_ok=True)
                dfs_empty = pd.DataFrame()
                dfs_empty.to_excel(file_path_7, index=False, header=False)
            try:
                url_list_7 = dfs_7.iloc[:, 0].tolist()
                print(url_list_7)
                difference_7 = [x for x in book_name_url7 if x not in url_list_7]
                if len(difference_7) == len(book_name_url7):
                    difference_7 = []
                else:
                    print(difference_7)
            except:
                difference_7 = book_name_url7
            for j7 in difference_7:
                while mini7 < max7:
                    try:
                        tab7 = proxy.browser7.new_tab()
                        tab7.get(j7)
                        soup17 = BeautifulSoup(tab7.html, 'lxml')
                        book_temp17 = soup17.find(attrs={'itemprop': 'articleBody'})
                        book_name_con7 = soup17.find(attrs={'class': 'toon-title'})
                        aname7 = book_name_con7.text.replace("/", ".").replace(":", ".").replace("?", "").replace("<", "").strip()
                        tab7.close()
                        print(aname7)
                        book_con7 = \
                            re.findall('<div class="view-img">\n</div>\n<div class=".*?">(.*?)</div>', str(book_temp17),
                                       re.DOTALL)[0]
                        soup27 = BeautifulSoup(book_con7, 'lxml')
                        soup27_ = soup27.find_all('p')
                        break
                    except:
                        proxy.browser7.quit()
                        co.set_argument('--window-size', '80,60')
                        co.set_local_port(9339)
                        co.add_extension(r'proxy_switchyomega-2.5.20-an+fx')
                        proxy.browser7 = ChromiumPage(co)
                        
                        proxy.browser7.get(url, retry=1)
                        proxy.browser7.wait(30)
                        for i in range(15):
                            if proxy.browser7.ele('x//*[text="确认您是真人"]'):
                                proxy.browser7.ele('x//*[text="确认您是真人"]').click()
                                print('q')
                            elif proxy.browser7.ele('x//input[@value="Verify you are human"]'):
                                proxy.browser7.ele('x//input[@value="Verify you are human"]').click
                                print('h')
                            else:
                                break
                        proxy.browser7.wait(30)
                file_path7 = f'book_all/{book_name7.text.strip()}/{aname7}.txt'
                os.makedirs(os.path.dirname(file_path7), exist_ok=True)
                with open(file_path7, 'a', encoding='utf-8') as file:
                    for soup2_7 in soup27_:
                        file.write(f'{soup2_7.get_text()}\n')
                dfsj7 = pd.DataFrame({
                    'Column1': [j7],
                    'Column2': [aname7]
                })
                with pd.ExcelWriter(file_path_7, engine='openpyxl', mode='a',
                                    if_sheet_exists='overlay') as writer:
                    if 'Sheet1' in writer.sheets:
                        startrow = writer.sheets['Sheet1'].max_row + 2
                    else:
                        startrow = 0  # 如果工作表不存在，从第0行开始写入
                    dfsj7.to_excel(writer, index=False, header=False, engine='openpyxl', sheet_name='Sheet1',
                                   startrow=startrow)
                print(f'book_all/{book_name7.text.replace(":", ".").strip()}/{aname7}.txt,已下载')
            name(df=df7)
            shujia(df7, file_path='线程7.xlsx')
            tab7.close()
    elif colist == 8:
        proxy.browser8.get(url, retry=1)
        proxy.browser8.wait(30)
        for i in range(15):
            if proxy.browser8.ele('x//*[text="确认您是真人"]'):
                proxy.browser8.ele('x//*[text="确认您是真人"]').click()
                print('q')
            elif proxy.browser8.ele('x//input[@value="Verify you are human"]'):
                proxy.browser8.ele('x//input[@value="Verify you are human"]').click()
                print('h')
            else:
                break
        proxy.browser8.wait(5)
        max8 = 50
        mini8 = 1
        while mini8 < max8:
            try:
                book_url8 = re.findall(r'class="in-lable trans-bg-black"><a href="(.*?)">', proxy.browser8.html, re.DOTALL)
                if book_url8 == []:
                    print(book_url8)
                    proxy.browser8.quit()
                    co.set_argument('--window-size', '80,60')
                    co.set_local_port(9340)
                    co.add_extension(r'proxy_switchyomega-2.5.20-an+fx')
                    proxy.browser8 = ChromiumPage(co)
                    
                    proxy.browser8.get(url, retry=1)
                    proxy.browser8.wait(30)
                    for i in range(15):
                        if proxy.browser8.ele('x//*[text="确认您是真人"]'):
                            proxy.browser8.ele('x//*[text="确认您是真人"]').click()
                            print('q')
                        elif proxy.browser8.ele('x//input[@value="Verify you are human"]'):
                            proxy.browser8.ele('x//input[@value="Verify you are human"]').click
                            print('h')
                        else:
                            break
                    proxy.browser8.wait(5)
                else:
                    break
            except:
                proxy.browser8.quit()
                co.set_argument('--window-size', '80,60')
                co.set_local_port(9340)
                co.add_extension(r'proxy_switchyomega-2.5.20-an+fx')
                proxy.browser8 = ChromiumPage(co)
                
                proxy.browser8.get(url, retry=1)
                proxy.browser8.wait(30)
                for i in range(15):
                    if proxy.browser8.ele('x//*[text="确认您是真人"]'):
                        proxy.browser8.ele('x//*[text="确认您是真人"]').click()
                        print('q')
                    elif proxy.browser8.ele('x//input[@value="Verify you are human"]'):
                        proxy.browser8.ele('x//input[@value="Verify you are human"]').click
                        print('h')
                    else:
                        break
                proxy.browser8.wait(5)
        dfs8 = pd.read_excel('线程书架/线程8.xlsx', usecols=[0], header=None)
        try:
            url_list8 = dfs8.iloc[:, 0].tolist()
            difference8 = [x for x in book_url8 if x not in url_list8]
        except:
            difference8 = book_url8
        for i8, no8 in zip(difference8, tqdm(range(len(difference8)), desc="线程8爬取进度")):
            tab8 = proxy.browser8.new_tab()
            while 1 < 2:
                tab8.get(i8)
                soup8 = BeautifulSoup(tab8.html, 'lxml')
                book_temp8 = soup8.find(attrs={'class': 'list-body'})
                book_name_url8 = re.findall(r'href="(.*?)"', str(book_temp8), re.DOTALL)
                book_name8 = soup8.find(attrs={'style': 'font-size:20px'})
                if book_name8 is None:
                    tab8.wait(10)
                    continue
                else:
                    df8 = pd.DataFrame({
                        'Column1': [book_name8.text.strip()],
                        'Column2': [i8]
                    })

                    print(book_name8.text.strip())
                    break
            file_path_8 = f'TOC/{book_name8.text.replace("?", "").strip()}.xlsx'
            if os.path.exists(file_path_8):
                try:
                    dfs_8 = pd.read_excel(file_path_8, usecols=[0], header=None)
                except:
                    pass
            else:
                os.makedirs(os.path.dirname(file_path_8), exist_ok=True)
                dfs_empty = pd.DataFrame()
                dfs_empty.to_excel(file_path_8, index=False, header=False)
            try:
                url_list_8 = dfs_8.iloc[:, 0].tolist()
                difference_8 = [x for x in book_name_url8 if x not in url_list_8]
                if len(difference_8) == len(book_name_url8):
                    difference_8 = []
                else:
                    print(difference_8)
            except:
                difference_8 = book_name_url8
            for j8 in difference_8:
                while mini8 < max8:
                    try:
                        tab8 = proxy.browser8.new_tab()
                        tab8.get(j8)
                        soup18 = BeautifulSoup(tab8.html, 'lxml')
                        book_temp18 = soup18.find(attrs={'itemprop': 'articleBody'})
                        book_name_con8 = soup18.find(attrs={'class': 'toon-title'})
                        aname8 = book_name_con8.text.replace("/", ".").replace(":", ".").replace("?", "").replace("<", "").strip()
                        tab8.close()
                        print(aname8)
                        book_con8 = \
                            re.findall('<div class="view-img">\n</div>\n<div class=".*?">(.*?)</div>', str(book_temp18),
                                       re.DOTALL)[0]
                        soup28 = BeautifulSoup(book_con8, 'lxml')
                        soup28_ = soup28.find_all('p')
                        break
                    except:
                        proxy.browser8.quit()
                        co.set_argument('--window-size', '80,60')
                        co.set_local_port(9340)
                        co.add_extension(r'proxy_switchyomega-2.5.20-an+fx')
                        proxy.browser8 = ChromiumPage(co)
                        
                        proxy.browser8.get(url, retry=1)
                        proxy.browser8.wait(30)
                        for i in range(15):
                            if proxy.browser8.ele('x//*[text="确认您是真人"]'):
                                proxy.browser8.ele('x//*[text="确认您是真人"]').click(by_js=True)
                                print('q')
                            elif proxy.browser8.ele('x//input[@value="Verify you are human"]'):
                                proxy.browser8.ele('x//input[@value="Verify you are human"]').click
                                print('h')
                            else:
                                break
                        proxy.browser8.wait(5)
                file_path8 = f'book_all/{book_name8.text.strip()}/{aname8}.txt'
                os.makedirs(os.path.dirname(file_path8), exist_ok=True)
                with open(file_path8, 'a', encoding='utf-8') as file:
                    for soup2_8 in soup28_:
                        file.write(f'{soup2_8.get_text()}\n')
                dfsj8 = pd.DataFrame({
                    'Column1': [j8],
                    'Column2': [aname8]
                })
                with pd.ExcelWriter(file_path_8, engine='openpyxl', mode='a',
                                    if_sheet_exists='overlay') as writer:
                    if 'Sheet1' in writer.sheets:
                        startrow = writer.sheets['Sheet1'].max_row + 2
                    else:
                        startrow = 0  # 如果工作表不存在，从第0行开始写入
                    dfsj8.to_excel(writer, index=False, header=False, engine='openpyxl', sheet_name='Sheet1',
                                   startrow=startrow)
                print(f'book_all/{book_name8.text.replace(":", ".").strip()}/{aname8}.txt,已下载')
            name(df=df8)
            shujia(df8, file_path='线程8.xlsx')
            tab8.close()
    elif colist == 9:
        proxy.browser9.get(url, retry=1)
        proxy.browser9.wait(30)
        for i in range(15):
            if proxy.browser9.ele('x//*[text="确认您是真人"]'):
                proxy.browser9.ele('x//*[text="确认您是真人"]').click(by_js=True)
                print('q')
            elif proxy.browser9.ele('x//input[@value="Verify you are human"]'):
                proxy.browser9.ele('x//input[@value="Verify you are human"]').click
                print('h')
            else:
                break
        proxy.browser9.wait(5)
        max9 = 50
        mini9 = 1
        while mini9 < max9:
            try:
                book_url9 = re.findall(r'class="in-lable trans-bg-black"><a href="(.*?)">', proxy.browser9.html, re.DOTALL)
                if book_url9 == []:
                    print(book_url9)
                    proxy.browser9.quit()
                    co.set_argument('--window-size', '80,60')
                    co.set_local_port(9341)
                    co.add_extension(r'proxy_switchyomega-2.5.20-an+fx')
                    proxy.browser9 = ChromiumPage(co)
                    
                    proxy.browser9.get(url, retry=1)
                    proxy.browser9.wait(30)
                    for i in range(15):
                        if proxy.browser9.ele('x//*[text="确认您是真人"]'):
                            proxy.browser9.ele('x//*[text="确认您是真人"]').click(by_js=True)
                            print('q')
                        elif proxy.browser9.ele('x//input[@value="Verify you are human"]'):
                            proxy.browser9.ele('x//input[@value="Verify you are human"]').click
                            print('h')
                        else:
                            break
                    proxy.browser9.wait(5)
                else:
                    break
            except:
                proxy.browser9.quit()
                co.set_argument('--window-size', '80,60')
                co.set_local_port(9341)
                co.add_extension(r'proxy_switchyomega-2.5.20-an+fx')
                proxy.browser9 = ChromiumPage(co)
                
                proxy.browser9.get(url, retry=1)
                proxy.browser9.wait(30)
                for i in range(15):
                    if proxy.browser9.ele('x//*[text="确认您是真人"]'):
                        proxy.browser9.ele('x//*[text="确认您是真人"]').click(by_js=True)
                        print('q')
                    elif proxy.browser9.ele('x//input[@value="Verify you are human"]'):
                        proxy.browser9.ele('x//input[@value="Verify you are human"]').click
                        print('h')
                    else:
                        break
                proxy.browser9.wait(5)
        dfs9 = pd.read_excel('线程书架/线程9.xlsx', usecols=[0], header=None)
        try:
            url_list9 = dfs9.iloc[:, 0].tolist()
            difference9 = [x for x in book_url9 if x not in url_list9]
        except:
            difference9 = book_url9
        for i9, no9 in zip(difference9, tqdm(range(len(difference9)), desc="线程9爬取进度")):
            tab9 = proxy.browser9.new_tab()
            while 1 < 2:
                tab9.get(i9)
                soup9 = BeautifulSoup(tab9.html, 'lxml')
                book_temp9 = soup9.find(attrs={'class': 'list-body'})
                book_name_url9 = re.findall(r'href="(.*?)"', str(book_temp9), re.DOTALL)
                book_name9 = soup9.find(attrs={'style': 'font-size:20px'})
                if book_name9 is None:
                    tab9.wait(10)
                    continue
                else:
                    df9 = pd.DataFrame({
                        'Column1': [book_name9.text.strip()],
                        'Column2': [i9]
                    })

                    print(book_name9.text.strip())
                    break
            file_path_9 = f'TOC/{book_name9.text.replace("?", "").strip()}.xlsx'
            if os.path.exists(file_path_9):
                try:
                    dfs_9 = pd.read_excel(file_path_9, usecols=[0], header=None)
                except:
                    pass
            else:
                os.makedirs(os.path.dirname(file_path_9), exist_ok=True)
                dfs_empty = pd.DataFrame()
                dfs_empty.to_excel(file_path_9, index=False, header=False)
            try:
                url_list_9 = dfs_9.iloc[:, 0].tolist()
                difference_9 = [x for x in book_name_url9 if x not in url_list_9]
                if len(difference_9) == len(book_name_url9):
                    difference_9 = []
                else:
                    print(difference_9)
            except:
                difference_9 = book_name_url9
            for j9 in difference_9:
                while mini9 < max9:
                    try:
                        tab9 = proxy.browser9.new_tab()
                        tab9.get(j9)
                        soup19 = BeautifulSoup(tab9.html, 'lxml')
                        book_temp19 = soup19.find(attrs={'itemprop': 'articleBody'})
                        book_name_con9 = soup19.find(attrs={'class': 'toon-title'})
                        aname9 = book_name_con9.text.replace("/", ".").replace(":", ".").replace("?", "").replace("<", "").strip()
                        tab9.close()
                        print(aname9)
                        book_con9 = \
                            re.findall('<div class="view-img">\n</div>\n<div class=".*?">(.*?)</div>', str(book_temp19),
                                       re.DOTALL)[0]
                        soup29 = BeautifulSoup(book_con9, 'lxml')
                        soup29_ = soup29.find_all('p')
                        break
                    except:
                        proxy.browser9.quit()
                        co.set_argument('--window-size', '80,60')
                        co.set_local_port(9341)
                        co.add_extension(r'proxy_switchyomega-2.5.20-an+fx')
                        proxy.browser9 = ChromiumPage(co)
                        
                        proxy.browser9.get(url, retry=1)
                        proxy.browser9.wait(30)
                        for i in range(15):
                            if proxy.browser9.ele('x//*[text="确认您是真人"]'):
                                proxy.browser9.ele('x//*[text="确认您是真人"]').click(by_js=True)
                                print('q')
                            elif proxy.browser9.ele('x//input[@value="Verify you are human"]'):
                                proxy.browser9.ele('x//input[@value="Verify you are human"]').click
                                print('h')
                            else:
                                break
                        proxy.browser9.wait(5)

                file_path9 = f'book_all/{book_name9.text.strip()}/{aname9}.txt'
                os.makedirs(os.path.dirname(file_path9), exist_ok=True)
                with open(file_path9, 'a', encoding='utf-8') as file:
                    for soup2_9 in soup29_:
                        file.write(f'{soup2_9.get_text()}\n')
                dfsj9 = pd.DataFrame({
                    'Column1': [j9],
                    'Column2': [aname9]
                })
                with pd.ExcelWriter(file_path_9, engine='openpyxl', mode='a',
                                    if_sheet_exists='overlay') as writer:
                    if 'Sheet1' in writer.sheets:
                        startrow = writer.sheets['Sheet1'].max_row + 2
                    else:
                        startrow = 0  # 如果工作表不存在，从第0行开始写入
                    dfsj9.to_excel(writer, index=False, header=False, engine='openpyxl', sheet_name='Sheet1',
                                   startrow=startrow)
                print(f'book_all/{book_name9.text.replace(":", ".").strip()}/{aname9}.txt,已下载')
            name(df=df9)
            shujia(df9, file_path='线程9.xlsx')
            tab9.close()
    elif colist == 10:
        proxy.browser10.get(url, retry=1)
        print('30')
        proxy.browser10.wait(30)
        for i in range(15):
            if proxy.browser10.ele('x//*[text="确认您是真人"]'):
                proxy.browser10.ele('x//*[text="确认您是真人"]').click(by_js=True)
                print('q')
            elif proxy.browser10.ele('x//input[@value="Verify you are human"]'):
                proxy.browser10.ele('x//input[@value="Verify you are human"]').click
                print('h')
            else:
                break
        proxy.browser10.wait(5)
        max10 = 50
        mini10 = 1
        while mini10 < max10:
            try:
                book_url10 = re.findall(r'class="in-lable trans-bg-black"><a href="(.*?)">', proxy.browser10.html, re.DOTALL)
                if book_url10 == []:
                    print('网站能过，但未获取到信息')
                    proxy.browser10.quit()
                    co.set_argument('--window-size', '80,60')
                    co.set_local_port(9342)
                    co.set_argument(
                        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36')
                    # co.set_argument('--no-sandbox')
                    co.add_extension(r'proxy_switchyomega-2.5.20-an+fx')
                    proxy.browser10 = ChromiumPage(co)

                    proxy.browser10.get(url, retry=1)
                    print('30')
                    proxy.browser10.wait(30)
                    for i in range(15):
                        if proxy.browser10.ele('x//*[text="确认您是真人"]'):
                            proxy.browser10.ele('x//*[text="确认您是真人"]').click()
                            print('q')
                        elif proxy.browser10.ele('x//input[@value="Verify you are human"]'):
                            proxy.browser10.ele('x//input[@value="Verify you are human"]').click()
                            print('h')
                        else:
                            break
                    proxy.browser10.wait(10)
                else:
                    break
            except:
                print('网站未过')
                proxy.browser10.quit()
                # co.headless()
                co.set_argument('--window-size', '80,60')
                co.set_local_port(9342)
                co.set_argument(
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36')
                co.set_argument('--no-sandbox')
                co.add_extension(r'proxy_switchyomega-2.5.20-an+fx')
                proxy.browser10 = ChromiumPage(co)

                proxy.browser10.get(url, retry=1)
                proxy.browser10.wait(30)
                for i in range(15):
                    if proxy.browser10.ele('x//*[text="确认您是真人"]'):
                        proxy.browser10.ele('x//*[text="确认您是真人"]').click()
                    elif proxy.browser10.ele('x//input[@value="Verify you are human"]'):
                        proxy.browser10.ele('x//input[@value="Verify you are human"]').click()
                    else:
                        break

                proxy.browser10.wait(10)
        dfs10 = pd.read_excel('线程书架/线程10.xlsx', usecols=[0], header=None)
        try:
            url_list10 = dfs10.iloc[:, 0].tolist()
            difference10 = [x for x in book_url10 if x not in url_list10]
        except:
            difference10 = book_url10
        for i10, no10 in zip(difference10, tqdm(range(len(difference10)), desc="线程10爬取进度")):
            tab10 = proxy.browser10.new_tab()
            while 1 < 2:
                tab10.get(i10)
                soup10 = BeautifulSoup(tab10.html, 'lxml')
                book_temp10 = soup10.find(attrs={'class': 'list-body'})
                book_name_url10 = re.findall(r'href="(.*?)"', str(book_temp10), re.DOTALL)
                book_name10 = soup10.find(attrs={'style': 'font-size:20px'})
                if book_name10 is None:
                    tab10.wait(10)
                    continue
                else:
                    df10 = pd.DataFrame({
                        'Column1': [book_name10.text.strip()],
                        'Column2': [i10]
                    })
                    print(book_name10.text.strip())
                    break
            file_path_10 = f'TOC/{book_name10.text.replace("?", "").strip()}.xlsx'
            if os.path.exists(file_path_10):
                try:
                    dfs_10 = pd.read_excel(file_path_10, usecols=[0], header=None)
                except:
                    pass
            else:
                os.makedirs(os.path.dirname(file_path_10), exist_ok=True)
                dfs_empty = pd.DataFrame()
                dfs_empty.to_excel(file_path_10, index=False, header=False)
            try:
                url_list_10 = dfs_10.iloc[:, 0].tolist()
                difference_10 = [x for x in book_name_url10 if x not in url_list_10]
                if len(difference_10) == len(book_name_url10):
                    difference_10 = []
                    print(difference_10)
                else:
                    print(difference_10)
            except:
                print('这是一本新书')
                difference_10 = book_name_url10
            for j10 in difference_10:
                while mini10 < max10:
                    try:
                        tab10 = proxy.browser10.new_tab()
                        tab10.get(j10)
                        soup110 = BeautifulSoup(tab10.html, 'lxml')
                        book_temp110 = soup110.find(attrs={'itemprop': 'articleBody'})
                        book_name_con10 = soup110.find(attrs={'class': 'toon-title'})
                        aname10 = book_name_con10.text.replace("/", ".").replace(":", ".").replace("?", "").replace("<", "").replace(">", "").strip()
                        tab10.close()
                        print(aname10)
                        book_con10 = \
                            re.findall('<div class="view-img">\n</div>\n<div class=".*?">(.*?)</div>',
                                       str(book_temp110),
                                       re.DOTALL)[0]
                        soup210 = BeautifulSoup(book_con10, 'lxml')
                        soup210_ = soup210.find_all('p')
                        break
                    except:
                        proxy.browser10.quit()
                        # co.headless()
                        co.set_argument('--window-size', '80,60')
                        co.set_local_port(9342)
                        co.set_argument(
                            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36')
                        co.set_argument('--no-sandbox')
                        co.add_extension(r'proxy_switchyomega-2.5.20-an+fx')
                        proxy.browser10 = ChromiumPage(co)

                        proxy.browser10.get(url, retry=1)
                        proxy.browser10.wait(30)
                        for i in range(15):
                            if proxy.browser10.ele('x//*[text="确认您是真人"]'):
                                proxy.browser10.ele('x//*[text="确认您是真人"]').click()
                            elif proxy.browser10.ele('x//input[@value="Verify you are human"]'):
                                proxy.browser10.ele('x//input[@value="Verify you are human"]').click()
                            else:
                                break
                        proxy.browser10.wait(10)


                file_path10 = f'book_all/{book_name10.text.strip()}/{aname10}.txt'
                os.makedirs(os.path.dirname(file_path10), exist_ok=True)
                with open(file_path10, 'a', encoding='utf-8') as file:
                    for soup2_10 in soup210_:
                        file.write(f'{soup2_10.get_text()}\n')
                dfsj10 = pd.DataFrame({
                    'Column1': [j10],
                    'Column2': [aname10]
                })
                with pd.ExcelWriter(file_path_10, engine='openpyxl', mode='a',
                                    if_sheet_exists='overlay') as writer:
                    if 'Sheet1' in writer.sheets:
                        startrow = writer.sheets['Sheet1'].max_row + 2
                    else:
                        startrow = 0  # 如果工作表不存在，从第0行开始写入
                    dfsj10.to_excel(writer, index=False, header=False, engine='openpyxl', sheet_name='Sheet1',
                                    startrow=startrow)
                print(f'book_all/{book_name10.text.replace(":", ".").strip()}/{aname10}.txt,已下载')
            name(df=df10)
            shujia(df10, file_path='线程10.xlsx')
            tab10.close()

if __name__ == "__main__":
    book(url="https://booktoki349.com/novel/p10?book=%EC%9D%BC%EB%B0%98%EC%86%8C%EC%84%A4|1")