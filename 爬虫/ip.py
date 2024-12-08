import requests
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
}
# prox ={
#             "http://72.10.160.90:22361",
#             "https://72.10.160.90:22361"
#         }
response = requests.get('https://www.baidu.com/', headers=headers)
if response.status_code == 200:
    print('ip可用')
