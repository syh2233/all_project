import requests

# 清除cookie的请求
headers = {
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/139.0.0.0 Safari/537.36"
}

response = requests.get("https://acpss.ahram.org.eg/Portal/29/أخبار-وفعاليات/0.aspx", headers=headers)
print("响应头:")
for header, value in response.headers.items():
  if 'cookie' in header.lower() or 'cf-' in header.lower():
      print(f"{header}: {value}")