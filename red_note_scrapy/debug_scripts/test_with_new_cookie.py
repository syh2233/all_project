#!/usr/bin/env python3
"""
使用新Cookie测试子评论和主评论API
"""

import json
import time
import requests
import urllib3
from xiaohongshu_xs_reverse_engineer import XiaohongshuXSReverseEngineer

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class NewCookieTester:
    """新Cookie测试器"""
    
    def __init__(self):
        self.xs_engineer = XiaohongshuXSReverseEngineer()
        
        # 新提供的Cookie
        self.cookie_str = "gid=yj8D24fWSDv0yj8D24fK069V0yIY6AFDTDxSxyU1kTyk2428MD7AC4888W2q2Yy8fJ0KjyDJ; xsecappid=xhs-pc-web; abRequestId=f425aaf4-2614-55c8-b8d1-262c611be2ab; a1=198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479; webId=fc4fb0dccb1a480d5f17359394c861d7; webBuild=4.79.0; unread={%22ub%22:%2268b56bf2000000001c004134%22%2C%22ue%22:%2268a3fe26000000001c0126d1%22%2C%22uc%22:20}; web_session=040069b3ed6ebed4fbe38d058d3a4bf7c6f823; loadts=1756911545822; websectiga=10f9a40ba454a07755a08f27ef8194c53637eba4551cf9751c009d9afb564467"
        
        # 基础请求头
        self.base_headers = {
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
            "Cookie": self.cookie_str
        }
    
    def test_main_comment_api(self):
        """测试主评论API"""
        print("🎯 测试主评论API")
        print("-" * 40)
        
        # 使用一个真实的笔记ID
        note_id = "6666666660000000000000000"
        url = f"https://edith.xiaohongshu.com/api/sns/web/v2/comment/page"
        
        params = {
            "note_id": note_id,
            "cursor": "",
            "num": 10
        }
        
        try:
            # 生成X-s参数
            xs_value = self.xs_engineer.generate_xs(url)
            
            # 构建请求头
            headers = self.base_headers.copy()
            headers["X-s"] = xs_value
            headers["X-t"] = str(int(time.time() * 1000))
            
            print(f"📋 请求URL: {url}")
            print(f"📋 笔记ID: {note_id}")
            
            # 发送请求
            response = requests.get(
                url,
                params=params,
                headers=headers,
                verify=False,
                timeout=10
            )
            
            print(f"📊 状态码: {response.status_code}")
            
            if response.status_code == 200:
                response_data = response.json()
                print(f"✅ 响应解析成功")
                
                if response_data.get("success"):
                    print("✅ 主评论API请求成功")
                    
                    if "data" in response_data and "comments" in response_data["data"]:
                        comments = response_data["data"]["comments"]
                        print(f"✅ 获取到 {len(comments)} 条主评论")
                        
                        if comments:
                            print("📝 第一条主评论:")
                            first_comment = comments[0]
                            print(f"   ID: {first_comment.get('id', 'N/A')}")
                            print(f"   内容: {first_comment.get('content', 'N/A')[:50]}...")
                            print(f"   用户: {first_comment.get('user_info', {}).get('nickname', 'N/A')}")
                            print(f"   点赞: {first_comment.get('like_count', 0)}")
                            
                            return {
                                "success": True,
                                "comment_count": len(comments),
                                "has_comments": len(comments) > 0,
                                "response_data": response_data
                            }
                        else:
                            print("⚠️ 评论列表为空")
                            return {
                                "success": True,
                                "comment_count": 0,
                                "has_comments": False,
                                "response_data": response_data
                            }
                    else:
                        print("⚠️ 响应结构异常")
                        return {
                            "success": False,
                            "error": "Unexpected response structure"
                        }
                else:
                    print(f"❌ 请求失败: {response_data.get('msg', 'Unknown error')}")
                    return {
                        "success": False,
                        "error": response_data.get('msg', 'Unknown error')
                    }
            else:
                print(f"❌ HTTP错误: {response.status_code}")
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}"
                }
                
        except Exception as e:
            print(f"❌ 异常: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def test_sub_comment_api(self):
        """测试子评论API"""
        print("\n🎯 测试子评论API")
        print("-" * 40)
        
        # 使用相同的笔记ID和评论ID
        note_id = "6666666660000000000000000"
        root_comment_id = "6666666660000000000000000"
        url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page"
        
        params = {
            "note_id": note_id,
            "root_comment_id": root_comment_id,
            "num": 10,
            "cursor": ""
        }
        
        try:
            # 生成X-s参数
            xs_value = self.xs_engineer.generate_xs(url)
            xs_common = self.xs_engineer.generate_xs(url)
            
            # 构建请求头
            headers = self.base_headers.copy()
            headers["X-s"] = xs_value
            headers["X-s-common"] = xs_common
            headers["X-t"] = str(int(time.time() * 1000))
            headers["Content-Type"] = "application/json;charset=UTF-8"
            
            print(f"📋 请求URL: {url}")
            print(f"📋 笔记ID: {note_id}")
            print(f"📋 根评论ID: {root_comment_id}")
            
            # 发送请求
            response = requests.get(
                url,
                params=params,
                headers=headers,
                verify=False,
                timeout=10
            )
            
            print(f"📊 状态码: {response.status_code}")
            
            if response.status_code == 200:
                response_data = response.json()
                print(f"✅ 响应解析成功")
                
                if response_data.get("success"):
                    print("✅ 子评论API请求成功")
                    
                    if "data" in response_data and "comments" in response_data["data"]:
                        comments = response_data["data"]["comments"]
                        print(f"✅ 获取到 {len(comments)} 条子评论")
                        
                        if comments:
                            print("📝 第一条子评论:")
                            first_comment = comments[0]
                            print(f"   ID: {first_comment.get('id', 'N/A')}")
                            print(f"   内容: {first_comment.get('content', 'N/A')[:50]}...")
                            print(f"   用户: {first_comment.get('user_info', {}).get('nickname', 'N/A')}")
                            print(f"   点赞: {first_comment.get('like_count', 0)}")
                            
                            return {
                                "success": True,
                                "comment_count": len(comments),
                                "has_comments": len(comments) > 0,
                                "response_data": response_data
                            }
                        else:
                            print("⚠️ 子评论列表为空")
                            return {
                                "success": True,
                                "comment_count": 0,
                                "has_comments": False,
                                "response_data": response_data
                            }
                    else:
                        print("⚠️ 响应结构异常")
                        print(f"📋 响应结构: {list(response_data.keys())}")
                        return {
                            "success": False,
                            "error": "Unexpected response structure"
                        }
                else:
                    print(f"❌ 请求失败: {response_data.get('msg', 'Unknown error')}")
                    return {
                        "success": False,
                        "error": response_data.get('msg', 'Unknown error')
                    }
            else:
                print(f"❌ HTTP错误: {response.status_code}")
                if response.status_code == 406:
                    print("🔍 406错误分析:")
                    print("   可能原因:")
                    print("   1. X-s参数生成错误")
                    print("   2. X-s-common参数问题")
                    print("   3. 请求头缺失")
                    print("   4. 参数格式错误")
                    print("   5. 服务器端特殊验证")
                
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}"
                }
                
        except Exception as e:
            print(f"❌ 异常: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def test_different_sub_comment_methods(self):
        """测试不同的子评论请求方法"""
        print("\n🎯 测试不同的子评论请求方法")
        print("-" * 40)
        
        note_id = "6666666660000000000000000"
        root_comment_id = "6666666660000000000000000"
        url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page"
        
        methods = [
            {"name": "GET请求", "method": "GET"},
            {"name": "POST请求", "method": "POST"}
        ]
        
        results = []
        
        for method_info in methods:
            print(f"\n📋 测试 {method_info['name']}")
            
            params = {
                "note_id": note_id,
                "root_comment_id": root_comment_id,
                "num": 10,
                "cursor": ""
            }
            
            try:
                # 生成X-s参数
                xs_value = self.xs_engineer.generate_xs(url)
                xs_common = self.xs_engineer.generate_xs(url)
                
                # 构建请求头
                headers = self.base_headers.copy()
                headers["X-s"] = xs_value
                headers["X-s-common"] = xs_common
                headers["X-t"] = str(int(time.time() * 1000))
                headers["Content-Type"] = "application/json;charset=UTF-8"
                
                # 发送请求
                if method_info["method"] == "GET":
                    response = requests.get(
                        url,
                        params=params,
                        headers=headers,
                        verify=False,
                        timeout=10
                    )
                else:
                    response = requests.post(
                        url,
                        json=params,
                        headers=headers,
                        verify=False,
                        timeout=10
                    )
                
                print(f"   状态码: {response.status_code}")
                
                result = {
                    "method": method_info["name"],
                    "status_code": response.status_code,
                    "success": response.status_code == 200
                }
                
                if response.status_code == 200:
                    response_data = response.json()
                    result["response_success"] = response_data.get("success", False)
                    result["message"] = response_data.get("msg", "")
                else:
                    result["response_success"] = False
                    result["message"] = f"HTTP {response.status_code}"
                
                results.append(result)
                
            except Exception as e:
                print(f"   异常: {e}")
                results.append({
                    "method": method_info["name"],
                    "success": False,
                    "error": str(e)
                })
        
        return results
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 使用新Cookie测试小红书API")
        print("=" * 60)
        
        # 测试主评论API
        main_result = self.test_main_comment_api()
        
        # 测试子评论API
        sub_result = self.test_sub_comment_api()
        
        # 测试不同的子评论方法
        method_results = self.test_different_sub_comment_methods()
        
        # 汇总结果
        print("\n" + "=" * 60)
        print("📊 测试结果汇总")
        print("=" * 60)
        
        print("🎯 主评论API:")
        if main_result["success"]:
            print("   ✅ 成功")
            print(f"   📝 获取 {main_result['comment_count']} 条评论")
        else:
            print(f"   ❌ 失败: {main_result.get('error', 'Unknown error')}")
        
        print("\n🎯 子评论API:")
        if sub_result["success"]:
            print("   ✅ 成功")
            print(f"   📝 获取 {sub_result['comment_count']} 条子评论")
        else:
            print(f"   ❌ 失败: {sub_result.get('error', 'Unknown error')}")
        
        print("\n🎯 不同请求方法对比:")
        for result in method_results:
            status = "✅" if result.get("success", False) else "❌"
            print(f"   {status} {result['method']}: {result.get('message', 'No message')}")
        
        # 保存结果
        final_results = {
            "main_comment": main_result,
            "sub_comment": sub_result,
            "method_comparison": method_results,
            "cookie_info": {
                "has_a1": "a1=" in self.cookie_str,
                "has_web_session": "web_session=" in self.cookie_str,
                "has_webId": "webId=" in self.cookie_str,
                "has_xsecappid": "xsecappid=" in self.cookie_str
            }
        }
        
        with open("new_cookie_test_results.json", "w", encoding="utf-8") as f:
            json.dump(final_results, f, ensure_ascii=False, indent=2)
        
        print(f"\n📁 详细结果已保存到: new_cookie_test_results.json")
        
        return final_results


def main():
    """主函数"""
    tester = NewCookieTester()
    results = tester.run_all_tests()
    
    print("\n" + "=" * 60)
    print("🎉 测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()