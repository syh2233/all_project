import requests
import time
import json
# from curl_cffi import requests

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,en-GB;q=0.6",
    "cache-control": "max-age=0",
    "cookie": "ASP.NET_SessionId=ownglohv4mm5z3iajuzmvt40; _ga=GA1.1.813765232.1757488013; cf_clearance=T62dFeU5FMKu3OGlddM7Sx0EIBNv0wlaUF6OjLVof3Q-1757488014-1.2.1.1-3ta3DvktRTCGpLSk8avZnrg3_13aAqJj927aOMQG046pI.ziELsK9aTCX5sGLILic9gDQtAO88g3VljB1okyyw5NOe5hupwT.WcE9XEJUNEh1G12E5CeBeIAPopT5wZFSK0b0v1YSvzB001fqcIDYR0TRmBPJg7ACXqvtXbsr94bKLEzDwfWHdRaOKgqHVw.tXUZKfPkkjnGDb_9FPmGiCj7ijSa8rx4_mhDaBqhOu0; _ga_8J1DN4NVHL=GS2.1.s1757488013$o1$g1$t1757488078$j60$l0$h0$dicntv-5E5gxJUL-YLBbruw_ciwisfQUeQg",
    "priority": "u=0, i",
    "referer": "http://mm.wisers.com:8080/",
    "sec-ch-ua": "\"Not;A=Brand\";v=\"99\", \"Microsoft Edge\";v=\"139\", \"Chromium\";v=\"139\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "cross-site",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0"
}



# 尝试不同的参数组合


for attempt in range(3):
    try:
        print(f"Attempt {attempt + 1}...")
        response = requests.get(
            f"https://acpss.ahram.org.eg/Portal/29/%D8%A3%D8%AE%D8%A8%D8%A7%D8%B1-%D9%88%D9%81%D8%B9%D8%A7%D9%84%D9%8A%D8%A7%D8%AA/0.aspx",
            # headers=headers,
            # json=data,
            # impersonate="chrome107",
            timeout=60,
            allow_redirects=True,
            # verify=False
        )
        print("Success! Response:", response.status_code)
        print(response.headers.get('Content-Encoding'))
        # import zstandard as zstd
        #
        # # 创建解压器对象
        # dctx = zstd.ZstdDecompressor()
        #
        # # 尝试流式解压
        # with dctx.stream_reader(response.content) as reader:
        #     decompressed_data = reader.read()
        #
        # # 尝试解码解压后的数据
        # print(decompressed_data.decode('utf-8'))
        print(response.text)

        break
    except Exception as e:
        print(f"Attempt {attempt + 1} failed: {e}")
        if attempt < 2:
            time.sleep(5)
