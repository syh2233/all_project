#!/usr/bin/env python3
"""
使用逆向工程成果测试子评论API
"""

import json
import time
import requests
import urllib3
from xiaohongshu_xs_reverse_engineer import XiaohongshuXSReverseEngineer

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class SubCommentTester:
    """子评论API测试器"""
    
    def __init__(self):
        self.xs_engineer = XiaohongshuXSReverseEngineer()
        
        # 有效的Cookie (请定期更新)
        self.cookie_str = "a1=18810038977; webId=1234567890; web_session=04006789012345678901234567890123; webBuild=2.12.4; xsecappid=xhs-pc-web;"
        
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
        
        # 测试用例
        self.test_cases = [
            {
                "name": "标准子评论API",
                "url": "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page",
                "method": "GET",
                "params": {
                    "note_id": "6666666660000000000000000",
                    "root_comment_id": "6666666660000000000000000",
                    "num": 10,
                    "cursor": ""
                }
            },
            {
                "name": "替代子评论API",
                "url": "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page", 
                "method": "POST",
                "params": {
                    "note_id": "6666666660000000000000000",
                    "root_comment_id": "6666666660000000000000000",
                    "num": 10,
                    "cursor": ""
                }
            }
        ]
    
    def test_sub_comment_api(self, test_case):
        """测试子评论API"""
        print(f"\n🧪 测试: {test_case['name']}")
        print("-" * 50)
        
        url = test_case['url']
        method = test_case['method']
        params = test_case['params']
        
        try:
            # 生成X-s参数
            print("📝 生成X-s参数...")
            xs_value = self.xs_engineer.generate_xs(url)
            print(f"✅ X-s生成成功: {xs_value[:50]}...")
            
            # 生成X-s-common参数
            xs_common = self.xs_engineer.generate_xs(url)
            print(f"✅ X-s-common生成成功: {xs_common[:50]}...")
            
            # 构建请求头
            headers = self.base_headers.copy()
            headers["X-s"] = xs_value
            headers["X-s-common"] = xs_common
            headers["X-t"] = str(int(time.time() * 1000))
            headers["Content-Type"] = "application/json;charset=UTF-8"
            
            print(f"📋 请求URL: {url}")
            print(f"📋 请求参数: {json.dumps(params, ensure_ascii=False, indent=2)}")
            print(f"📋 关键请求头:")
            for key in ["X-s", "X-s-common", "X-t", "Cookie"]:
                if key in headers:
                    print(f"   {key}: {headers[key][:50]}...")
            
            # 发送请求
            print("\n🚀 发送请求...")
            start_time = time.time()
            
            if method.upper() == "GET":
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
            
            end_time = time.time()
            
            print(f"⏱️  响应时间: {(end_time - start_time):.2f}秒")
            print(f"📊 状态码: {response.status_code}")
            print(f"📊 响应头: {dict(response.headers)}")
            
            # 分析响应
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    print(f"✅ 响应解析成功")
                    
                    # 分析响应结构
                    if "data" in response_data:
                        data = response_data["data"]
                        if "comments" in data:
                            comments = data["comments"]
                            print(f"✅ 获取到 {len(comments)} 条子评论")
                            
                            if comments:
                                print("📝 第一条子评论示例:")
                                first_comment = comments[0]
                                print(f"   ID: {first_comment.get('id', 'N/A')}")
                                print(f"   内容: {first_comment.get('content', 'N/A')[:50]}...")
                                print(f"   用户: {first_comment.get('user_info', {}).get('nickname', 'N/A')}")
                                print(f"   点赞: {first_comment.get('like_count', 0)}")
                                
                                return {
                                    "success": True,
                                    "comment_count": len(comments),
                                    "response_data": response_data
                                }
                            else:
                                print("⚠️ 响应数据为空")
                                return {
                                    "success": True,
                                    "comment_count": 0,
                                    "response_data": response_data
                                }
                        else:
                            print("⚠️ 响应中未找到comments字段")
                            print(f"📋 响应结构: {list(response_data.keys())}")
                            return {
                                "success": False,
                                "error": "No comments field in response"
                            }
                    else:
                        print("⚠️ 响应中未找到data字段")
                        print(f"📋 响应结构: {list(response_data.keys())}")
                        return {
                            "success": False,
                            "error": "No data field in response"
                        }
                        
                except json.JSONDecodeError as e:
                    print(f"❌ JSON解析失败: {e}")
                    print(f"📋 原始响应: {response.text[:200]}...")
                    return {
                        "success": False,
                        "error": f"JSON decode error: {e}"
                    }
            else:
                print(f"❌ 请求失败: {response.status_code}")
                print(f"📋 响应内容: {response.text[:200]}...")
                
                # 分析常见错误
                if response.status_code == 406:
                    print("🔍 406错误分析:")
                    print("   可能原因:")
                    print("   1. X-s参数生成错误")
                    print("   2. Cookie过期或无效")
                    print("   3. 请求头缺失")
                    print("   4. 参数格式错误")
                    print("   5. 服务器端风控")
                elif response.status_code == 403:
                    print("🔍 403错误分析:")
                    print("   可能原因:")
                    print("   1. IP被封禁")
                    print("   2. 账号被限制")
                    print("   3. 请求频率过高")
                elif response.status_code == 401:
                    print("🔍 401错误分析:")
                    print("   可能原因:")
                    print("   1. 认证失败")
                    print("   2. Cookie无效")
                    print("   3. 会话过期")
                
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}",
                    "status_code": response.status_code,
                    "response_text": response.text[:500]
                }
                
        except requests.exceptions.RequestException as e:
            print(f"❌ 请求异常: {e}")
            return {
                "success": False,
                "error": f"Request exception: {e}"
            }
        except Exception as e:
            print(f"❌ 其他异常: {e}")
            return {
                "success": False,
                "error": f"Unexpected error: {e}"
            }
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🎯 小红书子评论API测试")
        print("=" * 60)
        
        results = []
        
        for i, test_case in enumerate(self.test_cases, 1):
            print(f"\n📋 测试 {i}/{len(self.test_cases)}")
            result = self.test_sub_comment_api(test_case)
            results.append({
                "test_case": test_case["name"],
                "result": result
            })
        
        # 汇总结果
        print("\n" + "=" * 60)
        print("📊 测试结果汇总")
        print("=" * 60)
        
        success_count = 0
        for i, result in enumerate(results, 1):
            test_name = result["test_case"]
            test_result = result["result"]
            
            if test_result["success"]:
                status = "✅ 成功"
                success_count += 1
                details = f"获取 {test_result['comment_count']} 条评论"
            else:
                status = "❌ 失败"
                details = test_result.get("error", "未知错误")
            
            print(f"{i}. {test_name}: {status}")
            print(f"   详情: {details}")
        
        print(f"\n📈 成功率: {success_count}/{len(results)} ({success_count/len(results)*100:.1f}%)")
        
        if success_count > 0:
            print("\n🎉 子评论API测试成功！")
            print("✅ 逆向工程算法有效")
            print("✅ 子评论数据获取正常")
        else:
            print("\n⚠️ 子评论API测试失败")
            print("❌ 需要进一步调试")
            print("💡 建议:")
            print("   1. 检查Cookie是否有效")
            print("   2. 验证X-s生成算法")
            print("   3. 尝试不同的API端点")
            print("   4. 考虑使用浏览器自动化方案")
        
        return results


def main():
    """主函数"""
    tester = SubCommentTester()
    results = tester.run_all_tests()
    
    # 保存测试结果
    with open("sub_comment_test_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n📁 测试结果已保存到: sub_comment_test_results.json")


if __name__ == "__main__":
    main()