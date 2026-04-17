#!/usr/bin/env python3
"""
深度分析小红书子评论API问题
"""

import requests
import json
import time
import uuid
from urllib.parse import urlencode, urlparse, parse_qs
from xs_generator import XSGenerator

def deep_analysis():
    """深度分析子评论API问题"""
    
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
    
    def prepare_headers(url, additional_headers=None):
        """准备请求头"""
        timestamp = str(int(time.time() * 1000))
        
        headers = base_headers.copy()
        if additional_headers:
            headers.update(additional_headers)
            
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
    
    print("深度分析小红书子评论API问题...\n")
    
    # 先访问页面建立session
    print("1. 访问笔记页面建立session:")
    page_url = f"https://www.xiaohongshu.com/explore/{note_id}"
    page_headers = prepare_headers(page_url)
    
    try:
        page_response = session.get(page_url, headers=page_headers, timeout=10)
        print(f"页面访问状态码: {page_response.status_code}")
        if page_response.status_code == 200:
            print("页面访问成功，session已建立")
        else:
            print(f"页面访问失败: {page_response.status_code}")
    except Exception as e:
        print(f"页面访问出错: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 测试不同的API路径
    print("2. 测试不同的API路径:")
    
    api_paths = [
        "/api/sns/web/v2/comment/sub/page",
        "/api/sns/web/v2/comment/sub_comment/page",
        "/api/sns/web/v2/comment/reply/page",
        "/api/sns/web/v2/comment/child/page",
        "/api/sns/web/v2/comment/subcomments/page"
    ]
    
    base_url = "https://edith.xiaohongshu.com"
    
    for path in api_paths:
        print(f"\n测试路径: {path}")
        full_url = base_url + path
        
        params = {
            'note_id': note_id,
            'comment_id': comment_id,
            'cursor': '',
            'image_formats': 'jpg,webp,avif',
            'xsec_token': 'ABIyAXG1J9ckAl0VbljygE3I8b6TZ0k5P4jORY-kCIzzw%3D'
        }
        
        params = {k: v for k, v in params.items() if v}
        url_with_params = full_url + '?' + urlencode(params)
        headers = prepare_headers(url_with_params)
        
        try:
            response = session.get(url_with_params, headers=headers, timeout=10)
            print(f"  状态码: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"  成功: {data.get('success', False)}")
                if data.get('success', False):
                    comments = data.get('data', {}).get('comments', [])
                    print(f"  子评论数量: {len(comments)}")
                else:
                    print(f"  错误信息: {data.get('msg', 'Unknown error')}")
                    print(f"  错误代码: {data.get('code', 'Unknown')}")
            else:
                print(f"  失败: {response.text}")
        except Exception as e:
            print(f"  错误: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 测试不同的参数组合
    print("3. 测试不同的参数组合:")
    
    param_combinations = [
        # 基础参数
        {'note_id': note_id, 'comment_id': comment_id},
        # 添加cursor
        {'note_id': note_id, 'comment_id': comment_id, 'cursor': ''},
        # 添加image_formats
        {'note_id': note_id, 'comment_id': comment_id, 'image_formats': 'jpg,webp,avif'},
        # 添加xsec_token
        {'note_id': note_id, 'comment_id': comment_id, 'xsec_token': 'ABIyAXG1J9ckAl0VbljygE3I8b6TZ0k5P4jORY-kCIzzw%3D'},
        # 完整参数
        {'note_id': note_id, 'comment_id': comment_id, 'cursor': '', 'image_formats': 'jpg,webp,avif', 'xsec_token': 'ABIyAXG1J9ckAl0VbljygE3I8b6TZ0k5P4jORY-kCIzzw%3D'},
        # 尝试不同的xsec_token
        {'note_id': note_id, 'comment_id': comment_id, 'xsec_token': ''},
    ]
    
    sub_url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page"
    
    for i, params in enumerate(param_combinations, 1):
        print(f"\n参数组合 {i}:")
        print(f"  参数: {params}")
        
        params = {k: v for k, v in params.items() if v}
        url_with_params = sub_url + '?' + urlencode(params)
        headers = prepare_headers(url_with_params)
        
        try:
            response = session.get(url_with_params, headers=headers, timeout=10)
            print(f"  状态码: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"  成功: {data.get('success', False)}")
                if not data.get('success', False):
                    print(f"  错误信息: {data.get('msg', 'Unknown error')}")
                    print(f"  错误代码: {data.get('code', 'Unknown')}")
            else:
                print(f"  失败: {response.text}")
        except Exception as e:
            print(f"  错误: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 检查是否需要特定的请求头
    print("4. 检查特定的请求头:")
    
    # 获取正常的主评论响应头
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
        print(f"主评论API状态码: {main_response.status_code}")
        if main_response.status_code == 200:
            print("主评论API成功，对比请求头差异...")
            print("\n主评论API请求头:")
            for key, value in main_headers.items():
                print(f"  {key}: {value}")
    except Exception as e:
        print(f"主评论API出错: {e}")
    
    print("\n结论:")
    print("基于以上分析，可能的原因:")
    print("1. 子评论API路径不正确")
    print("2. 需要特定的参数组合")
    print("3. 需要特定的访问顺序（先访问页面）")
    print("4. 可能需要额外的认证信息")
    print("5. API可能有权限控制")

if __name__ == "__main__":
    # 禁用SSL警告
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    deep_analysis()