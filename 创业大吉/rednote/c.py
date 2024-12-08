import time
import proxy2
from DrissionPage import ChromiumPage, ChromiumOptions


def ip():
    while 1 < 2:
        co = ChromiumOptions().set_paths()
        co.set_argument('--window-size', '80,60')
        co.set_timeouts(6, 6, 6)
        co.set_local_port(9445)
        browser = ChromiumPage(co)
        try:
            browser.get('https://www.zhihu.com/', retry=1, timeout=3)
            if browser.ele('@text():403 Forbidden'):
                print('代理403')
                browser.quit()
                proxy2.main()
                continue
            browser.ele('@class:css-1hlrcxk')
            browser.quit()
            print('代理当前可用')
            time.sleep(600)
        except:
            browser.quit()
            print('代理未过反爬')
            proxy2.main()


if __name__ == "__main__":
    ip()