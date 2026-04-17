#!/usr/bin/env python3
"""
深入分析子评论API问题
"""

import requests
import json
import time
import uuid
from urllib.parse import urlencode, urlparse, parse_qs
from xs_generator import XSGenerator

def debug_subcomment_api():
    """调试子评论API问题"""
    
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
    comment_id = "68a048ef000000003002a604"
    
    # 创建session
    session = requests.Session()
    session.verify = False
    session.timeout = 10
    
    # XS生成器
    xs_gen = XSGenerator()
    
    def generate_trace_id():
        return str(uuid.uuid4()).replace('-', '')[:24]
    
    def prepare_headers(url):
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
    
    print("深入分析子评论API问题...\n")
    
    # 首先获取有效的评论ID
    print("1. 获取有效的评论ID:")
    main_url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/page"
    main_params = {
        'note_id': note_id,
        'cursor': '',
        'top_comment_id': '',
        'image_formats': 'jpg,webp,avif',
        'xsec_token': 'ABIyAXG1J9ckAl0VbljygE3I8b6TZ0k5P4jORY-kCIzzw%3D'
    }
    
    main_params = {k: v for k, v in main_params.items() if v}
    main_url_full = main_url + '?' + urlencode(main_params)
    main_headers = prepare_headers(main_url_full)
    
    try:
        main_response = session.get(main_url_full, headers=main_headers, timeout=10)
        if main_response.status_code == 200:
            main_data = main_response.json()
            if main_data.get('success', False):
                comments = main_data.get('data', {}).get('comments', [])
                print(f"获取到 {len(comments)} 条评论")
                
                # 选择第一条有回复的评论
                valid_comment_id = None
                for comment in comments:
                    sub_count = comment.get('sub_comment_count', 0)
                    if isinstance(sub_count, str):
                        try:
                            sub_count = int(sub_count)
                        except:
                            sub_count = 0
                    if sub_count > 0:
                        valid_comment_id = comment.get('id')
                        print(f"找到有子评论的评论ID: {valid_comment_id}")
                        print(f"子评论数量: {sub_count}")
                        break
                
                if not valid_comment_id:
                    print("未找到有子评论的评论，使用第一条评论")
                    valid_comment_id = comments[0].get('id') if comments else comment_id
            else:
                print(f"获取评论失败: {main_data.get('msg', 'Unknown error')}")
                valid_comment_id = comment_id
        else:
            print(f"获取评论失败，状态码: {main_response.status_code}")
            valid_comment_id = comment_id
    except Exception as e:
        print(f"获取评论出错: {e}")
        valid_comment_id = comment_id
    
    print("\n" + "="*50 + "\n")
    
    # 测试不同的子评论API调用方式
    print("2. 测试不同的子评论API调用方式:")
    
    sub_url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page"
    
    # 方式1：使用有效的comment_id
    print("\n方式1：使用有效的comment_id")
    sub_params = {
        'note_id': note_id,
        'comment_id': valid_comment_id,
        'cursor': '',
        'image_formats': 'jpg,webp,avif',
        'xsec_token': 'ABIyAXG1J9ckAl0VbljygE3I8b6TZ0k5P4jORY-kCIzzw%3D'
    }
    
    sub_params = {k: v for k, v in sub_params.items() if v}
    sub_url_full = sub_url + '?' + urlencode(sub_params)
    sub_headers = prepare_headers(sub_url_full)
    
    try:
        sub_response = session.get(sub_url_full, headers=sub_headers, timeout=10)
        print(f"状态码: {sub_response.status_code}")
        print(f"响应头: {dict(sub_response.headers)}")
        if sub_response.status_code == 200:
            sub_data = sub_response.json()
            print(f"响应体: {json.dumps(sub_data, indent=2, ensure_ascii=False)}")
        else:
            print(f"失败: {sub_response.text}")
    except Exception as e:
        print(f"错误: {e}")
    
    print("\n" + "-"*30 + "\n")
    
    # 方式2：不使用xsec_token
    print("方式2：不使用xsec_token")
    sub_params_no_token = {
        'note_id': note_id,
        'comment_id': valid_comment_id,
        'cursor': '',
        'image_formats': 'jpg,webp,avif'
    }
    
    sub_url_full_no_token = sub_url + '?' + urlencode(sub_params_no_token)
    sub_headers_no_token = prepare_headers(sub_url_full_no_token)
    
    try:
        sub_response = session.get(sub_url_full_no_token, headers=sub_headers_no_token, timeout=10)
        print(f"状态码: {sub_response.status_code}")
        if sub_response.status_code == 200:
            sub_data = sub_response.json()
            print(f"响应体: {json.dumps(sub_data, indent=2, ensure_ascii=False)}")
        else:
            print(f"失败: {sub_response.text}")
    except Exception as e:
        print(f"错误: {e}")
    
    print("\n" + "-"*30 + "\n")
    
    # 方式3：使用POST方法
    print("方式3：使用POST方法")
    sub_headers_post = prepare_headers(sub_url)
    sub_headers_post['content-type'] = 'application/json'
    
    try:
        sub_response = session.post(sub_url, headers=sub_headers_post, json=sub_params_no_token, timeout=10)
        print(f"状态码: {sub_response.status_code}")
        if sub_response.status_code == 200:
            sub_data = sub_response.json()
            print(f"响应体: {json.dumps(sub_data, indent=2, ensure_ascii=False)}")
        else:
            print(f"失败: {sub_response.text}")
    except Exception as e:
        print(f"错误: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 分析请求头差异
    print("3. 请求头分析:")
    print("当前使用的请求头:")
    for key, value in sub_headers.items():
        print(f"  {key}: {value}")
    
    print("\n可能的问题:")
    print("1. comment_id 可能无效或格式不正确")
    print("2. 子评论API可能需要额外的认证参数")
    print("3. 可能需要特定的请求头")
    print("4. API可能有访问频率限制")
    print("5. 可能需要先访问页面建立session")

if __name__ == "__main__":
    # 禁用SSL警告
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    debug_subcomment_api()