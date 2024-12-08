from DrissionPage import ChromiumPage, ChromiumOptions

co = ChromiumOptions()
# co.headless()
browser = ChromiumPage(co)
for i in range(30000):
    browser.get('http://www.baidu.com')
    tab = browser.new_tab()
    tab.get('https://message.bilibili.com/?spm_id_from=333.1007.0.0#/reply')
    tab.ele('@class:action-button').click(by_js=type)
    tab.wait(3)
    tab.ele('@name:reply-box').input('纯你牛魔，nt' + str(i))
    tab.wait(10)
    tab.ele('@class:send-button').click(by_js=type)
    tab.close()
    print(f'已发{i}')