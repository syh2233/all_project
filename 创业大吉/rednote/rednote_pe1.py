import pygame
import time

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('14.mp3')
from appium import webdriver
from selenium.webdriver.common.by import By
from appium.webdriver.extensions.android.nativekey import AndroidKey
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

desired_caps = {
  'a': {'platformName': 'Android',  # 被测手机是安卓
   'platformVersion': '9',  # 手机安卓版本，如果是鸿蒙系统，依次尝试 12、11、10 这些版本号
   'deviceName': 'emulator-5588',  # 使用实际的设备名
   'appPackage': 'com.xingin.xhs',  # 启动APP Package名称
   'appActivity': 'com.xingin.xhs.index.v2.IndexActivityV2',  # 启动Activity名称（完整路径）
   'unicodeKeyboard': True,  # 自动化需要输入中文时填True
   'resetKeyboard': True,  # 执行完程序恢复原来输入法
   'noReset': True,  # 不要重置App
   'newCommandTimeout': 6000,
   'automationName': 'UiAutomator2'},
  'b': {'platformName': 'Android',  # 被测手机是安卓
   'platformVersion': '12',  # 手机安卓版本，如果是鸿蒙系统，依次尝试 12、11、10 这些版本号
   'deviceName': 'xxx',  # 设备名，安卓手机可以随意填写
   'appPackage': 'com.qihoo.magic.dMHa45ibpdmbphnLt92Yk_104',  # 启动APP Package名称
   'appActivity': 'com.morgoo.droidplugin.stub.ActivityProxy',  # 启动Activity名称
   'unicodeKeyboard': True,  # 自动化需要输入中文时填True
   'resetKeyboard': True,  # 执行完程序恢复原来输入法
   'noReset': True,  # 不要重置App
   'newCommandTimeout': 6000,
   'automationName': 'UiAutomator2'
  },
    'c':{'platformName': 'Android',  # 被测手机是安卓
   'platformVersion': '10',  # 手机安卓版本，如果是鸿蒙系统，依次尝试 12、11、10 这些版本号
   'deviceName': 'xxx',  # 设备名，安卓手机可以随意填写
   'appPackage': 'com.qihoo.magic.dMHa45ibpdmbphnLt92Yk_104',  # 启动APP Package名称
   'appActivity': 'com.qihoo.magic.plugin.AppEnterActivity',  # 启动Activity名称
   'unicodeKeyboard': True,  # 自动化需要输入中文时填True
   'resetKeyboard': True,  # 执行完程序恢复原来输入法
   'noReset': True,  # 不要重置App
   'newCommandTimeout': 6000,
   'automationName': 'UiAutomator2'
    },
    'd':{'platformName': 'Android',  # 被测手机是安卓
   'platformVersion': '10',  # 手机安卓版本，如果是鸿蒙系统，依次尝试 12、11、10 这些版本号
   'deviceName': 'xxx',  # 设备名，安卓手机可以随意填写
   'appPackage': 'com.qihoo.magic.dMHa45ibpdmbphnLt92Yk_103',  # 启动APP Package名称
   'appActivity': 'com.qihoo.magic.plugin.AppEnterActivity',  # 启动Activity名称
   'unicodeKeyboard': True,  # 自动化需要输入中文时填True
   'resetKeyboard': True,  # 执行完程序恢复原来输入法
   'noReset': True,  # 不要重置App
   'newCommandTimeout': 6000,
   'automationName': 'UiAutomator2'

    },
    'e':{'platformName': 'Android',  # 被测手机是安卓
   'platformVersion': '10',  # 手机安卓版本，如果是鸿蒙系统，依次尝试 12、11、10 这些版本号
   'deviceName': 'xxx',  # 设备名，安卓手机可以随意填写
   'appPackage': 'com.qihoo.magic.dMHa45ibpdmbphnLt92Yk_102',  # 启动APP Package名称
   'appActivity': 'com.qihoo.magic.plugin.AppEnterActivity',  # 启动Activity名称
   'unicodeKeyboard': True,  # 自动化需要输入中文时填True
   'resetKeyboard': True,  # 执行完程序恢复原来输入法
   'noReset': True,  # 不要重置App
   'newCommandTimeout': 6000,
   'automationName': 'UiAutomator2'

    },
   # 'app': r'd:\apk\bili.apk',
}
list1 = ['a']
for i in list1:
    print(desired_caps[i])
    # 连接Appium Server，初始化自动化环境
    driver = webdriver.Remote('http://localhost:4723/wd/hub', options=UiAutomator2Options().load_capabilities(desired_caps[i]))

    # 设置缺省等待时间
    driver.implicitly_wait(90)
    driver.find_element(AppiumBy.XPATH, '//android.widget.Button[@content-desc="未选中，同意"]').click()
    driver.find_element(AppiumBy.XPATH,'/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.view.ViewGroup/android.widget.Button').click()
    driver.find_element(AppiumBy.XPATH,'//android.widget.Button[@content-desc="未选中，同意"]').click()
    # # 根据id定位搜索位置框，点击
    # driver.find_element(By.ID, 'com.xingin.xhs:id/search').click()
    #
    # # 根据id定位搜索输入框，点击
    box = driver.find_element(AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.RelativeLayout[1]/android.widget.EditText')
    box.send_keys('13328442979')
    driver.find_element(AppiumBy.XPATH,'/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.Button/android.widget.TextView').click()
    box = driver.find_element(AppiumBy.XPATH,'/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.RelativeLayout[2]/android.widget.EditText')
    box.send_keys('123456')
    driver.find_element(AppiumBy.XPATH,'/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.Button/android.widget.TextView').click()
    # # 输入回车键，确定搜索
    # driver.press_keycode(AndroidKey.ENTER)
    # driver.find_element(By.ID, 'com.xingin.xhs:id/noteTitle').click()
    # for i_1 in range(30):
    #     while True:
    #         try:
    #             driver.swipe(start_x=51, start_y=400, end_x=51, end_y=50, duration=50)
    #             break
    #         except:
    #             print(f"重启{i_1}")
    #             pygame.mixer.music.play()
    #             driver = webdriver.Remote('http://localhost:4723/wd/hub',
    #                                       options=UiAutomator2Options().load_capabilities(desired_caps[i]))
    #
    #             # 设置缺省等待时间
    #             driver.implicitly_wait(30)
    #
    #             # 根据id定位搜索位置框，点击
    #             driver.find_element(By.ID, 'com.xingin.xhs:id/search').click()
    #
    #             # 根据id定位搜索输入框，点击
    #             box = driver.find_element(By.ID, 'com.xingin.xhs:id/mSearchToolBarEt')
    #             box.send_keys('双眼皮')
    #             # 输入回车键，确定搜索
    #             driver.press_keycode(AndroidKey.ENTER)
    #             driver.find_element(By.ID, 'com.xingin.xhs:id/noteTitle').click()
    #             while pygame.mixer.music.get_busy():  # 当音乐还在播放时
    #                 pygame.time.Clock().tick(10)
    #     # driver.find_element(By.ID, 'com.xingin.xhs:id/fqn')
    #     i_1 += 1
    #     if i_1 % 5 == 0:
    #         driver.find_element(By.ID, 'com.xingin.xhs:id/matrixFollowView').click()
    #         try:
    #             driver.find_element(By.ID, 'android:id/button2').click()
    #         except:
    #             print('未关注过')
    #         driver.find_element(By.ID, 'com.xingin.xhs:id/matrix_detail_feed_item_like_image_view').click()
    #     time.sleep(60)
    # driver.quit()
