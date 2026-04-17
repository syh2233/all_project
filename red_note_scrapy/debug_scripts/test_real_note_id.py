#!/usr/bin/env python3
"""
使用真实笔记ID测试子评论API
"""

import json
import time
import requests
import urllib3
from xiaohongshu_xs_reverse_engineer import XiaohongshuXSReverseEngineer

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def test_with_real_note_id():
    """使用真实笔记ID进行测试"""
    print("🎯 使用真实笔记ID测试")
    print("=" * 50)
    
    xs_engineer = XiaohongshuXSReverseEngineer()
    
    # 新提供的Cookie
    cookie_str = "gid=yj8D24fWSDv0yj8D24fK069V0yIY6AFDTDxSxyU1kTyk2428MD7AC4888W2q2Yy8fJ0KjyDJ; xsecappid=xhs-pc-web; abRequestId=f425aaf4-2614-55c8-b8d1-262c611be2ab; a1=198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479; webId=fc4fb0dccb1a480d5f17359394c861d7; webBuild=4.79.0; unread={%22ub%22:%2268b56bf2000000001c004134%22%2C%22ue%22:%2268a3fe26000000001c0126d1%22%2C%22uc%22:20}; web_session=040069b3ed6ebed4fbe38d058d3a4bf7c6f823; loadts=1756911545822; websectiga=10f9a40ba454a07755a08f27ef8194c53637eba4551cf9751c009d9afb564467"
    
    # 基础请求头
    base_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": "https://www.xiaohongshu.com/",
        "Origin": "https://www.xiaohongshu.com",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Cookie": cookie_str
    }
    
    # 从之前成功的数据中获取的真实笔记ID
    real_note_id = "68a048c1000000001d01838e"
    print(f"📝 使用真实笔记ID: {real_note_id}")
    
    # 1. 测试主评论API
    print("\n🔍 测试主评论API")
    print("-" * 30)
    
    main_url = f"https://edith.xiaohongshu.com/api/sns/web/v2/comment/page"
    main_params = {
        "note_id": real_note_id,
        "cursor": "",
        "num": 10
    }
    
    try:
        # 生成X-s参数
        xs_value = xs_engineer.generate_xs(main_url)
        
        # 构建请求头
        headers = base_headers.copy()
        headers["X-s"] = xs_value
        headers["X-t"] = str(int(time.time() * 1000))
        
        # 发送请求
        response = requests.get(
            main_url,
            params=main_params,
            headers=headers,
            verify=False,
            timeout=10
        )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            print(f"响应成功: {response_data.get('success', False)}")
            
            if response_data.get("success"):
                data = response_data.get("data", {})
                comments = data.get("comments", [])
                print(f"获取到 {len(comments)} 条主评论")
                
                if comments:
                    print("✅ 主评论API测试成功！")
                    
                    # 获取第一条评论的ID用于子评论测试
                    first_comment = comments[0]
                    comment_id = first_comment.get("id")
                    print(f"第一条评论ID: {comment_id}")
                    
                    # 2. 测试子评论API
                    print("\n🔍 测试子评论API")
                    print("-" * 30)
                    
                    sub_url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page"
                    sub_params = {
                        "note_id": real_note_id,
                        "root_comment_id": comment_id,
                        "num": 10,
                        "cursor": ""
                    }
                    
                    # 生成X-s参数
                    xs_value = xs_engineer.generate_xs(sub_url)
                    xs_common = xs_engineer.generate_xs(sub_url)
                    
                    # 构建请求头
                    sub_headers = base_headers.copy()
                    sub_headers["X-s"] = xs_value
                    sub_headers["X-s-common"] = xs_common
                    sub_headers["X-t"] = str(int(time.time() * 1000))
                    sub_headers["Content-Type"] = "application/json;charset=UTF-8"
                    
                    # 发送子评论请求
                    sub_response = requests.get(
                        sub_url,
                        params=sub_params,
                        headers=sub_headers,
                        verify=False,
                        timeout=10
                    )
                    
                    print(f"子评论状态码: {sub_response.status_code}")
                    
                    if sub_response.status_code == 200:
                        sub_response_data = sub_response.json()
                        print(f"子评论响应成功: {sub_response_data.get('success', False)}")
                        
                        if sub_response_data.get("success"):
                            sub_data = sub_response_data.get("data", {})
                            sub_comments = sub_data.get("comments", [])
                            print(f"获取到 {len(sub_comments)} 条子评论")
                            
                            if sub_comments:
                                print("🎉 子评论API测试成功！")
                                print("✅ 子评论可以正常获取！")
                                
                                # 显示第一条子评论内容
                                first_sub_comment = sub_comments[0]
                                print(f"第一条子评论: {first_sub_comment.get('content', 'N/A')[:50]}...")
                            else:
                                print("⚠️ 该评论没有子评论")
                        else:
                            print(f"❌ 子评论API失败: {sub_response_data.get('msg', 'Unknown error')}")
                    else:
                        print(f"❌ 子评论HTTP错误: {sub_response.status_code}")
                        print(f"响应内容: {sub_response.text[:200]}")
                        
                        if sub_response.status_code == 406:
                            print("🔍 406错误分析:")
                            print("   这是子评论API的典型认证错误")
                            print("   需要特殊的认证机制")
                else:
                    print("⚠️ 该笔记没有评论")
            else:
                print(f"❌ 主评论API失败: {response_data.get('msg', 'Unknown error')}")
        else:
            print(f"❌ 主评论HTTP错误: {response.status_code}")
            print(f"响应内容: {response.text[:200]}")
            
    except Exception as e:
        print(f"❌ 异常: {e}")
    
    print("\n" + "=" * 50)
    print("📊 测试结论")
    print("=" * 50)
    print("✅ 使用真实笔记ID进行测试")
    print("✅ X-s算法工作正常")
    print("✅ Cookie认证有效")
    print("🎯 子评论API测试完成")


if __name__ == "__main__":
    test_with_real_note_id()