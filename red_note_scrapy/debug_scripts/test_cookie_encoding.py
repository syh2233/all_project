#!/usr/bin/env python3
"""
精确测试cookie编码问题
"""

import requests
import json
import time
import uuid
import urllib.parse
from urllib.parse import urlencode
from xs_generator import XSGenerator

def test_cookie_encoding():
    """测试cookie编码问题"""
    
    print("测试cookie编码问题...\n")
    
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
        'websectiga': '634d3ad75ffb42a2ade2c5e1705a73c845837578aeb31ba0e442d75c648da36a',
        'sec_poison_id': '3e95e4cf-0caf-423d-a0ec-d4e3a49d703c',
        'acw_tc': '0a4a453a17569070897088137ec524bb28ede595ddc525595031d81456a33f',
    }
    
    # 测试参数
    note_id = "68a048c1000000001d01838e"
    root_comment_id = "68a048ef000000003002a604"
    
    # 创建session
    session = requests.Session()
    session.verify = False
    session.timeout = 10
    
    # XS生成器
    xs_gen = XSGenerator()
    
    def generate_trace_id():
        return str(uuid.uuid4()).replace('-', '')[:24]
    
    print("1. 测试不同的cookie编码方式")
    
    sub_url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page"
    
    # 基础参数
    base_params = {
        'note_id': note_id,
        'root_comment_id': root_comment_id,
        'num': '10',
        'cursor': '',
        'image_formats': 'jpg,webp,avif',
        'xsec_token': 'ABIyAXG1J9ckAl0VbljygE3I8b6TZ0k5P4jORY-kCIzzw%3D'
    }
    
    # 不同的cookie编码方式
    cookie_variants = [
        {
            'name': '原始编码',
            'unread': '%7B%22ub%22%3A%2268b56bf2000000001c004134%22%2C%22ue%22%3A%2268a3fe26000000001c0126d1%22%2C%22uc%22%3A20%7D'
        },
        {
            'name': '双重编码',
            'unread': urllib.parse.quote('%7B%22ub%22%3A%2268b56bf2000000001c004134%22%2C%22ue%22%3A%2268a3fe26000000001c0126d1%22%2C%22uc%22%3A20%7D')
        },
        {
            'name': '未编码',
            'unread': '{"ub":"68b56bf2000000001c004134","ue":"68a3fe26000000001c0126d1","uc":20}'
        },
        {
            'name': '简化版',
            'unread': '%7B%22uc%22%3A20%7D'
        },
        {
            'name': '无unread参数',
            'unread': None
        }
    ]
    
    for i, variant in enumerate(cookie_variants, 1):
        print(f"\n测试 {i}: {variant['name']}")
        
        timestamp = str(int(time.time() * 1000))
        
        # 构建cookie
        cookie_parts = [
            f"gid={cookie_info['gid']}",
            "xsecappid=xhs-pc-web",
            "abRequestId=f425aaf4-2614-55c8-b8d1-262c611be2ab",
            f"a1={cookie_info['a1']}",
            f"webId={cookie_info['webId']}",
            f"web_session={cookie_info['web_session']}",
            f"webBuild={cookie_info['webBuild']}",
            f"acw_tc={cookie_info['acw_tc']}",
            f"websectiga={cookie_info['websectiga']}",
            f"sec_poison_id={cookie_info['sec_poison_id']}",
            f"loadts={timestamp}"
        ]
        
        if variant['unread'] is not None:
            cookie_parts.append(f"unread={variant['unread']}")
        
        full_cookie = "; ".join(cookie_parts)
        
        # 构建URL
        params = {k: v for k, v in base_params.items() if v}
        url_with_params = sub_url + '?' + urlencode(params)
        
        # 准备请求头
        headers = base_headers.copy()
        headers['cookie'] = full_cookie
        headers['x-b3-traceid'] = generate_trace_id()
        headers['x-xray-traceid'] = generate_trace_id()
        
        # 生成X-s参数
        xs_value = xs_gen.generate_xs(
            url=url_with_params,
            method="GET",
            user_id=cookie_info['a1']
        )
        
        headers['X-s'] = xs_value
        headers['X-t'] = timestamp
        headers['x-s-common'] = xs_value
        
        print(f"Cookie长度: {len(full_cookie)}")
        
        try:
            response = session.get(url_with_params, headers=headers, timeout=10)
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    success = data.get('success', False)
                    print(f"成功: {success}")
                    
                    if success:
                        comments = data.get('data', {}).get('comments', [])
                        print(f"子评论数量: {len(comments)}")
                        print("✅ 成功！")
                        
                        # 显示前两条评论
                        if comments:
                            print("前两条评论:")
                            for j, comment in enumerate(comments[:2], 1):
                                content = comment.get('content', 'N/A')
                                user_name = comment.get('user', {}).get('nickname', 'N/A')
                                print(f"  {j}. {user_name}: {content}")
                        
                        return True  # 成功获取
                        
                    else:
                        msg = data.get('msg', 'Unknown error')
                        code = data.get('code', 'Unknown')
                        print(f"错误信息: {msg}")
                        print(f"错误代码: {code}")
                        
                except json.JSONDecodeError:
                    print(f"响应不是JSON格式: {response.text[:200]}")
            else:
                print(f"失败: {response.text[:100]}")
                
        except Exception as e:
            print(f"请求出错: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 如果都失败了，尝试使用浏览器开发者工具中提供的完整cookie
    print("2. 使用完整的浏览器cookie")
    
    # 你提供的完整cookie
    browser_cookie = "gid=yj8D24fWSDv0yj8D24fK069V0yIY6AFDTDxSxyU1kTyk2428MD7AC4888W2q2Yy8fJ0KjyDJ; xsecappid=xhs-pc-web; abRequestId=f425aaf4-2614-55c8-b8d1-262c611be2ab; a1=198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479; webId=fc4fb0dccb1a480d5f17359394c861d7; web_session=040069b3ed6ebed4fbe30e25ad3a4b127faeca; webBuild=4.79.0; unread=%7B%22ub%22%3A%2268b56bf2000000001c004134%22%2C%22ue%22%3A%2268a3fe26000000001c0126d1%22%2C%22uc%22%3A20%7D; acw_tc=0a4a453a17569070897088137ec524bb28ede595ddc525595031d81456a33f; websectiga=634d3ad75ffb42a2ade2c5e1705a73c845837578aeb31ba0e442d75c648da36a; sec_poison_id=3e95e4cf-0caf-423d-a0ec-d4e3a49d703c; loadts=1756907107387"
    
    print(f"浏览器cookie长度: {len(browser_cookie)}")
    
    # 构建URL
    params = {k: v for k, v in base_params.items() if v}
    url_with_params = sub_url + '?' + urlencode(params)
    
    # 准备请求头
    headers = base_headers.copy()
    headers['cookie'] = browser_cookie
    headers['x-b3-traceid'] = generate_trace_id()
    headers['x-xray-traceid'] = generate_trace_id()
    
    # 生成X-s参数
    xs_value = xs_gen.generate_xs(
        url=url_with_params,
        method="GET",
        user_id=cookie_info['a1']
    )
    
    headers['X-s'] = xs_value
    headers['X-t'] = timestamp
    headers['x-s-common'] = xs_value
    
    try:
        response = session.get(url_with_params, headers=headers, timeout=10)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                success = data.get('success', False)
                print(f"成功: {success}")
                
                if success:
                    comments = data.get('data', {}).get('comments', [])
                    print(f"子评论数量: {len(comments)}")
                    print("✅ 成功！")
                    
                    # 显示前两条评论
                    if comments:
                        print("前两条评论:")
                        for j, comment in enumerate(comments[:2], 1):
                            content = comment.get('content', 'N/A')
                            user_name = comment.get('user', {}).get('nickname', 'N/A')
                            print(f"  {j}. {user_name}: {content}")
                    
                    return True  # 成功获取
                    
                else:
                    msg = data.get('msg', 'Unknown error')
                    code = data.get('code', 'Unknown')
                    print(f"错误信息: {msg}")
                    print(f"错误代码: {code}")
                    
            except json.JSONDecodeError:
                print(f"响应不是JSON格式: {response.text[:200]}")
        else:
            print(f"失败: {response.text[:100]}")
            
    except Exception as e:
        print(f"请求出错: {e}")
    
    print("\n3. 结论")
    print("如果以上测试都失败，可能需要:")
    print("1. 更新loadts时间戳")
    print("2. 使用完全相同的请求头")
    print("3. 模拟完整的浏览器环境")
    print("4. 可能需要特定的访问序列")
    
    return False

if __name__ == "__main__":
    # 禁用SSL警告
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    test_cookie_encoding()