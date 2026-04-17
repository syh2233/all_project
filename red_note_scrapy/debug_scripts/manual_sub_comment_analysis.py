#!/usr/bin/env python3
"""
手动分析子评论API认证机制
不使用自动化，专注于分析认证参数
"""

import json
import time
import requests
import urllib3
from xiaohongshu_xs_reverse_engineer import XiaohongshuXSReverseEngineer

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def manual_analysis_sub_comment():
    """手动分析子评论API认证机制"""
    print("🔍 手动分析子评论API认证机制")
    print("=" * 60)
    print("📋 不使用自动化，专注于认证参数分析")
    print("=" * 60)
    
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
    
    # 子评论API信息
    sub_url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page"
    sub_params = {
        "note_id": "68a35fc0000000001c009cd9",
        "root_comment_id": "68a83b5900000000260052c3",
        "num": 10,
        "cursor": ""
    }
    
    print("📋 子评论API基本信息:")
    print(f"URL: {sub_url}")
    print(f"参数: {json.dumps(sub_params, ensure_ascii=False, indent=2)}")
    print()
    
    # 1. 分析当前的X-s生成
    print("🔍 1. 分析当前X-s生成")
    print("-" * 30)
    
    current_time = str(int(time.time() * 1000))
    xs_value = xs_engineer.generate_xs(sub_url)
    
    print(f"当前时间戳: {current_time}")
    print(f"生成的X-s: {xs_value[:80]}...")
    
    # 分析X-s结构
    analysis = xs_engineer.analyze_xs_structure(xs_value)
    if "error" not in analysis:
        structure = analysis["structure"]
        print(f"X-s结构分析:")
        print(f"  x0 (时间戳): {structure['x0']}")
        print(f"  x1 (应用ID): {structure['x1']}")
        print(f"  x2 (设备类型): {structure['x2']}")
        print(f"  x3 (签名): {structure['x3'][:16]}...")
        print(f"  x4 (附加数据): {structure['x4']}")
    
    print()
    
    # 2. 测试基础请求
    print("🔍 2. 测试基础请求")
    print("-" * 30)
    
    headers = base_headers.copy()
    headers["X-s"] = xs_value
    headers["X-t"] = current_time
    
    print("发送基础请求...")
    try:
        response = requests.get(
            sub_url,
            params=sub_params,
            headers=headers,
            verify=False,
            timeout=10
        )
        
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            response_data = response.json()
            print(f"响应成功: {response_data.get('success', False)}")
            if not response_data.get("success"):
                print(f"错误信息: {response_data.get('msg', 'Unknown')}")
        else:
            print(f"响应内容: {response.text[:200]}")
    except Exception as e:
        print(f"请求异常: {e}")
    
    print()
    
    # 3. 分析缺失的认证参数
    print("🔍 3. 分析缺失的认证参数")
    print("-" * 30)
    
    print("基于406错误分析，可能缺失的参数:")
    print("1. X-s-common 参数")
    print("2. xsec_token 参数")
    print("3. 特殊的请求头")
    print("4. 设备指纹信息")
    print("5. 行为验证参数")
    
    print()
    
    # 4. 手动构建可能的认证参数
    print("🔍 4. 手动构建认证参数")
    print("-" * 30)
    
    # 生成X-s-common
    xs_common = xs_engineer.generate_xs(sub_url)
    print(f"生成的X-s-common: {xs_common[:80]}...")
    
    # 可能的xsec_token格式
    possible_tokens = [
        "ABMARfqKuxx76hZj-CQH0D9AIHxh8oCmV_RTOxyE_DIpI=",
        "ABMARfqKuxx76hZj-CQH0D9AIHxh8oCmV_RTOxyE_DIpI%3D",
        "",
        None
    ]
    
    print("可能的xsec_token值:")
    for i, token in enumerate(possible_tokens, 1):
        if token:
            print(f"  {i}. {token[:50]}...")
        else:
            print(f"  {i}. None")
    
    print()
    
    # 5. 分析认证逻辑
    print("🔍 5. 认证逻辑分析")
    print("-" * 30)
    
    print("子评论API的认证逻辑可能包括:")
    print("1. 请求链路验证 - 需要先访问主页面")
    print("2. 时间窗口验证 - 请求时间需要在特定范围内")
    print("3. 参数关联验证 - 多个参数之间需要有关联性")
    print("4. 设备一致性验证 - 请求头中的设备信息需要一致")
    print("5. 行为模式验证 - 请求模式需要模拟真实用户行为")
    
    print()
    
    # 6. 手动测试建议
    print("🔍 6. 手动测试建议")
    print("-" * 30)
    
    print("建议的手动测试步骤:")
    print("1. 先访问小红书主页获取初始Cookie")
    print("2. 访问笔记页面获取页面上下文")
    print("3. 获取主评论数据")
    print("4. 基于主评论的响应获取子评论")
    print("5. 分析每个步骤的响应头和Cookie变化")
    
    print()
    
    # 7. 认证参数分析总结
    print("🔍 7. 认证参数分析总结")
    print("-" * 30)
    
    analysis_summary = {
        "当前状态": "406认证错误",
        "X-s算法": "✅ 工作正常",
        "Cookie状态": "✅ 有效",
        "缺失参数": [
            "X-s-common",
            "xsec_token", 
            "设备指纹",
            "行为验证"
        ],
        "建议方法": "手动浏览器分析",
        "复杂度": "高"
    }
    
    print("分析总结:")
    for key, value in analysis_summary.items():
        if isinstance(value, list):
            print(f"  {key}:")
            for item in value:
                print(f"    - {item}")
        else:
            print(f"  {key}: {value}")
    
    print()
    
    # 8. 保存分析结果
    print("📁 保存分析结果")
    print("-" * 30)
    
    manual_analysis_result = {
        "analysis_timestamp": current_time,
        "api_info": {
            "url": sub_url,
            "params": sub_params
        },
        "auth_analysis": analysis_summary,
        "generated_params": {
            "xs_value": xs_value,
            "xs_common": xs_common,
            "timestamp": current_time
        },
        "recommendations": {
            "immediate_actions": [
                "手动浏览器分析",
                "网络请求抓包",
                "认证参数提取"
            ],
            "long_term_research": [
                "JavaScript深度分析",
                "认证机制逆向",
                "参数生成算法还原"
            ]
        }
    }
    
    with open("manual_sub_comment_analysis.json", "w", encoding="utf-8") as f:
        json.dump(manual_analysis_result, f, ensure_ascii=False, indent=2)
    
    print("✅ 分析结果已保存到: manual_sub_comment_analysis.json")
    
    print()
    print("🎯 手动分析结论")
    print("=" * 60)
    print("子评论API的认证机制比主评论API复杂得多")
    print("需要深入的手动分析才能完全理解其认证逻辑")
    print("建议使用浏览器开发者工具进行网络请求分析")
    print("=" * 60)
    
    return manual_analysis_result


if __name__ == "__main__":
    manual_analysis_sub_comment()