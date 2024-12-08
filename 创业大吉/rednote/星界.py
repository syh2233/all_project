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
   'appPackage': 'com.xingin.xhs',  # 启动APP Package名称
   'appActivity': '.index.v2.IndexActivityV2',  # 启动Activity名称
   'unicodeKeyboard': True,  # 自动化需要输入中文时填True
   'resetKeyboard': True,  # 执行完程序恢复原来输入法
   'noReset': True,  # 不要重置App
   'newCommandTimeout': 6000,
   'automationName': 'UiAutomator2'},
    'b': {'platformName': 'Android',  # 被测手机是安卓
   'platformVersion': '11',  # 手机安卓版本，如果是鸿蒙系统，依次尝试 12、11、10 这些版本号
   'deviceName': 'xxx',  # 设备名，安卓手机可以随意填写
   'appPackage': 'com.android.vending',  # 启动APP Package名称
   'appActivity': '.AssetBrowserActivity',  # 启动Activity名称
   'unicodeKeyboard': True,  # 自动化需要输入中文时填True
   'resetKeyboard': True,  # 执行完程序恢复原来输入法
   'noReset': True,  # 不要重置App
   'newCommandTimeout': 6000,
   'automationName': 'UiAutomator2'},
   # 'app': r'd:\apk\bili.apk',
}
list1 = [
# "5154818883|https://sms555.vip/266fcd5ec6cf2e1675c4d7a97a84f8b1",
# "5707552629|https://sms555.vip/29e84f85cf94b9ad2bd7b7aab4e692f7",
# "7746864152|https://sms555.vip/f87ff632e5cf52f92b07fbefbde1feae",
# "7859974266|https://sms555.vip/8e5a2baa12617550662abf3939e06e17",
# "9893572526|https://sms555.vip/60e7798f349f58b9ba38964bf182d9a1",
# "9302391478|https://sms555.vip/7ee137cf19fe7beca6e7871349777d55",
# "4757633922|https://sms555.vip/dcf454e162df1c14ee64d9e9067b28b8",
# "6673761280|https://sms555.vip/35c48677f4e100fa8593dd542aa89c21",
# "3075339217|https://sms555.vip/974f9264c19c2d8e94e76cd1b8d39642",
# "2184235884|https://sms555.vip/0d6e9058efdaa12eadf0f3a59da9ac6d",
# "4754662501|https://sms555.vip/e124d8ca602d77ada3160e83b47e39cd",
# "7653559370|https://sms555.vip/197a8d1ddf28816c7d9f40e8fefd977a",
# "3026211947|https://sms555.vip/b0336868907e38d1cb145a1310c2bae8",
# "7704705576|https://sms555.vip/ad4a649b112b6e9b1d5a23af8f0760a0",
# "6017977100|https://sms555.vip/b3fc7963b8e20ed56b37e59b833c34c0",
# "6626844934|https://sms555.vip/963477cc00a06e671c16c176a3949975",
# "9134087250|https://sms555.vip/5ad8b29bd8b7d8acf9bc63cc14859549",
# "5759997685|https://sms555.vip/7fd472b4ce5f47e8dc4435a92b54cc40",
"8508504292|https://sms555.vip/4feaa1d8fede9cb561f8217db554b7ca",
"7275160300|https://sms555.vip/4c30e320911f934b6898c07cf4e61abe",
]
for aa in list1:
 driver1 = webdriver.Remote('http://localhost:4723/wd/hub', options=UiAutomator2Options().load_capabilities(desired_caps['b']))

 driver1.implicitly_wait(30)
 # driver1.find_element(AppiumBy.XPATH, '//android.widget.FrameLayout[@content-desc="账号和设置。"]/android.widget.FrameLayout/android.widget.ImageView').click()
 # driver1.find_element(By.ID, 'com.android.vending:id/0_resource_name_obfuscated').click()
 # driver1.find_element(AppiumBy.XPATH, '//android.widget.ImageView[@content-desc="展开账号列表。"]').click()
 # driver1.find_element(AppiumBy.XPATH, '[@text="添加其他账号"]').click()
 input('回车')
 driver1.find_element(AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.Button').click()
 box1 = driver1.find_element(AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View[2]/android.view.View/android.view.View[1]/android.view.View/android.view.View/android.view.View/android.widget.EditText')
 box1.send_keys('syh2031.')

 driver1.find_element(AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.Button').click()
 driver1.find_element(AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View[3]/android.view.View/android.widget.Button').click()
 try:
  driver1.find_element(AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[5]/android.view.View[1]/android.widget.Button').click()
  driver1.swipe(start_x=101, start_y=1000, end_x=101, end_y=100, duration=80)
  driver1.find_element(AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.widget.Button').click()
 except:
  print('ll')


 # 连接Appium Server，初始化自动化环境
 driver = webdriver.Remote('http://localhost:4723/wd/hub', options=UiAutomator2Options().load_capabilities(desired_caps['a']))

 # 设置缺省等待时间
 driver.implicitly_wait(30)

 driver.find_element(AppiumBy.XPATH, '//android.widget.ImageView[@content-desc="菜单"]').click()
 driver.find_element(AppiumBy.XPATH, '//android.widget.LinearLayout[@content-desc="设置"]').click()
 driver.swipe(start_x=101, start_y=1000, end_x=101, end_y=100, duration=80)
 driver.find_element(AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[11]/android.view.ViewGroup/android.widget.TextView').click()
 driver.find_element(AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.TextView[1]').click()
 driver.find_element(AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.LinearLayout[1]/android.widget.Button').click()
 driver.find_element(AppiumBy.XPATH, '//android.widget.Button[@content-desc="未选中，同意"]').click()
 driver.find_element(AppiumBy.XPATH, '//android.widget.Button[@content-desc="Google登录"]').click()
 input('回车')
 try:
  driver.find_element(AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.ImageView[2]').click()
  driver.find_element(AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout[2]/android.widget.LinearLayout').click()
  driver.find_element(AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.ImageView[2]').click()
  driver.find_element(AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.TextView').click()
  driver.find_element(AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[1]').click()
 except:
  print('零零')

 driver.find_element(AppiumBy.XPATH, '//android.widget.ImageView[@content-desc="菜单"]').click()
 driver.find_element(AppiumBy.XPATH, '//android.widget.LinearLayout[@content-desc="设置"]').click()
 driver.find_element(AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[1]/android.view.ViewGroup/android.widget.TextView').click()
 driver.find_element(AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.RelativeLayout[1]/android.widget.LinearLayout/android.widget.TextView[2]').click()
 driver.find_element(AppiumBy.XPATH, '//android.widget.TextView[@content-desc="手机区号：+86"]').click()
 driver.find_element(AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.ListView/android.widget.FrameLayout[2]').click()
 box = driver.find_element(AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.RelativeLayout[1]/android.widget.EditText')

 a, b = aa.split('|')
 box.send_keys(a)
 driver.find_element(AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.RelativeLayout[2]/android.widget.TextView').click()
 input('回车')
 box2 = driver.find_element(AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.RelativeLayout[2]/android.widget.EditText')
 from DrissionPage import ChromiumPage, ChromiumOptions
 co = ChromiumOptions().set_paths()
 co.set_local_port(9999)
 browser = ChromiumPage(co)
 browser.get(b)
 al = re.findall(r'Your verification code is (.*?), for the changing phone number binding, please verify within 5 mins. Do not share the verification code to others.', browser.html, re.DOTALL)
 box2.send_keys(al)

 browser.quit()
 # driver.find_element(AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]').click()
 driver.find_element(AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.RelativeLayout[2]/android.widget.LinearLayout').click()
 box3 = driver.find_element(AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.widget.EditText')
 box3.send_keys('abcd1234.')
 box4 = driver.find_element(AppiumBy.XPATH, '	/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout[3]/android.widget.EditText')
 box4.send_keys('abcd1234.')
 driver.find_element(AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.Button').click()
 driver.find_element(AppiumBy.XPATH, '//android.widget.ImageButton[@content-desc="转到上一层级"]').click()
 driver.find_element(AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout[1]/android.widget.ImageView').click()
 driver.find_element(AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="我"]/android.widget.TextView').click()
 driver.find_element(AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="我"]/android.widget.TextView').click()
 print(driver.find_element(AppiumBy.XPATH,'/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/android.widget.LinearLayout/android.widget.RelativeLayout/androidx.viewpager.widget.ViewPager/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.widget.FrameLayout[1]/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.view.ViewGroup[1]/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView').text)


 input('回车')
