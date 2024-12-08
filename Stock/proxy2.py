list1 = ['174.138.174.154:7383:LV16795954-LV1659893070-20:122d4e1c86',
'174.138.174.154:7383:LV16795954-LV1659893070-21:122d4e1c86',
'174.138.174.154:7383:LV16795954-LV1659893070-22:122d4e1c86',
'174.138.174.154:7383:LV16795954-LV1659893070-23:122d4e1c86',
'174.138.174.154:7383:LV16795954-LV1659893070-24:122d4e1c86',
'174.138.174.154:7383:LV16795954-LV1659893070-25:122d4e1c86',
'174.138.174.154:7383:LV16795954-LV1659893070-26:122d4e1c86',
'174.138.174.154:7383:LV16795954-LV1659893070-27:122d4e1c86',
'174.138.174.154:7383:LV16795954-LV1659893070-28:122d4e1c86',
'174.138.174.154:7383:LV16795954-LV1659893070-29:122d4e1c86',
'174.138.174.154:7383:LV16795954-LV1659893070-30:122d4e1c86']
import platform
import random
from DrissionPage import ChromiumPage, ChromiumOptions
from loguru import logger


def switch_ip(ips=None):
    global set_proxy
    if ips:
        # 设置proxy
        ip, port, username, password = ips.split(":")
        tab = browser.new_tab()
        tab.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy")
        tab.ele('x://input[@ng-model="proxyEditors[scheme].host"]').input(ip, clear=True)
        tab.ele('x://input[@ng-model="proxyEditors[scheme].port"]').input(port, clear=True)
        tab.ele('@class:glyphicon glyphicon-lock').click()
        tab.ele('@ng-model:model').input(username, clear=True)
        tab.ele('@name:password').input(password, clear=True)
        tab.ele('@class:btn btn-primary ng-binding').click()
        tab.wait(1)
        tab.ele('x://a[@ng-click="applyOptions()"]').click()
        tab.wait(1)
        # 提示框
        txt = tab.handle_alert()
        print("提示框", txt)
        tab.handle_alert(accept=False)
        if not omega_proxy:
            # 切换proxy
            tab.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#")
            tab.wait(1)
            tab.ele('x://span[text()="proxy"]').click()
            set_proxy = True
    else:
        tab = browser.new_tab()
        tab.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/popup/index.html#")
        tab.ele('x://span[text()="[直接连接]"]').click()
    if len(browser.tab_ids) > 1:
        print("当前tab个数", len(browser.tab_ids))
        tab.close()

def aa(a):
    if platform.system().lower() == 'windows':
        # UA = ['1', '2']
        # a = random.choice(UA)
        # print(a)
        if a == 1:
            co = ChromiumOptions().set_paths(browser_path=r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
        else:
            co = ChromiumOptions().set_paths()
        # co.headless(True)
    else:
        co = ChromiumOptions().set_paths(browser_path=r"/opt/google/chrome/google-chrome")
        # co.headless(True)  # 设置无头加载  无头模式是一种在浏览器没有界面的情况下运行的模式，它可以提高浏览器的性能和加载速
        # co.incognito(True)  # 无痕隐身模式打开的话，不会记住你的网站账号密码的
        # co.set_argument('--no-sandbox')  # 禁用沙箱 禁用沙箱可以避免浏览器在加载页面时进行安全检查,从而提高加载速度 默认情况下，所有Chrome 用户都启用了隐私沙盒选项  https://zhuanlan.zhihu.com/p/475639754
        # co.set_argument("--disable-gpu")  # 禁用GPU加速可以避免浏览器在加载页面时使用过多的计算资源，从而提高加载速度
        UA = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36']
        user_agent_ip = random.choice(UA)
        co.set_user_agent(user_agent=user_agent_ip)  # 设置ua

    co.set_timeouts(6, 6, 6)
    random_port = random.randint(9333, 9337)
    co.set_local_port(random_port)
    # 1、设置switchyOmega插件
    co.add_extension(r'C:\Users\沈家\Downloads\proxy_switchyomega-2.5.20-an+fx')
    browser = ChromiumPage(co)
    return browser

if platform.system().lower() == 'windows':
    co = ChromiumOptions()  # .set_paths(browser_path=r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
else:
    co = ChromiumOptions().set_paths(browser_path=r"/opt/google/chrome/google-chrome")
    co.headless(True)  # 设置无头加载  无头模式是一种在浏览器没有界面的情况下运行的模式，它可以提高浏览器的性能和加载速
    # co.incognito(True)  # 无痕隐身模式打开的话，不会记住你的网站账号密码的
    co.set_argument('--no-sandbox')  # 禁用沙箱 禁用沙箱可以避免浏览器在加载页面时进行安全检查,从而提高加载速度 默认情况下，所有Chrome 用户都启用了隐私沙盒选项  https://zhuanlan.zhihu.com/p/475639754
    co.set_argument("--disable-gpu")  # 禁用GPU加速可以避免浏览器在加载页面时使用过多的计算资源，从而提高加载速度
    co.set_user_agent(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36')  # 设置ua

co.set_timeouts(6, 6, 6)
# random_port = random.randint(9211, 9213)
co.set_local_port(9333)
# 1、设置switchyOmega插件
co.add_extension(r'C:\Users\沈家\Downloads\proxy_switchyomega-2.5.20-an+fx')
browser = ChromiumPage(co)

# 2、重置switchyOmega插件
omega_proxy = False
switch_ip()
browser.get("https://ipinfo.io/", retry=0)
html_text = browser.ele('@class:text-green-05').text
logger.success(f">>>>当前的ip {html_text}")

# 3、随机切换代理ip
def proxy_pool():
    ips = random.choice(list1)
    print(ips)
    ip1, port1, username1, password1 = ips.split(":")
    logger.info(f"~~~切换ip，now {ip1}")
    # 重置switchyOmega插件
    switch_ip(ips)
    browser.wait(1)
    try:
        browser.get("https://www.baidu.com/", retry=0)
        # browser.get("https://ipinfo.io/", retry=0)
        # browser.get("https://www.google.com/", retry=0)
        # html_text = browser.ele('@class:text-green-05').text
        logger.success(f">>>>>>>>切换代理成功")
    except Exception as err:
        logger.error(f"----------切换代理失败 dp {err}")
# browser.quit()
