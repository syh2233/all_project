#!/usr/bin/env python3
"""
深度测试子评论API的不同方法
"""

import json
import time
import requests
import urllib3
from xiaohongshu_xs_reverse_engineer import XiaohongshuXSReverseEngineer

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def deep_test_sub_comment_api():
    """深度测试子评论API的不同方法"""
    print("🔬 深度测试子评论API的不同方法")
    print("=" * 60)
    
    xs_engineer = XiaohongshuXSReverseEngineer()
    
    # 新提供的Cookie
    cookie_str = "gid=yj8D24fWSDv0yj8D24fK069V0yIY6AFDTDxSxyU1kTyk2428MD7AC4888W2q2Yy8fJ0KjyDJ; xsecappid=xhs-pc-web; abRequestId=f425aaf4-2614-55c8-b8d1-262c611be2ab; a1=198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479; webId=fc4fb0dccb1a480d5f17359394c861d7; webBuild=4.79.0; unread={%22ub%22:%2268b56bf2000000001c004134%22%2C%22ue%22:%2268a3fe26000000001c0126d1%22%2C%22uc%22:20}; web_session=040069b3ed6ebed4fbe38d058d3a4bf7c6f823; loadts=1756911545822; websectiga=10f9a40ba454a07755a08f27ef8194c53637eba4551cf9751c009d9afb564467"
    
    # API参数
    base_url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page"
    params = {
        "note_id": "68a35fc0000000001c009cd9",
        "root_comment_id": "68a83b5900000000260052c3",
        "num": 10,
        "cursor": ""
    }
    
    # 不同的测试方法
    test_methods = [
        {
            "name": "GET请求 + 基础X-s",
            "method": "GET",
            "headers": {
                "X-s": None,  # 将在运行时生成
                "X-t": None,
                "Content-Type": "application/json;charset=UTF-8"
            },
            "params": params
        },
        {
            "name": "GET请求 + X-s + X-s-common",
            "method": "GET",
            "headers": {
                "X-s": None,
                "X-s-common": None,
                "X-t": None,
                "Content-Type": "application/json;charset=UTF-8"
            },
            "params": params
        },
        {
            "name": "POST请求 + X-s + X-s-common",
            "method": "POST",
            "headers": {
                "X-s": None,
                "X-s-common": None,
                "X-t": None,
                "Content-Type": "application/json;charset=UTF-8"
            },
            "params": params
        },
        {
            "name": "GET请求 + 完整浏览器头",
            "method": "GET",
            "headers": {
                "X-s": None,
                "X-s-common": None,
                "X-t": None,
                "Content-Type": "application/json;charset=UTF-8",
                "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
                "Cache-Control": "no-cache",
                "Pragma": "no-cache"
            },
            "params": params
        },
        {
            "name": "GET请求 + xsec_token",
            "method": "GET",
            "headers": {
                "X-s": None,
                "X-s-common": None,
                "X-t": None,
                "Content-Type": "application/json;charset=UTF-8",
                "xsec_token": "ABMARfqKuxx76hZj-CQH0D9AIHxh8oCmV_RTOxyE_DIpI="
            },
            "params": params
        },
        {
            "name": "GET请求 + trace-id",
            "method": "GET",
            "headers": {
                "X-s": None,
                "X-s-common": None,
                "X-t": None,
                "Content-Type": "application/json;charset=UTF-8",
                "trace-id": f"{int(time.time() * 1000)}"
            },
            "params": params
        }
    ]
    
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
    
    results = []
    
    for i, test_method in enumerate(test_methods):
        print(f"\n🔬 测试方法 {i+1}: {test_method['name']}")
        print("-" * 50)
        
        try:
            # 构建完整请求头
            headers = base_headers.copy()
            
            # 生成X-s参数
            timestamp = str(int(time.time() * 1000))
            xs_value = xs_engineer.generate_xs(base_url)
            xs_common = xs_engineer.generate_xs(base_url)
            
            # 添加测试方法的请求头
            for key, value in test_method["headers"].items():
                if key == "X-s":
                    headers[key] = xs_value
                elif key == "X-s-common":
                    headers[key] = xs_common
                elif key == "X-t":
                    headers[key] = timestamp
                else:
                    headers[key] = value
            
            print(f"请求方法: {test_method['method']}")
            print(f"关键请求头:")
            for key in ["X-s", "X-s-common", "X-t", "xsec_token", "trace-id"]:
                if key in headers:
                    print(f"  {key}: {headers[key][:50]}..." if len(headers[key]) > 50 else f"  {key}: {headers[key]}")
            
            # 发送请求
            if test_method["method"] == "GET":
                response = requests.get(
                    base_url,
                    params=test_method["params"],
                    headers=headers,
                    verify=False,
                    timeout=10
                )
            else:
                response = requests.post(
                    base_url,
                    json=test_method["params"],
                    headers=headers,
                    verify=False,
                    timeout=10
                )
            
            print(f"\n状态码: {response.status_code}")
            
            if response.status_code == 200:
                response_data = response.json()
                print(f"响应成功: {response_data.get('success', False)}")
                
                if response_data.get("success"):
                    data = response_data.get("data", {})
                    comments = data.get("comments", [])
                    print(f"✅ 成功获取到 {len(comments)} 条子评论！")
                    
                    result = {
                        "method": test_method["name"],
                        "success": True,
                        "comment_count": len(comments),
                        "has_comments": len(comments) > 0,
                        "status_code": response.status_code
                    }
                else:
                    msg = response_data.get("msg", "未知错误")
                    print(f"❌ 失败: {msg}")
                    
                    result = {
                        "method": test_method["name"],
                        "success": False,
                        "error": msg,
                        "status_code": response.status_code
                    }
            else:
                print(f"❌ HTTP错误: {response.status_code}")
                print(f"响应内容: {response.text[:200]}")
                
                result = {
                    "method": test_method["name"],
                    "success": False,
                    "http_error": response.status_code,
                    "response_text": response.text[:500]
                }
                
        except Exception as e:
            print(f"❌ 异常: {e}")
            result = {
                "method": test_method["name"],
                "success": False,
                "exception": str(e)
            }
        
        results.append(result)
        
        # 避免请求过快
        time.sleep(0.5)
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("📊 深度测试结果汇总")
    print("=" * 60)
    
    success_count = sum(1 for r in results if r.get("success"))
    
    print(f"测试方法数量: {len(results)}")
    print(f"成功数量: {success_count}")
    
    if success_count > 0:
        print("🎉 成功！找到有效的子评论获取方法！")
        
        print("\n✅ 成功的方法:")
        for result in results:
            if result.get("success"):
                print(f"   - {result['method']}: {result['comment_count']} 条子评论")
    else:
        print("❌ 所有方法都失败了")
        print("💡 子评论API需要特殊的认证机制")
        print("🔍 可能需要:")
        print("   1. 浏览器环境")
        print("   2. 特殊的JavaScript计算")
        print("   3. 设备指纹")
        print("   4. 行为序列验证")
        
        print("\n❌ 失败的方法详情:")
        for result in results:
            status = "406" if result.get("http_error") == 406 else "其他错误"
            error = result.get("error", result.get("http_error", result.get("exception", "Unknown")))
            print(f"   - {result['method']}: {status} - {error}")
    
    # 保存结果
    final_results = {
        "test_summary": {
            "total_methods": len(results),
            "success_count": success_count,
            "success_rate": f"{(success_count/len(results)*100):.1f}%" if len(results) > 0 else "0%"
        },
        "method_results": results,
        "conclusion": {
            "sub_comment_accessible": success_count > 0,
            "needs_browser_environment": success_count == 0,
            "recommended_approach": "browser_automation" if success_count == 0 else "direct_api"
        }
    }
    
    with open("deep_sub_comment_test_results.json", "w", encoding="utf-8") as f:
        json.dump(final_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n📁 详细结果已保存到: deep_sub_comment_test_results.json")
    
    return final_results


if __name__ == "__main__":
    deep_test_sub_comment_api()