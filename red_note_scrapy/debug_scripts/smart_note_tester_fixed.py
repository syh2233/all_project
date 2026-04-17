#!/usr/bin/env python3
"""
使用多个可能的笔记ID进行测试
"""

import json
import time
import requests
import urllib3
from xiaohongshu_xs_reverse_engineer import XiaohongshuXSReverseEngineer

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class SmartNoteTester:
    """智能笔记测试器"""
    
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
        
        # 尝试一些可能的笔记ID格式
        self.test_note_ids = [
            "67b1a2d50000000000001c4e",  # 24位十六进制
            "67b1a2d50000000000001c4e",  # 另一个可能的格式
            "67b1a2d50000000000001c4e",  # 可能的真实ID
            "67b1a2d50000000000001c4e",  # 更多可能的格式
        ]
    
    def test_note_id(self, note_id):
        """测试单个笔记ID"""
        print(f"\n🧪 测试笔记ID: {note_id}")
        print("-" * 40)
        
        # 测试主评论API
        main_url = f"https://edith.xiaohongshu.com/api/sns/web/v2/comment/page"
        main_params = {
            "note_id": note_id,
            "cursor": "",
            "num": 5  # 减少数量以提高成功率
        }
        
        try:
            # 生成X-s参数
            xs_value = self.xs_engineer.generate_xs(main_url)
            
            # 构建请求头
            headers = self.base_headers.copy()
            headers["X-s"] = xs_value
            headers["X-t"] = str(int(time.time() * 1000))
            
            # 发送主评论请求
            print("📋 测试主评论API...")
            response = requests.get(
                main_url,
                params=main_params,
                headers=headers,
                verify=False,
                timeout=10
            )
            
            print(f"   状态码: {response.status_code}")
            
            if response.status_code == 200:
                response_data = response.json()
                
                if response_data.get("success"):
                    data = response_data.get("data", {})
                    comments = data.get("comments", [])
                    print(f"   ✅ 成功！获取到 {len(comments)} 条主评论")
                    
                    if comments:
                        # 如果有评论，尝试获取第一条评论的ID来测试子评论
                        first_comment = comments[0]
                        comment_id = first_comment.get("id")
                        
                        if comment_id:
                            print(f"   📝 第一条评论ID: {comment_id}")
                            
                            # 测试子评论API
                            return self.test_sub_comment_for_note(note_id, comment_id)
                        else:
                            print("   ⚠️ 评论没有ID字段")
                            return {"note_id": note_id, "main_success": True, "sub_tested": False}
                    else:
                        print("   ⚠️ 评论列表为空")
                        return {"note_id": note_id, "main_success": True, "sub_tested": False, "no_comments": True}
                else:
                    msg = response_data.get("msg", "未知错误")
                    print(f"   ❌ 失败: {msg}")
                    return {"note_id": note_id, "main_success": False, "error": msg}
            else:
                print(f"   ❌ HTTP错误: {response.status_code}")
                return {"note_id": note_id, "main_success": False, "http_error": response.status_code}
                
        except Exception as e:
            print(f"   ❌ 异常: {e}")
            return {"note_id": note_id, "main_success": False, "exception": str(e)}
    
    def test_sub_comment_for_note(self, note_id, comment_id):
        """测试特定笔记和评论的子评论"""
        print(f"📋 测试子评论API...")
        
        sub_url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page"
        sub_params = {
            "note_id": note_id,
            "root_comment_id": comment_id,
            "num": 5,
            "cursor": ""
        }
        
        try:
            # 生成X-s参数
            xs_value = self.xs_engineer.generate_xs(sub_url)
            xs_common = self.xs_engineer.generate_xs(sub_url)
            
            # 构建请求头
            headers = self.base_headers.copy()
            headers["X-s"] = xs_value
            headers["X-s-common"] = xs_common
            headers["X-t"] = str(int(time.time() * 1000))
            headers["Content-Type"] = "application/json;charset=UTF-8"
            
            # 发送子评论请求
            response = requests.get(
                sub_url,
                params=sub_params,
                headers=headers,
                verify=False,
                timeout=10
            )
            
            print(f"   状态码: {response.status_code}")
            
            if response.status_code == 200:
                response_data = response.json()
                
                if response_data.get("success"):
                    data = response_data.get("data", {})
                    comments = data.get("comments", [])
                    print(f"   ✅ 子评论成功！获取到 {len(comments)} 条子评论")
                    
                    if comments:
                        first_sub_comment = comments[0]
                        print(f"   📝 第一条子评论: {first_sub_comment.get('content', 'N/A')[:30]}...")
                    
                    return {
                        "note_id": note_id,
                        "comment_id": comment_id,
                        "main_success": True,
                        "sub_success": True,
                        "sub_comment_count": len(comments),
                        "has_sub_comments": len(comments) > 0
                    }
                else:
                    msg = response_data.get("msg", "未知错误")
                    print(f"   ❌ 子评论失败: {msg}")
                    
                    return {
                        "note_id": note_id,
                        "comment_id": comment_id,
                        "main_success": True,
                        "sub_success": False,
                        "sub_error": msg
                    }
            else:
                print(f"   ❌ 子评论HTTP错误: {response.status_code}")
                
                return {
                    "note_id": note_id,
                    "comment_id": comment_id,
                    "main_success": True,
                    "sub_success": False,
                    "sub_http_error": response.status_code
                }
                
        except Exception as e:
            print(f"   ❌ 子评论异常: {e}")
            return {
                "note_id": note_id,
                "comment_id": comment_id,
                "main_success": True,
                "sub_success": False,
                "sub_exception": str(e)
            }
    
    def test_with_recent_format(self):
        """使用最近可能的笔记ID格式测试"""
        print("\n🎯 使用近期格式测试")
        print("=" * 50)
        
        # 生成一些近期的笔记ID（基于当前时间戳）
        current_time = int(time.time() * 1000)
        recent_ids = []
        
        # 生成几个可能的时间戳相关的ID
        for i in range(5):
            timestamp = current_time - (i * 86400000)  # 减去i天
            hex_time = hex(timestamp)[2:]  # 去掉0x前缀
            note_id = f"{hex_time}{'0' * (24 - len(hex_time))}"[:24]  # 填充到24位
            recent_ids.append(note_id)
        
        print("📝 生成的近期笔记ID:")
        for i, note_id in enumerate(recent_ids, 1):
            print(f"   {i}. {note_id}")
        
        results = []
        
        for note_id in recent_ids:
            result = self.test_note_id(note_id)
            results.append(result)
            
            # 如果找到了有效的笔记，就停止测试
            if result.get("main_success"):
                print(f"\n✅ 找到有效笔记: {note_id}")
                break
        
        return results
    
    def run_comprehensive_test(self):
        """运行综合测试"""
        print("🚀 小红书API综合测试")
        print("=" * 60)
        
        # 首先测试近期格式
        recent_results = self.test_with_recent_format()
        
        # 如果近期格式没有找到有效笔记，尝试预定义的ID
        found_valid = any(result.get("main_success") for result in recent_results)
        
        if not found_valid:
            print(f"\n🔍 尝试预定义的笔记ID...")
            predefined_results = []
            
            for note_id in self.test_note_ids:
                result = self.test_note_id(note_id)
                predefined_results.append(result)
                
                if result.get("main_success"):
                    print(f"\n✅ 找到有效笔记: {note_id}")
                    break
            
            recent_results.extend(predefined_results)
        
        # 汇总结果
        print("\n" + "=" * 60)
        print("📊 测试结果汇总")
        print("=" * 60)
        
        main_success_count = sum(1 for r in recent_results if r.get("main_success"))
        sub_success_count = sum(1 for r in recent_results if r.get("sub_success"))
        
        print(f"📈 测试的笔记数量: {len(recent_results)}")
        print(f"✅ 主评论成功: {main_success_count}")
        print(f"✅ 子评论成功: {sub_success_count}")
        
        if main_success_count > 0:
            print("\n🎉 成功获取到主评论数据！")
            print("✅ X-s算法工作正常")
            print("✅ Cookie认证有效")
            
            if sub_success_count > 0:
                print("🎉 成功获取到子评论数据！")
                print("✅ 子评论API突破成功！")
            else:
                print("\n⚠️ 子评论API仍然存在问题")
                print("💡 可能需要进一步分析子评论的特殊要求")
        else:
            print("\n❌ 未能获取到任何评论数据")
            print("💡 可能的原因:")
            print("   1. 笔记ID格式不正确")
            print("   2. 笔记不存在或已删除")
            print("   3. API限制或风控")
        
        # 保存详细结果
        final_results = {
            "test_summary": {
                "total_tests": len(recent_results),
                "main_success": main_success_count,
                "sub_success": sub_success_count,
                "cookie_valid": main_success_count > 0
            },
            "detailed_results": recent_results
        }
        
        with open("comprehensive_api_test_results.json", "w", encoding="utf-8") as f:
            json.dump(final_results, f, ensure_ascii=False, indent=2)
        
        print(f"\n📁 详细结果已保存到: comprehensive_api_test_results.json")
        
        return final_results


def main():
    """主函数"""
    tester = SmartNoteTester()
    results = tester.run_comprehensive_test()
    
    print("\n" + "=" * 60)
    print("🎯 测试结论")
    print("=" * 60)
    
    if results["test_summary"]["main_success"] > 0:
        print("✅ 主评论API功能正常")
        print("✅ X-s逆向工程成功")
        print("✅ Cookie认证有效")
        
        if results["test_summary"]["sub_success"] > 0:
            print("✅ 子评论API功能正常")
            print("🎉 完全成功！")
        else:
            print("⚠️ 子评论API需要进一步研究")
    else:
        print("❌ 需要进一步调试")
        print("💡 建议:")
        print("   1. 检查网络连接")
        print("   2. 验证Cookie有效性")
        print("   3. 尝试真实的笔记ID")


if __name__ == "__main__":
    main()