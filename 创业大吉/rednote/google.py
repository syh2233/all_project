import time

from appium import webdriver
from selenium.webdriver.common.by import By
from appium.webdriver.extensions.android.nativekey import AndroidKey
from appium.options.android import UiAutomator2Options

desired_caps = {'platformName': 'Android',  # 被测手机是安卓
   'platformVersion': '8',  # 手机安卓版本，如果是鸿蒙系统，依次尝试 12、11、10 这些版本号
   'deviceName': 'xxx',  # 设备名，安卓手机可以随意填写
   'appPackage': 'com.vivo.browser',  # 启动APP Package名称
   'appActivity': '.BrowserActivity',  # 启动Activity名称
   'unicodeKeyboard': True,  # 自动化需要输入中文时填True
   'resetKeyboard': True,  # 执行完程序恢复原来输入法
   'noReset': True,  # 不要重置App
   'newCommandTimeout': 6000,
   'automationName': 'UiAutomator2'
}

driver = webdriver.Remote('http://localhost:4723/wd/hub', options=UiAutomator2Options().load_capabilities(desired_caps))
driver.implicitly_wait(30)
driver.find_element(By.ID, 'com.vivo.browser:id/search_text').click()
box = driver.find_element(By.ID, 'com.vivo.browser:id/edit')
box.send_keys('https://accounts.google.com/')
driver.press_keycode(AndroidKey.ENTER)
