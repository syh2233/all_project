import pygame
import re
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('14.mp3')
from appium import webdriver
from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options

desired_caps = {
  'a': {'platformName': 'Android',  # 被测手机是安卓
   'platformVersion': '11',  # 手机安卓版本，如果是鸿蒙系统，依次尝试 12、11、10 这些版本号
   'deviceName': 'xxx',  # 设备名，安卓手机可以随意填写
   'appPackage': 'com.android.appstore',  # 启动APP Package名称
   'appActivity': '.view.MainActivity',  # 启动Activity名称
   'unicodeKeyboard': True,  # 自动化需要输入中文时填True
   'resetKeyboard': True,  # 执行完程序恢复原来输入法
   'noReset': True,  # 不要重置App
   'newCommandTimeout': 6000,
   'automationName': 'UiAutomator2'},
  'b': {'platformName': 'Android',  # 被测手机是安卓
   'platformVersion': '11',  # 手机安卓版本，如果是鸿蒙系统，依次尝试 12、11、10 这些版本号
   'deviceName': 'xxx',  # 设备名，安卓手机可以随意填写
   'appPackage': 'com.github.kr328.clash.foss',  # 启动APP Package名称
   'appActivity': 'com.github.kr328.clash.MainActivity',  # 启动Activity名称
   'unicodeKeyboard': True,  # 自动化需要输入中文时填True
   'resetKeyboard': True,  # 执行完程序恢复原来输入法
   'noReset': True,  # 不要重置App
   'newCommandTimeout': 6000,
   'automationName': 'UiAutomator2'},
}
driver = webdriver.Remote('http://localhost:4723/wd/hub', options=UiAutomator2Options().load_capabilities(desired_caps['a']))
driver.implicitly_wait(30)
driver.find_element(AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/androidx.viewpager.widget.ViewPager/android.widget.LinearLayout/androidx.viewpager.widget.ViewPager/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[1]/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.TextView[1]').click()
driver.find_element(AppiumBy.XPATH, '//android.widget.LinearLayout[@content-desc="系统工具"]/android.widget.TextView').click()
driver.find_element(AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/androidx.viewpager.widget.ViewPager/android.widget.LinearLayout/androidx.viewpager.widget.ViewPager/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[6]/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.TextView[1]').click()
driver1 = webdriver.Remote('http://localhost:4723/wd/hub', options=UiAutomator2Options().load_capabilities(desired_caps['b']))
driver1.implicitly_wait(30)
driver1.find_element(AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.ScrollView/android.widget.LinearLayout/androidx.cardview.widget.CardView[2]/android.widget.LinearLayout').click()
driver1.find_element(AppiumBy.XPATH, '//android.widget.ImageView[@content-desc="新建"]').click()
driver1.find_element(AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[1]').click()
driver1.find_element(AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.ScrollView/android.widget.LinearLayout/android.widget.FrameLayout[4]/android.widget.LinearLayout').click()
driver1.find_element(AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout/android.widget.FrameLayout/android.view.View').click()
driver1.find_element(AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout').click()
driver1.find_element(AppiumBy.XPATH, '').click()
