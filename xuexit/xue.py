from DrissionPage import ChromiumPage, ChromiumOptions
import schedule
import time


def job():
    co = ChromiumOptions().set_paths()
    # co.headless()
    co.set_timeouts(6, 6, 6)
    browser = ChromiumPage(co)
    while 1 < 2:
        browser.get(
            'https://mooc2-ans.chaoxing.com/mooc2-ans/mycourse/stu?courseid=236266580&clazzid=102479311&cpi=412833606&enc=f6828dff76190511f330f92e8b25120e&t=1725374880034&pageHeader=0&v=2')
        browser.ele('@class:right-content').click(by_js=False)
        try:
            print(browser.ele('@class:sign-title fontBold colorDeep').text)
            break
        except:
            continue
    # browser.quit()


if __name__ == '__main__':
    schedule.every().day.at("16:00").do(job)
    schedule.every().day.at("22:13").do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)
