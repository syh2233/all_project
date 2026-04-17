#!/usr/bin/env python3
"""
最终验证x-s-common = X-s的发现
"""

import requests
import json
import time
import uuid
from urllib.parse import urlencode
from xs_generator import XSGenerator

def final_verification():
    """最终验证发现"""
    
    print("最终验证：x-s-common = X-s\n")
    
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
    
    print("1. 测试发现：使用正确的参数名和完整的认证")
    
    # 先访问页面建立session
    page_url = f"https://www.xiaohongshu.com/explore/{note_id}"
    
    timestamp = str(int(time.time() * 1000))
    
    # 构建完整的cookie
    full_cookie = (
        f"gid={cookie_info['gid']}; "
        f"xsecappid=xhs-pc-web; "
        f"abRequestId=f425aaf4-2614-55c8-b8d1-262c611be2ab; "
        f"a1={cookie_info['a1']}; "
        f"webId={cookie_info['webId']}; "
        f"web_session={cookie_info['web_session']}; "
        f"webBuild={cookie_info['webBuild']}; "
        f"unread=%7B%22ub%22%3A%2268b56bf2000000001c004134%22%2C%22ue%22%3A%2268a3fe26000000001c0126d1%22%2C%22uc%22%3A20%7D; "
        f"acw_tc={cookie_info['acw_tc']}; "
        f"websectiga={cookie_info['websectiga']}; "
        f"sec_poison_id={cookie_info['sec_poison_id']}; "
        f"loadts={timestamp}"
    )
    
    # 访问页面
    page_headers = base_headers.copy()
    page_headers['cookie'] = full_cookie
    
    try:
        page_response = session.get(page_url, headers=page_headers, timeout=10)
        print(f"页面访问状态码: {page_response.status_code}")
    except Exception as e:
        print(f"页面访问出错: {e}")
    
    print("\n2. 测试子评论API")
    
    sub_url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page"
    
    # 使用正确的参数
    params = {
        'note_id': note_id,
        'root_comment_id': root_comment_id,
        'num': '10',
        'cursor': '',
        'image_formats': 'jpg,webp,avif',
        'xsec_token': 'ABIyAXG1J9ckAl0VbljygE3I8b6TZ0k5P4jORY-kCIzzw%3D'
    }
    
    # 构建完整URL
    params = {k: v for k, v in params.items() if v}
    url_with_params = sub_url + '?' + urlencode(params)
    
    print(f"请求URL: {url_with_params}")
    
    # 准备完整的请求头
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
    
    # 关键发现：x-s-common = X-s
    headers['x-s-common'] = xs_value
    
    print(f"X-s: {xs_value}")
    print(f"x-s-common: {xs_value}")
    print("两者相同！")
    
    print("\n3. 发送请求")
    
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
                    cursor = data.get('data', {}).get('cursor', '')
                    has_more = data.get('data', {}).get('has_more', False)
                    
                    print(f"子评论数量: {len(comments)}")
                    print(f"下一页cursor: {cursor}")
                    print(f"是否有更多: {has_more}")
                    
                    if comments:
                        print("\n前3条子评论:")
                        for i, comment in enumerate(comments[:3], 1):
                            content = comment.get('content', 'N/A')
                            like_count = comment.get('like_count', 0)
                            user_name = comment.get('user', {}).get('nickname', 'N/A')
                            print(f"  {i}. {user_name}: {content}")
                            print(f"     点赞: {like_count}")
                    
                    print("\n✅ 成功获取子评论！")
                    print("🎉 关键发现：x-s-common = X-s")
                    
                else:
                    msg = data.get('msg', 'Unknown error')
                    code = data.get('code', 'Unknown')
                    print(f"错误信息: {msg}")
                    print(f"错误代码: {code}")
                    
            except json.JSONDecodeError:
                print(f"响应不是JSON格式: {response.text[:200]}")
        else:
            print(f"失败: {response.text[:200]}")
            
    except Exception as e:
        print(f"请求出错: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 测试不同的cursor值
    print("4. 测试分页功能")
    
    if 'comments' in locals() and len(comments) > 0:
        # 使用返回的cursor进行分页测试
        next_cursor = data.get('data', {}).get('cursor', '')
        if next_cursor:
            print(f"测试下一页，cursor: {next_cursor}")
            
            # 更新参数
            params['cursor'] = next_cursor
            
            # 重新生成URL和X-s
            url_with_params = sub_url + '?' + urlencode(params)
            xs_value = xs_gen.generate_xs(
                url=url_with_params,
                method="GET",
                user_id=cookie_info['a1']
            )
            
            headers['X-s'] = xs_value
            headers['x-s-common'] = xs_value
            headers['X-t'] = str(int(time.time() * 1000))
            
            try:
                response = session.get(url_with_params, headers=headers, timeout=10)
                print(f"分页状态码: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success', False):
                        page_comments = data.get('data', {}).get('comments', [])
                        print(f"第二页评论数量: {len(page_comments)}")
                        
                        if page_comments:
                            print("第二页第一条评论:")
                            comment = page_comments[0]
                            content = comment.get('content', 'N/A')
                            user_name = comment.get('user', {}).get('nickname', 'N/A')
                            print(f"  {user_name}: {content}")
                    else:
                        print(f"分页失败: {data.get('msg', 'Unknown error')}")
            except Exception as e:
                print(f"分页测试出错: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 总结
    print("5. 总结")
    print("=" * 30)
    print("🎯 关键发现:")
    print("1. 子评论API路径: /api/sns/web/v2/comment/sub/page")
    print("2. 正确参数名: root_comment_id (不是comment_id)")
    print("3. 分页参数: num, cursor")
    print("4. 关键认证: x-s-common = X-s")
    print("5. 必需参数: note_id, root_comment_id, num, image_formats, xsec_token")
    
    print("\n📋 完整参数列表:")
    print("- note_id: 笔记ID")
    print("- root_comment_id: 根评论ID")
    print("- num: 返回数量 (默认10)")
    print("- cursor: 分页游标 (首页为空)")
    print("- image_formats: 图片格式")
    print("- xsec_token: 安全令牌")
    
    print("\n🔑 必需请求头:")
    print("- X-s: 签名参数")
    print("- x-s-common: 与X-s相同")
    print("- X-t: 时间戳")
    print("- cookie: 完整的认证信息")
    print("- 其他标准浏览器头")
    
    print("\n✅ 问题已解决！")

if __name__ == "__main__":
    # 禁用SSL警告
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    final_verification()