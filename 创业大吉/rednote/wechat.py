from wxauto import *
import schedule
import time


def job():
    wx = WeChat()
    wx.SendMsg('1001已完成', '物联1班班群')
    wx.SendMsg('@所有人 大家记得晚点名打卡', '1001')


if __name__ == '__main__':
    schedule.every().day.at("19:30").do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
