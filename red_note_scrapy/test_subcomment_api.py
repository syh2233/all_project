#!/usr/bin/env python3
"""
测试子评论API的不同参数组合
"""

import requests
import json
import time
import uuid
from urllib.parse import urlencode
from xs_generator import XSGenerator

def test_subcomment_api():
    """测试不同的子评论API参数"""
    
    # 基础请求头
    base_headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,en-GB;q=0.6',
        'origin': 'https://www.xiaohongshu.com',
        'priority': 'u=1, i',
        'referer': 'https://www.xiaohongshu.com/',
        'sec-ch-ua': '"Not;A=Brand";v="99", "Microsoft Edge";v="139", "Chromium";v="139"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0',
    }
    
    # Cookie信息
    cookie_info = {
        'a1': '198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479',
        'web_session': '040069b3ed6ebed4fbe30e25ad3a4b127faeca',
        'webId': 'fc4fb0dccb1a480d5f17359394c861d7',
        'webBuild': '4.79.0',
        'gid': 'yj8D24fWSDv0yj8D24fK069V0yIY6AFDTDxSxyU1kTyk2428MD7AC4888W2q2Yy8fJ0KjyDJ',
        'websectiga': '7750c37de43b7be9de8ed9ff8ea0e576519e8cd2157322eb972ecb429a7735d4',
        'sec_poison_id': 'bea36e3e-7471-4c83-8689-912f189ae738',
        'acw_tc': '0a4addf217569034688425790e21260cba639995389e86a499d4035458907d',
    }
    
    # 测试参数
    note_id = "68a048c1000000001d01838e"
    comment_id = "68a048ef000000003002a604"  # 这个评论有69条子评论
    
    # 不同的xsec_token尝试
    xsec_tokens = [
        'ABIyAXG1J9ckAl0VbljygE3I8b6TZ0k5P4jORY-kCIzzw%3D',  # 当前使用的
        'ABIyAXG1J9ckAl0VbljygE3I8b6TZ0k5P4jORY-kCIzzw=',   # 不带%3D
        '',                                                    # 空的
        None,                                                  # 不传这个参数
    ]
    
    # 创建session
    session = requests.Session()
    session.verify = False
    session.timeout = 10
    
    # XS生成器
    xs_gen = XSGenerator()
    
    def generate_trace_id():
        return str(uuid.uuid4()).replace('-', '')[:24]
    
    def prepare_headers(url, xsec_token):
        """准备请求头"""
        timestamp = str(int(time.time() * 1000))
        
        headers = base_headers.copy()
        headers['cookie'] = (
            f"gid={cookie_info['gid']}; "
            f"xsecappid=xhs-pc-web; "
            f"abRequestId=f425aaf4-2614-55c8-b8d1-262c611be2ab; "
            f"a1={cookie_info['a1']}; "
            f"webId={cookie_info['webId']}; "
            f"web_session={cookie_info['web_session']}; "
            f"webBuild={cookie_info['webBuild']}; "
            f"acw_tc={cookie_info['acw_tc']}; "
            f"websectiga={cookie_info['websectiga']}; "
            f"sec_poison_id={cookie_info['sec_poison_id']}; "
            "unread=%7B%22ub%22%3A%2268aa6588000000001d014a3f%22%2C%22ue%22%3A%2268b7bacf000000001c012ca6%22%2C%22uc%22%3A24%7D; "
            f"loadts={timestamp}"
        )
        
        headers['x-b3-traceid'] = generate_trace_id()
        headers['x-xray-traceid'] = generate_trace_id()
        
        # 生成X-s参数
        xs_value = xs_gen.generate_xs(
            url=url,
            method="GET",
            user_id=cookie_info['a1']
        )
        
        headers['X-s'] = xs_value
        headers['X-t'] = timestamp
        
        return headers
    
    print("测试不同的xsec_token参数...\n")
    
    for i, xsec_token in enumerate(xsec_tokens, 1):
        print(f"测试 {i}: xsec_token = {xsec_token}")
        
        # 构建URL
        base_url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page"
        params = {
            'note_id': note_id,
            'comment_id': comment_id,
            'cursor': '',
            'image_formats': 'jpg,webp,avif',
        }
        
        # 添加xsec_token（如果不为None）
        if xsec_token is not None:
            params['xsec_token'] = xsec_token
        
        params = {k: v for k, v in params.items() if v}
        url = base_url + '?' + urlencode(params)
        
        # 准备请求头
        headers = prepare_headers(url, xsec_token)
        
        try:
            response = session.get(url, headers=headers, timeout=10)
            print(f"  状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success', False):
                    comment_data = data.get('data', {})
                    sub_comments = comment_data.get('comments', [])
                    print(f"  成功！获取到 {len(sub_comments)} 条子评论")
                    if sub_comments:
                        print(f"  第一条子评论: {sub_comments[0].get('content', '')[:50]}...")
                else:
                    print(f"  失败: {data.get('msg', 'Unknown error')}")
            else:
                print(f"  失败: {response.text}")
                
        except Exception as e:
            print(f"  错误: {e}")
        
        print("-" * 50)
        time.sleep(1)  # 避免请求过快

if __name__ == "__main__":
    # 禁用SSL警告
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    test_subcomment_api()