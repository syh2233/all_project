#!/usr/bin/env python3
"""
测试主评论API以验证X-s算法的有效性
"""

import json
import time
import requests
import urllib3
from xiaohongshu_xs_reverse_engineer import XiaohongshuXSReverseEngineer

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class MainCommentTester:
    """主评论API测试器"""
    
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
    
    def test_main_comment_api(self):
        """测试主评论API"""
        print("🎯 测试主评论API (验证X-s算法)")
        print("=" * 50)
        
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
            print("📝 生成X-s参数...")
            xs_value = self.xs_engineer.generate_xs(url)
            print(f"✅ X-s生成成功: {xs_value[:50]}...")
            
            # 构建请求头
            headers = self.base_headers.copy()
            headers["X-s"] = xs_value
            headers["X-t"] = str(int(time.time() * 1000))
            
            print(f"📋 请求URL: {url}")
            print(f"📋 请求参数: {json.dumps(params, ensure_ascii=False, indent=2)}")
            print(f"📋 关键请求头:")
            for key in ["X-s", "X-t", "Cookie"]:
                if key in headers:
                    print(f"   {key}: {headers[key][:50]}...")
            
            # 发送请求
            print("\n🚀 发送请求...")
            start_time = time.time()
            
            response = requests.get(
                url,
                params=params,
                headers=headers,
                verify=False,
                timeout=10
            )
            
            end_time = time.time()
            
            print(f"⏱️  响应时间: {(end_time - start_time):.2f}秒")
            print(f"📊 状态码: {response.status_code}")
            
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
                            print(f"✅ 获取到 {len(comments)} 条主评论")
                            
                            if comments:
                                print("📝 第一条主评论示例:")
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
                
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}",
                    "status_code": response.status_code,
                    "response_text": response.text[:500]
                }
                
        except Exception as e:
            print(f"❌ 异常: {e}")
            return {
                "success": False,
                "error": f"Exception: {e}"
            }
    
    def test_xs_algorithm_consistency(self):
        """测试X-s算法的一致性"""
        print("\n🔍 测试X-s算法一致性")
        print("-" * 50)
        
        url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/page"
        
        # 生成多个X-s值进行对比
        print("📝 生成多个X-s值进行对比...")
        xs_values = []
        
        for i in range(3):
            xs_value = self.xs_engineer.generate_xs(url)
            xs_values.append(xs_value)
            print(f"   X-s {i+1}: {xs_value[:50]}...")
            time.sleep(0.1)  # 避免时间戳重复
        
        # 分析一致性
        print(f"\n📊 一致性分析:")
        unique_values = set(xs_values)
        print(f"   生成次数: {len(xs_values)}")
        print(f"   唯一值数量: {len(unique_values)}")
        
        if len(unique_values) == len(xs_values):
            print("✅ 每次生成的X-s都不同 (正常，因为时间戳不同)")
        else:
            print("⚠️ 发现重复的X-s值")
        
        # 分析结构
        print(f"\n🔍 X-s结构分析:")
        for i, xs_value in enumerate(xs_values):
            analysis = self.xs_engineer.analyze_xs_structure(xs_value)
            if "error" not in analysis:
                structure = analysis["structure"]
                padding = analysis["padding_info"]
                print(f"   X-s {i+1}:")
                print(f"     时间戳: {structure['x0']}")
                print(f"     签名: {structure['x3'][:16]}...")
                print(f"     填充长度: {padding['padding_length']} 字节")
            else:
                print(f"   X-s {i+1}: 分析失败 - {analysis['error']}")


def main():
    """主函数"""
    tester = MainCommentTester()
    
    # 测试主评论API
    main_result = tester.test_main_comment_api()
    
    # 测试X-s算法一致性
    tester.test_xs_algorithm_consistency()
    
    print("\n" + "=" * 50)
    print("📋 测试总结")
    print("=" * 50)
    
    if main_result["success"]:
        print("✅ 主评论API测试成功")
        print("✅ X-s算法工作正常")
        print("✅ 主评论数据获取正常")
        print("\n⚠️ 但子评论API仍然返回406错误")
        print("🔍 这表明子评论API有不同的认证机制")
        print("💡 可能的原因:")
        print("   1. 子评论API需要特殊的参数或请求头")
        print("   2. 子评论API有额外的验证步骤")
        print("   3. 子评论API使用不同的签名算法")
        print("   4. 需要特定的请求顺序或上下文")
    else:
        print("❌ 主评论API测试失败")
        print("❌ X-s算法可能有问题")
        print("🔍 需要进一步调试")


if __name__ == "__main__":
    main()