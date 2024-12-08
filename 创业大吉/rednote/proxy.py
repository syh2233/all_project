import yaml
import time
import requests
from DrissionPage import ChromiumPage, ChromiumOptions
import re

# 切换节点的间隔时间（秒），这里设置为1秒
interval = 1

# 配置文件路径
config_path = r'.\red.yaml'

# Clash API地址和密钥
clash_api_url = 'https://www.fawncloud.one/link/6zPgzN5FZMvl6dEh?clash=1'
secret_key = ''

def load_config():
    with open(config_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    return config

def get_clash_api_url_and_secret():
    global clash_api_url
    global secret_key
    with open(r'C:\Users\沈家\.config\clash\config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    clash_api_url = config['external-controller']
    secret_key = ''  # 从配置文件或环境变量中获取您的密钥

def switch_proxy(proxy_name):
    payload = {'name': proxy_name}
    headers = {
        'Authorization': f'Bearer {secret_key}',
        'Content-Type': 'application/json'
    }
    response = requests.put(clash_api_url, json=payload, headers=headers)
    if response.status_code == 200:
        print(f'Successfully switched to proxy: {proxy_name}')
    else:
        print(f'Failed to switch to proxy: {proxy_name}. Status code: {response.status_code}')

def main():
    get_clash_api_url_and_secret()
    config = load_config()
    proxies_list = config.get('proxies', [])

    if not proxies_list:
        print("No proxies found in the configuration file.")
        return

    current_index = 0
    while True:
        proxy = proxies_list[current_index]
        proxy_name = proxy['name']
        switch_proxy(proxy_name)
        # 更新索引
        current_index = (current_index + 1) % len(proxies_list)
        # 等待下一次切换
        co = ChromiumOptions().set_paths()
        co.set_timeouts(6, 6, 6)
        co.set_local_port(9446)
        browser = ChromiumPage(co)
        try:
            browser.get('https://www.ip38.com/', retry=1, timeout=3)
            ab = browser.ele('@id:ipad').text
            print(ab)
            browser.quit()
            with open('代理.txt', 'a', encoding='utf-8') as file:
                file.write(f'{proxy_name}:{ab}\n')
        except Exception as e:
            print('代理不可用', e)
        time.sleep(interval)

if __name__ == '__main__':
    main()