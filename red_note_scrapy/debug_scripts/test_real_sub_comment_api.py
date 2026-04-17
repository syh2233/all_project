#!/usr/bin/env python3
"""
测试真实的子评论API
"""

import json
import time
import requests
import urllib3
from xiaohongshu_xs_reverse_engineer import XiaohongshuXSReverseEngineer

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def test_real_sub_comment_api():
    """测试真实的子评论API"""
    print("🎯 测试真实的子评论API")
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
    
    # 真实的子评论API参数
    base_url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page"
    
    # 测试不同的参数组合
    test_cases = [
        {
            "name": "完整参数（包含xsec_token）",
            "params": {
                "note_id": "68a35fc0000000001c009cd9",
                "root_comment_id": "68a83b5900000000260052c3",
                "num": 10,
                "cursor": "68a83ccd000000002700255f",
                "image_formats": "jpg,webp,avif",
                "top_comment_id": "",
                "xsec_token": "ABMARfqKuxx76hZj-CQH0D9AIHxh8oCmV_RTOxyE_DIpI%3D"
            }
        },
        {
            "name": "基础参数",
            "params": {
                "note_id": "68a35fc0000000001c009cd9",
                "root_comment_id": "68a83b5900000000260052c3",
                "num": 10,
                "cursor": ""
            }
        },
        {
            "name": "带cursor参数",
            "params": {
                "note_id": "68a35fc0000000001c009cd9",
                "root_comment_id": "68a83b5900000000260052c3",
                "num": 10,
                "cursor": "68a83ccd000000002700255f"
            }
        },
        {
            "name": "带image_formats参数",
            "params": {
                "note_id": "68a35fc0000000001c009cd9",
                "root_comment_id": "68a83b5900000000260052c3",
                "num": 10,
                "cursor": "",
                "image_formats": "jpg,webp,avif"
            }
        }
    ]
    
    results = []
    
    for test_case in test_cases:
        print(f"\n🔍 测试 {test_case['name']}")
        print("-" * 50)
        print(f"参数: {json.dumps(test_case['params'], ensure_ascii=False, indent=2)}")
        
        try:
            # 生成X-s参数
            xs_value = xs_engineer.generate_xs(base_url)
            xs_common = xs_engineer.generate_xs(base_url)
            
            # 构建请求头
            headers = base_headers.copy()
            headers["X-s"] = xs_value
            headers["X-s-common"] = xs_common
            headers["X-t"] = str(int(time.time() * 1000))
            headers["Content-Type"] = "application/json;charset=UTF-8"
            
            # 如果有xsec_token，添加到请求头
            if "xsec_token" in test_case["params"]:
                headers["xsec_token"] = test_case["params"]["xsec_token"].replace("%3D", "=")
            
            print(f"关键请求头:")
            print(f"  X-s: {xs_value[:50]}...")
            print(f"  X-s-common: {xs_common[:50]}...")
            print(f"  X-t: {headers['X-t']}")
            if "xsec_token" in headers:
                print(f"  xsec_token: {headers['xsec_token']}")
            
            # 发送请求
            response = requests.get(
                base_url,
                params=test_case["params"],
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
                    
                    if comments:
                        print("📝 第一条子评论详情:")
                        first_comment = comments[0]
                        print(f"   ID: {first_comment.get('id', 'N/A')}")
                        print(f"   内容: {first_comment.get('content', 'N/A')[:100]}...")
                        print(f"   用户: {first_comment.get('user_info', {}).get('nickname', 'N/A')}")
                        print(f"   点赞: {first_comment.get('like_count', 0)}")
                        print(f"   时间: {first_comment.get('create_time', 'N/A')}")
                    
                    result = {
                        "test_case": test_case["name"],
                        "success": True,
                        "comment_count": len(comments),
                        "has_comments": len(comments) > 0,
                        "response_data": response_data
                    }
                else:
                    msg = response_data.get("msg", "未知错误")
                    print(f"❌ 失败: {msg}")
                    
                    result = {
                        "test_case": test_case["name"],
                        "success": False,
                        "error": msg,
                        "response_data": response_data
                    }
            else:
                print(f"❌ HTTP错误: {response.status_code}")
                print(f"响应内容: {response.text[:500]}")
                
                result = {
                    "test_case": test_case["name"],
                    "success": False,
                    "http_error": response.status_code,
                    "response_text": response.text[:1000]
                }
                
        except Exception as e:
            print(f"❌ 异常: {e}")
            result = {
                "test_case": test_case["name"],
                "success": False,
                "exception": str(e)
            }
        
        results.append(result)
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("📊 测试结果汇总")
    print("=" * 60)
    
    success_count = sum(1 for r in results if r.get("success"))
    
    print(f"测试用例数量: {len(results)}")
    print(f"成功数量: {success_count}")
    
    if success_count > 0:
        print("🎉 成功！子评论API可以正常获取！")
        
        # 显示成功的测试用例
        print("\n✅ 成功的测试用例:")
        for result in results:
            if result.get("success"):
                print(f"   - {result['test_case']}: {result['comment_count']} 条子评论")
        
        print("\n🎯 子评论获取功能已突破！")
        print("✅ X-s算法工作正常")
        print("✅ Cookie认证有效")
        print("✅ 子评论API认证成功")
    else:
        print("❌ 所有测试用例都失败了")
        print("💡 可能的原因:")
        print("   1. xsec_token参数问题")
        print("   2. X-s-common参数问题")
        print("   3. 请求头缺失")
        print("   4. 参数格式问题")
        
        # 显示失败的详细信息
        print("\n❌ 失败的测试用例:")
        for result in results:
            if not result.get("success"):
                print(f"   - {result['test_case']}: {result.get('error', result.get('http_error', 'Unknown error'))}")
    
    # 保存结果
    final_results = {
        "test_summary": {
            "total_tests": len(results),
            "success_count": success_count,
            "success_rate": f"{(success_count/len(results)*100):.1f}%"
        },
        "detailed_results": results,
        "api_info": {
            "base_url": base_url,
            "note_id": "68a35fc0000000001c009cd9",
            "root_comment_id": "68a83b5900000000260052c3"
        }
    }
    
    with open("real_sub_comment_test_results.json", "w", encoding="utf-8") as f:
        json.dump(final_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n📁 详细结果已保存到: real_sub_comment_test_results.json")
    
    return final_results


if __name__ == "__main__":
    test_real_sub_comment_api()