
from DrissionPage import ChromiumPage, ChromiumOptions
from bs4 import BeautifulSoup
import re
from tqdm import tqdm
import threading
from collections import OrderedDict
import schedule
import time


class StoppableThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def ll(mo):
        global browser
        co = ChromiumOptions().set_paths()
        co.set_local_port(mo)
        # co.headless()
        browser = ChromiumPage(co)
        return browser

    def convert_time_to_seconds(time_str):
        minutes, seconds = map(int, time_str.split(':'))
        return minutes * 60 + seconds

    def run(self):
        global browser
        list1 = ["双眼皮"]
        list3 = []
        for kh, p in zip(list1, tqdm(range(len(list1)), desc="线程1爬取进度")):
            if not self._stop_event.is_set():
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
                time.sleep(1)
                for j in range(30):
                    if not self._stop_event.is_set():
                        soup = BeautifulSoup(browser.html, 'lxml')
                        b = soup.findAll(attrs={"class": "title"})
                        aa = re.findall(r'<span data-v-.*?="" data-v-.*?="">(.*?)</span>', str(b), re.DOTALL)
                        unique_urls = list(OrderedDict.fromkeys(aa))
                        difference1 = [x for x in unique_urls if x not in list3]
                        for i in difference1:
                            if not self._stop_event.is_set():
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
                                        print(StoppableThread.convert_time_to_seconds(kk[0]))
                                    except:
                                        kk = ['00:00']
                                    if j % 5 == 0:
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
                                    time.sleep(StoppableThread.convert_time_to_seconds(kk[0]))
                                    try:
                                        browser.ele('@class:close-box').click(by_js=True)
                                    except:
                                        continue
                        browser.scroll.to_bottom()
                        time.sleep(0.3)


class StoppableThread_1(threading.Thread):
    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def ll1(mo):
        global browser1
        co = ChromiumOptions().set_paths()
        co.set_local_port(mo)
        # co.headless()
        browser1 = ChromiumPage(co)
        return browser1

    def run(self):
        global browser1
        list1_1 = ["叶黄素"]
        list3 = []
        for kh_1, p in zip(list1_1, tqdm(range(len(list1_1)), desc="线程2爬取进度")):
            if not self._stop_event.is_set():
                browser1.get("https://www.xiaohongshu.com/explore")
                try:
                    browser1.ele("@id:search-input").clear()
                except:
                    while 1 < 2:
                        if browser1.ele('@class:active'):
                            print("已过")
                            break
                        else:
                            time.sleep(60)
                            continue
                browser1.ele("@id:search-input").input(kh_1)
                browser1.ele("@class:search-icon").click(by_js=False)
                time.sleep(1)
                for j_1 in range(30):
                    if not self._stop_event.is_set():
                        soup_1 = BeautifulSoup(browser1.html, 'lxml')
                        b_1 = soup_1.findAll(attrs={"class": "title"})
                        aa_1 = re.findall(r'<span data-v-.*?="" data-v-.*?="">(.*?)</span>', str(b_1), re.DOTALL)
                        unique_urls_1 = list(OrderedDict.fromkeys(aa_1))
                        difference1_1 = [x for x in unique_urls_1 if x not in list3]
                        for i_1 in difference1_1:
                            if not self._stop_event.is_set():
                                time.sleep(1)
                                list3.append(i_1)
                                print(i_1)
                                if '<img src=' in str(i_1):
                                    continue
                                else:
                                    browser1.ele(f'x://span[text()="{i_1}"]').click(by_js=True)
                                    if browser1.ele('@class:no-comments-text'):
                                        browser1.ele('@class:close-box').click(by_js=True)
                                        continue
                                    try:
                                        kk_1 = re.findall(
                                            r'<span class="xgplayer-time-current">.*?</span><span>(.*?)</span>',
                                            str(browser1.ele('@class:xgplayer-time').html), re.DOTALL)
                                        print(StoppableThread.convert_time_to_seconds(kk_1[0]))
                                    except:
                                        kk_1 = ['00:00']
                                    if j_1 % 5 == 0:
                                        try:
                                            browser1.ele('x://span[text()="关注"]').click(by_js=True)
                                            try:
                                                browser1.ele('x://span[text()="说点什么..."]').input('受教了，谢谢美女')
                                                browser1.ele('x://button[text()="发送"]').click(by_js=True)
                                            except:
                                                print("未完成评论")
                                            browser1.ele('@@class:like-lottie@@style:width: 24px; height: 24px;').click(
                                                by_js=True)
                                        except:
                                            print('已关注')
                                    for k in range(300):
                                        browser1.ele('@class:note-scroller').scroll.to_bottom()
                                        if browser1.ele('@class:end-container'):
                                            break
                                    time.sleep(StoppableThread.convert_time_to_seconds(kk_1[0]))
                                    try:
                                        browser1.ele('@class:close-box').click(by_js=True)
                                    except:
                                        continue
                        browser1.scroll.to_bottom()
                        time.sleep(0.3)


class StoppableThread_2(threading.Thread):
    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def ll2(mo):
        global browser2
        co = ChromiumOptions().set_paths()
        co.set_local_port(mo)
        # co.headless()
        browser2 = ChromiumPage(co)
        return browser2

    def run(self):
        global browser2
        list1_2 = ["化妆"]
        list3 = []
        for kh_2, p in zip(list1_2, tqdm(range(len(list1_2)), desc="线程3爬取进度")):
            if not self._stop_event.is_set():
                browser2.get("https://www.xiaohongshu.com/explore")
                # try:
                #     browser1.ele("@id:search-input").clear()
                # except:
                #     while 1 < 2:
                #         if browser1.ele('@class:active'):
                #             print("已过")
                #             break
                #         else:
                #             time.sleep(60)
                #             continue
                # browser1.ele("@id:search-input").input(kh)
                # browser1.ele("@class:search-icon").click(by_js=False)
                time.sleep(1)
                for j_2 in range(30):
                    if not self._stop_event.is_set():
                        soup_2 = BeautifulSoup(browser2.html, 'lxml')
                        b_2 = soup_2.findAll(attrs={"class": "title"})
                        aa_2 = re.findall(r'<span data-v-.*?="" data-v-.*?="">(.*?)</span>', str(b_2), re.DOTALL)
                        unique_urls_2 = list(OrderedDict.fromkeys(aa_2))
                        difference1_2 = [x for x in unique_urls_2 if x not in list3]
                        for i_2 in difference1_2:
                            if not self._stop_event.is_set():
                                time.sleep(1)
                                list3.append(i_2)
                                print(i_2)
                                if '<img src=' in str(i_2):
                                    continue
                                else:
                                    browser2.ele(f'x://span[text()="{i_2}"]').click(by_js=True)
                                    if browser2.ele('@class:no-comments-text'):
                                        browser2.ele('@class:close-box').click(by_js=True)
                                        continue
                                    try:
                                        kk_2 = re.findall(
                                            r'<span class="xgplayer-time-current">.*?</span><span>(.*?)</span>',
                                            str(browser2.ele('@class:xgplayer-time').html), re.DOTALL)
                                        print(StoppableThread.convert_time_to_seconds(kk_2[0]))
                                    except:
                                        kk_2 = ['00:00']
                                    if j_2 % 5 == 0:
                                        try:
                                            browser2.ele('x://span[text()="关注"]').click(by_js=True)
                                            try:
                                                browser2.ele('x://span[text()="说点什么..."]').input('受教了，谢谢美女')
                                                browser2.ele('x://button[text()="发送"]').click(by_js=True)
                                            except:
                                                print("未完成评论")
                                            browser2.ele('@@class:like-lottie@@style:width: 24px; height: 24px;').click(
                                                by_js=True)
                                        except:
                                            print('已关注')
                                    for k in range(300):
                                        browser2.ele('@class:note-scroller').scroll.to_bottom()
                                        if browser2.ele('@class:end-container'):
                                            break
                                    time.sleep(StoppableThread.convert_time_to_seconds(kk_2[0]))
                                    try:
                                        browser2.ele('@class:close-box').click(by_js=True)
                                    except:
                                        continue
                        browser2.scroll.to_bottom()
                        time.sleep(0.3)


def drive_state():
    thread_1 = StoppableThread.ll(mo=ilp)


def drive_state1():
    thread_2 = StoppableThread.ll1(mo=ilp1)


def drive_state2():
    thread_3 = StoppableThread.ll2(mo=ilp2)


def state_run(list1):
    global ilp
    for ilp in list1:
        thread_1 = StoppableThread.ll(mo=ilp)
        thread = StoppableThread()
        thread.start()

        # 设置定时器
        timer = threading.Timer(1800, thread.stop)
        timer.start()

        # 等待定时器结束
        timer.join()
        thread.join()


def settime():
    global yy
    yy = 2000


def function1():
    global browser
    settime()
    # 创建并启动线程
    list1 = [9712, 9710, 9707, 9706, 9705, 9704]
    # for i in range(9704, 9711):
    #     list1.append(i)
    global ilp
    for ilp in list1:
        thread_1 = StoppableThread.ll(mo=ilp)
        thread = StoppableThread()
        thread.start()

        # 设置定时器
        timer = threading.Timer(yy, thread.stop)
        timer.start()

        # 等待定时器结束
        timer.join()
        thread.join()
        browser.quit()


def function2():
    global browser1
    settime()
    # 创建并启动线 叶黄素
    list1 = [9739, 9740, 9737, 9736, 9735, 9704, 9718, 9742, 9738, 9741]
    # list1 = []
    # for i in range(9737, 9742):
    #     list1.append(i)
    global ilp1
    for ilp1 in list1:
        thread_1 = StoppableThread_1.ll1(mo=ilp1)
        thread_2 = StoppableThread_1()
        thread_2.start()

        # 设置定时器
        timer = threading.Timer(yy, thread_2.stop)
        timer.start()

        # 等待定时器结束
        timer.join()
        thread_2.join()
        browser1.quit()


def function3():
    global browser2
    settime()
    list1 = []
    for i in range(9742, 9752):
        list1.append(i)
    global ilp2
    for ilp2 in list1:
        thread_1 = StoppableThread_2.ll2(mo=ilp2)
        thread = StoppableThread_2()
        thread.start()

        # 设置定时器
        timer = threading.Timer(yy, thread.stop)
        timer.start()

        # 等待定时器结束
        timer.join()
        thread.join()
        browser2.quit()



def job():
    thread1 = threading.Thread(target=function1)
    thread2 = threading.Thread(target=function2)
    thread3 = threading.Thread(target=function3)

    # 启动线程
    thread1.start()
    thread2.start()
    thread3.start()

    # 等待线程结束
    thread1.join()
    thread2.join()
    thread3.join()


def time_state():
    schedule.every().day.at("09:00").do(job)
    # schedule.every().day.at("12:00").do(job)
    # schedule.every().day.at("21:00").do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    time_state()
