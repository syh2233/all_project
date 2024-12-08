import re
import os
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
    if colist == 10:
        proxy.browser10.get(url, retry=1)
        print('30')
        proxy.browser10.wait(30)
        for i in range(15):
            if proxy.browser10.ele('x//input[@name="cf-turnstile-response"]'):
                proxy.browser10.ele('x//input[@name="cf-turnstile-response"]').click(by_js=True)
                print('q')
            elif proxy.browser10.ele('x//input[@value="Verify you are human"]'):
                proxy.browser10.ele('x//input[@value="Verify you are human"]').click
                print('h')
            else:
                break
        print(proxy.browser10.html)
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
                    # proxy.proxy_pool(colist=10)
                    proxy.browser10.get(url, retry=1)
                    print('30')
                    proxy.browser10.wait(30)
                    for i in range(15):
                        if proxy.browser10.ele('x//input[@name="cf-turnstile-response"]'):
                            proxy.browser10.ele('x//input[@name="cf-turnstile-response"]').click()
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
                # proxy.proxy_pool(colist=10)
                proxy.browser10.get(url, retry=1)
                proxy.browser10.wait(2)
                for i in range(15):
                    if proxy.browser10.ele('x//input[@name="cf-turnstile-response"]'):
                        proxy.browser10.ele('x//input[@name="cf-turnstile-response"]').click()
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
                        aname10 = book_name_con10.text.replace("/", ".").replace(":", ".").replace("?", "").replace("<",
                                                                                                                    "").replace(
                            ">", "").strip()
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
                        # proxy.proxy_pool(colist=10)
                        proxy.browser10.get(url, retry=1)
                        proxy.browser10.wait(2)
                        for i in range(15):
                            if proxy.browser10.ele('x//input[@type="checkbox"]'):
                                proxy.browser10.ele('x//input[@type="checkbox"]').click()
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
    book(url="https://booktoki349.com/novel/p10?book=%EC%9D%BC%EB%B0%98%EC%86%8C%EC%84%A4|10")