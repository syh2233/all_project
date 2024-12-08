import requests
from bs4 import BeautifulSoup

url1 = "https://www.baidu.com/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
}
proxies_a={
    "http": "http://us.owproxy.com:10086",
    "https": "https://us.owproxy.com:10086"
}
response = requests.get(url1, headers=headers, proxies=proxies_a)
print(response.status_code)

# 确保文本内容是字符串
content = response.text
print(content)
