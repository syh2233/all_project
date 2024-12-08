from DrissionPage import ChromiumPage, ChromiumOptions
import pygame
import xas
import time

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('11.mp3')
co = ChromiumOptions().set_paths()
co.set_timeouts(6, 6, 6)
co.add_extension(r'C:\Users\沈家\Downloads\proxy_switchyomega-2.5.20-an+fx')
browser = ChromiumPage(co)
browser.get('https://kyfw.12306.cn/otn/resources/login.html')
input('请登录，登录完回车')
browser.get('https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc')
browser.ele('@aria-label:请输入或选择出发站，按回车确认输入').clear()
browser.ele('@aria-label:请输入或选择目的地站，按回车确认输入').clear()
browser.ele('@aria-label:请输入日期，例如2021杠01杠01').clear()
Begin = input('请设置出发点，回车\n')
Begin = f"{Begin}"
browser.ele('@aria-label:请输入或选择出发站，按回车确认输入').input(Begin)
end = input('请设置到达点，回车\n')
end = f"{end}"
browser.ele('@aria-label:请输入或选择目的地站，按回车确认输入').input(end)
aa = input('请输入日期，格式例如2021—01—01\n')
aa = f"{aa}"
for i in range(50):
    try:
        browser.ele('@aria-label:请输入日期，例如2021杠01杠01').input(aa)
        break
    except:
        print('该日期未开售')
times = input('请选择时间点:a:"00:00-24:00",b:"00:00-06:00",c:"06:00-12:00",d:"12:00-18:00",e:"18:00-24:00"\n')
if times == "a" or times == 'A':
    times_new = "00:00--24:00"
elif times == "b" or times == 'B':
    times_new = "00:00--06:00"
elif times == 'c' or times == 'C':
    times_new = "06:00--12:00"
elif times == 'd' or times == 'D':
    times_new = "12:00--18:00"
elif times == 'e' or times == 'E':
    times_new = "18:00--24:00"
times_new1 = f"{times_new}"
for i in range(3000):
    try:
        browser.get('https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc')
        try:
            browser.ele(f'x://option[text()="{times_new1}"]').click(by_js=True)
        except:
            xas.proxy_pool(colist=1)
            browser.get('https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc')
            browser.ele('@aria-label:请输入或选择出发站，按回车确认输入').input(Begin)
            browser.ele('@aria-label:请输入或选择目的地站，按回车确认输入').input(end)
            browser.ele('@aria-label:请输入日期，例如2021杠01杠01').input(aa)
            # browser.ele(f'x://option[text()="{times_new1}"]').click(by_js=True)
        browser.ele('@id:query_ticket').click(by_js=True)
        browser.ele(f'@id:cc_from_station_{end}').click(by_js=True)
        browser.ele(f'@id:cc_to_station_{Begin}_check').click(by_js=True)
        time.sleep(1)
        con = browser.ele('@class:t-list transfer-ticket-list').html
        browser.ele('x://a[text()="预订"]').click(by_js=True, timeout=1)
        print(con)
        break
    except:
        i += 1
        print(f'失败{i}')
        continue
print("成功")
browser.ele('@aria-label:按空格键进行操作,按空格键进行操作').click(by_js=True)
browser.ele('x://a[text()="提交订单"]').click(by_js=True)
pygame.mixer.music.play()
input('请手动选择座位并确认,并去付钱')
while pygame.mixer.music.get_busy():  # 当音乐还在播放时
    pygame.times.Clock().tick(10)

