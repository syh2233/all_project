#!/usr/bin/env python3
"""
测试当前时间生成的笔记ID
"""

import json
import time
import requests
import urllib3
from xiaohongshu_xs_reverse_engineer import XiaohongshuXSReverseEngineer

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def test_current_time_notes():
    """测试当前时间生成的笔记ID"""
    print("🕐 测试当前时间生成的笔记ID")
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
    
    # 生成当前时间戳相关的笔记ID
    current_time = int(time.time() * 1000)
    
    # 生成多个不同时间偏移的ID
    test_ids = []
    
    # 当前时间
    hex_time = hex(current_time)[2:]
    note_id = f"{hex_time}{'0' * (24 - len(hex_time))}"[:24]
    test_ids.append(("当前时间", note_id))
    
    # 1小时前
    hour_ago = current_time - 3600000
    hex_time = hex(hour_ago)[2:]
    note_id = f"{hex_time}{'0' * (24 - len(hex_time))}"[:24]
    test_ids.append(("1小时前", note_id))
    
    # 1天前
    day_ago = current_time - 86400000
    hex_time = hex(day_ago)[2:]
    note_id = f"{hex_time}{'0' * (24 - len(hex_time))}"[:24]
    test_ids.append(("1天前", note_id))
    
    # 1周前
    week_ago = current_time - 604800000
    hex_time = hex(week_ago)[2:]
    note_id = f"{hex_time}{'0' * (24 - len(hex_time))}"[:24]
    test_ids.append(("1周前", note_id))
    
    print("📝 测试的笔记ID:")
    for name, note_id in test_ids:
        print(f"   {name}: {note_id}")
    
    results = []
    
    for name, note_id in test_ids:
        print(f"\n🔍 测试 {name}: {note_id}")
        print("-" * 40)
        
        # 测试主评论API
        main_url = f"https://edith.xiaohongshu.com/api/sns/web/v2/comment/page"
        main_params = {
            "note_id": note_id,
            "cursor": "",
            "num": 5
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
                success = response_data.get("success", False)
                msg = response_data.get("msg", "No message")
                
                print(f"响应成功: {success}")
                print(f"响应消息: {msg}")
                
                if success:
                    data = response_data.get("data", {})
                    comments = data.get("comments", [])
                    print(f"评论数量: {len(comments)}")
                    
                    result = {
                        "name": name,
                        "note_id": note_id,
                        "success": True,
                        "comment_count": len(comments),
                        "has_comments": len(comments) > 0
                    }
                    
                    # 如果有评论，尝试获取子评论
                    if comments:
                        first_comment = comments[0]
                        comment_id = first_comment.get("id")
                        
                        if comment_id:
                            print(f"测试子评论 (评论ID: {comment_id})")
                            
                            sub_url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page"
                            sub_params = {
                                "note_id": note_id,
                                "root_comment_id": comment_id,
                                "num": 5,
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
                                sub_success = sub_response_data.get("success", False)
                                sub_msg = sub_response_data.get("msg", "No message")
                                
                                print(f"子评论成功: {sub_success}")
                                print(f"子评论消息: {sub_msg}")
                                
                                if sub_success:
                                    sub_data = sub_response_data.get("data", {})
                                    sub_comments = sub_data.get("comments", [])
                                    print(f"子评论数量: {len(sub_comments)}")
                                    
                                    result["sub_comment_success"] = True
                                    result["sub_comment_count"] = len(sub_comments)
                                else:
                                    result["sub_comment_success"] = False
                                    result["sub_comment_error"] = sub_msg
                            else:
                                result["sub_comment_success"] = False
                                result["sub_comment_http_error"] = sub_response.status_code
                    else:
                        result["sub_comment_success"] = False
                        result["no_comments"] = True
                else:
                    result = {
                        "name": name,
                        "note_id": note_id,
                        "success": False,
                        "error": msg
                    }
            else:
                print(f"HTTP错误: {response.status_code}")
                result = {
                    "name": name,
                    "note_id": note_id,
                    "success": False,
                    "http_error": response.status_code
                }
                
        except Exception as e:
            print(f"异常: {e}")
            result = {
                "name": name,
                "note_id": note_id,
                "success": False,
                "exception": str(e)
            }
        
        results.append(result)
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("📊 测试结果汇总")
    print("=" * 60)
    
    main_success_count = sum(1 for r in results if r.get("success"))
    sub_success_count = sum(1 for r in results if r.get("sub_comment_success"))
    
    print(f"测试的笔记数量: {len(results)}")
    print(f"主评论成功: {main_success_count}")
    print(f"子评论成功: {sub_success_count}")
    
    if main_success_count > 0:
        print("\n🎉 成功获取到主评论数据！")
        print("✅ X-s算法工作正常")
        print("✅ Cookie认证有效")
        
        if sub_success_count > 0:
            print("🎉 成功获取到子评论数据！")
            print("✅ 子评论API突破成功！")
        else:
            print("\n⚠️ 子评论API仍然存在问题")
            print("💡 需要进一步分析子评论的特殊要求")
    else:
        print("\n❌ 未能获取到任何评论数据")
        print("💡 可能的原因:")
        print("   1. 笔记ID格式不正确")
        print("   2. 笔记不存在或已删除")
        print("   3. API限制或风控")
        print("   4. Cookie权限不足")
    
    # 保存结果
    final_results = {
        "test_summary": {
            "total_tests": len(results),
            "main_success": main_success_count,
            "sub_success": sub_success_count,
            "timestamp": current_time
        },
        "detailed_results": results
    }
    
    with open("current_time_test_results.json", "w", encoding="utf-8") as f:
        json.dump(final_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n📁 详细结果已保存到: current_time_test_results.json")
    
    return final_results


if __name__ == "__main__":
    test_current_time_notes()