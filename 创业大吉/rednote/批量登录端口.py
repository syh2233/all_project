import pygame
import time

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('14.mp3')
from appium import webdriver
from selenium.webdriver.common.by import By
from appium.webdriver.extensions.android.nativekey import AndroidKey
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options

desired_caps = {
  'a': {'platformName': 'Android',  # 被测手机是安卓
   'platformVersion': '10',  # 手机安卓版本，如果是鸿蒙系统，依次尝试 12、11、10 这些版本号
   'deviceName': 'xxx',  # 设备名，安卓手机可以随意填写
   'appPackage': 'com.qihoo.magic.dMHa45ibpdmbphnLt92Yk_106',  # 启动APP Package名称
   'appActivity': 'com.qihoo.magic.plugin.AppEnterActivity',  # 启动Activity名称
   'unicodeKeyboard': True,  # 自动化需要输入中文时填True
   'resetKeyboard': True,  # 执行完程序恢复原来输入法
   'noReset': True,  # 不要重置App
   'newCommandTimeout': 6000,
   'automationName': 'UiAutomator2'},
   # 'app': r'd:\apk\bili.apk',
}
list1 = ['a']
for i in list1:
    print(desired_caps[i])
    # 连接Appium Server，初始化自动化环境
    driver = webdriver.Remote('http://localhost:4723/wd/hub', options=UiAutomator2Options().load_capabilities(desired_caps[i]))

    # 设置缺省等待时间
    driver.implicitly_wait(30)

    driver.find_element(By.ID, 'com.xingin.xhs:id/iby').click()
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, '设置').click()
    driver.swipe(start_x=101, start_y=1000, end_x=101, end_y=100, duration=80)
    # driver.find_element(By.ID, 'com.xingin.xhs:id/axk').click()
    driver.find_element(AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[10]/android.view.ViewGroup/android.widget.TextView').click()
    driver.find_element(AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.TextView[2]').click()
    driver.find_element(By.ID, 'com.xingin.xhs:id/gov').click()
    driver.find_element(AppiumBy.XPATH, '//android.widget.Button[@content-desc="未选中，同意"]').click()
    driver.find_element(AppiumBy.XPATH, '//android.widget.Button[@content-desc="手机号登录"]').click()
    driver.find_element(By.ID, 'com.xingin.xhs:id/f91').click()
    driver.find_element(AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.ListView/android.widget.FrameLayout[2]').click()
    driver.find_element(AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.RelativeLayout[1]/android.widget.EditText').send_keys('152')


    # driver.quit()
