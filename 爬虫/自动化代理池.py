import platform

from DrissionPage import ChromiumPage, ChromiumOptions
from loguru import logger


def switch_ip(ip_port=None):
    global set_proxy
    if ip_port:
        # 设置proxy
        ip, port = ip_port.split(":")
        tab = browser.new_tab()
        tab.get("chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy")
        tab.ele('x://input[@ng-model="proxyEditors[scheme].host"]').input(ip, clear=True)
        tab.ele('x://input[@ng-model="proxyEditors[scheme].port"]').input(port, clear=True)
        tab.ele('@class:glyphicon glyphicon-lock').click()
        tab.ele('@ng-model:model').input('LV16795954-LV1659893070-20', clear=True)
        tab.ele('@name:password').input('122d4e1c86', clear=True)
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
co.set_local_port(9211)
# 1、设置switchyOmega插件
co.add_extension(r'C:\Users\沈家\Downloads\proxy_switchyomega-2.5.20-an+fx')
browser = ChromiumPage(co)

# 2、重置switchyOmega插件
omega_proxy = False
switch_ip()
browser.get("https://www.ip138.com/", retry=0)
html_text = browser.get_frame('x://div[@class="hd"]//iframe').ele('text:您的iP地址是').text
logger.success(f">>>>当前的ip {html_text}")

# 3、随机切换代理ip
ip_all = [{"ip": "174.138.174.154", "port": 7383, "username": "LV16795954-LV1659893070-20"}]
for ips in ip_all:
    logger.info(f"~~~切换ip，now {ips['ip']}")
    # 重置switchyOmega插件
    switch_ip(f"{ips['ip']}:{ips['port']}")
    browser.wait(1)
    try:
        # browser.get("https://www.baidu.com/", retry=0)
        browser.get("https://www.ip38.com/", retry=0)
        # browser.get("https://www.google.com/", retry=0)
        html_text = browser.get_frame('x://div[@class="hd"]//iframe').ele('text:您的iP地址是').text
        logger.success(f">>>>>>>>切换代理成功 {html_text}")
    except Exception as err:
        logger.error(f"----------切换代理失败 dp {err}")
    browser.wait(10)
browser.quit()