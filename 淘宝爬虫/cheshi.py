from selenium import webdriver


options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])
prefs = {'credentials_enable_service': False, 'profile.password_manager_enabled': False}
options.add_experimental_option('prefs', prefs)
options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(options=options)
f = open('stealth.min.js', mode='r', encoding='utf-8').read()
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': f})

driver.get('https://login.taobao.com/member/login.jhtml')

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 20)  # 等待最多10秒
element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#fm-login-id")))
element.send_keys('13328442979')
element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#fm-login-password")))
element.send_keys('syh2031.')
element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class='fm-button fm-submit password-login']")))
element.click()
element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-haspopup='true']")))
element.send_keys('Xreal beam pro')
element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class='btn-search tb-bg']")))
element.click()
element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-spm-click='gostr=/newpcsearch.item_search.sortbar_sale_cli;locaid=d2;name=销量']")))
element.click()
element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class='Title--iconPic--kYJcAc0']")))
element.click()
element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class='Comments--footer--3QTpCIW']")))
element.click()

input("Press Enter to quit...")