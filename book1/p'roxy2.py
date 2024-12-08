import yaml
import time
import requests
from DrissionPage import ChromiumPage, ChromiumOptions
import re
# 切换节点的间隔时间（秒），这里设置为1秒
interval = 1

# 配置文件路径
config_path = r'.\AllBlue Cloud.yaml'

# Clash API地址和密钥
def ip():
    global clash_api_url
    global secret_key
    with open(r'C:\Users\沈家\.config\clash\config.yaml', 'r', encoding='utf-8') as f:
        a = f.read()
    aa = re.findall(r'external-controller: (.*?)\n', str(a), re.DOTALL)[0]
    clash_api_url = f'http://{aa}/proxies/蓝色海洋-网络云加速'
    secret_key = 'beeebd30-5302-4965-bf28-7a74bb30a39b'  # 替换为你的密钥


def load_config():
    with open(config_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    return config


def switch_proxy(proxy_name):
    payload = {'name': proxy_name}
    headers = {
        'Authorization': f'Bearer {secret_key}'
    }
    response = requests.put(clash_api_url, json=payload, headers=headers)
    if response.status_code == 204:
        print(f'Successfully switched to proxy: {proxy_name}')
    else:
        print(f'Failed to switch to proxy: {proxy_name}. Status code: {response.status_code}')


def main():
    ip()
    config = load_config()
    proxies_list = config.get('proxies', [])

    if not proxies_list:
        print("No proxies found in the configuration file.")
        return

    current_index = 0
    while True:
        proxy_name = proxies_list[current_index]['name']
        switch_proxy(proxy_name)
        # 更新索引
        current_index = (current_index + 1) % len(proxies_list)
        # 等待下一次切换
        co = ChromiumOptions().set_paths()
        # co.headless()
        # co.set_argument('--window-size', '80,60')
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
        except:
            print('代理不可用')
        time.sleep(interval)


if __name__ == '__main__':
    main()