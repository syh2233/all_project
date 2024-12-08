from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
from lxml import etree
import pandas as pd
import time

url = "https://uland.taobao.com/sem/tbsearch"

chrome_options = Options()
chrome_options.binary_location = r'C:\Users\沈家\Documents\WeChat Files\wxid_5jlamuqhhcju22\FileStorage\File\2024-11\chrome-win64\chrome-win64\chrome.exe'  # 这里设置你的Chrome可执行文件的路径

service = Service(r'C:\Users\沈家\Documents\WeChat Files\wxid_5jlamuqhhcju22\FileStorage\File\2024-11\chromedriver-win64\chromedriver-win64\chromedriver.exe')
browser = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(browser, 10)

browser.get(url)
# print(browser.page_source)

def craw_keyword(keyword, page_num):
    # 获取page_num页的keyword物品信息
    browser.find_element(By.XPATH, '//*[text()="亲，请登录"]').click()
    a = input("登录后回车")
    input1 = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="q"]')))
    input1.send_keys(keyword)
    sousu_btn = browser.find_element(By.CLASS_NAME, 'btn-search')
    sousu_btn.click()
    time.sleep(2)
    flag = True
    count = 0
    imgs = []
    titles = []
    priceInts = []
    priceFloats = []
    place1s = []
    place2s = []
    storenames = []
    while flag:
        # 模拟人进行浏览
        for i in range(1, 8):
            browser.execute_script(f'window.scrollTo(0, {i * 1000 - 500})')
            time.sleep(0.5)
        etree_html = etree.HTML(browser.page_source)
        # 获取信息
        img = etree_html.xpath('//*[@id="search-content-leftWrap"]/div[2]/div[1]/div/a[7]/div/div[1]/div[1]/img/@src')
        title = etree_html.xpath('//*[@id="search-content-leftWrap"]/div[2]/div[1]/div/a[7]/div/div[1]/div[2]/div/span/text()')
        priceInt = etree_html.xpath('//*[@id="search-content-leftWrap"]/div[2]/div[1]/div/a[7]/div/div[1]/div[4]/div[1]/span[1]/text()')
        priceFloat = etree_html.xpath('//*[@id="search-content-leftWrap"]/div[2]/div[1]/div/a[7]/div/div[1]/div[4]/div[1]/span[2]/text()')
        place1 = etree_html.xpath('//*[@id="search-content-leftWrap"]/div[2]/div[1]/div/a[7]/div/div[1]/div[4]/div[2]/span/text()')
        place2 = etree_html.xpath('//*[@id="search-content-leftWrap"]/div[2]/div[1]/div/a[7]/div/div[1]/div[4]/div[3]/span/text()')
        storename = etree_html.xpath('//*[@id="search-content-leftWrap"]/div[2]/div[1]/div/a[7]/div/div[3]/div/a/text()')
        imgs.extend(img)
        titles.extend(title)
        priceInts.extend(priceInt)
        priceFloats.extend(priceFloat)
        place1s.extend(place1)
        place2s.extend(place2)
        storenames.extend(storename)
        # 点击下一页
        next_page = browser.find_element(By.XPATH, '//*[@id="pageContent"]/div[1]/div[2]/div[2]/div[1]/div/button[2]')
        next_page.click()
        time.sleep(5)
        count += 1
        if count >= page_num:
            flag = False
            break
    return imgs, titles, priceInts, priceFloats, place1s, place2s, storenames

if __name__ == '__main__':
    keyword = "笔记本电脑"  # 关键词
    pages = 5  # 获取几页的数据
    imgs, titles, priceInts, priceFloats, place1s, place2s, storenames = craw_keyword(keyword, pages)
    data = pd.DataFrame({"img_url": imgs,
                         "titles": titles,
                         "priceInt": priceInts,
                         "priceFloats": priceFloats,
                         "place1s": place1s,
                         "storenames": storenames,
                         })
    data.to_csv('taobao.csv', index=False, encoding='utf-8')