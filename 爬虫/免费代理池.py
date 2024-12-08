import requests
import re
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
}
list_ip = []
for i in range(0, 2000):
    resonpse = requests.get('https://www.iphaiwai.com/free/' + str(i) + '/', headers=headers)
    ip_list = re.findall('"ip": "(.*?)"', resonpse.text)
    port_list = re.findall('"port": "(.*?)"', resonpse.text)
    for ip, port in zip(ip_list, port_list):
        ip_http = "http://" + ip + ':' + port,
        ip_https = "https://" + ip + ':' + port,
        prox ={
            "http": str(ip_http),
            "https": str(ip_https)
        }
        try:
            response = requests.get('https://www.baidu.com/', headers=headers, proxies=prox, timeout=1)

            if response.status_code == 200:
                print('ip可用', prox)
                list_ip.append(prox)

        except:
            print('ip不可用', prox)
        i = i + 1
print(list_ip)