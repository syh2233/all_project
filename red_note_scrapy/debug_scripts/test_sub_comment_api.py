#!/usr/bin/env python3
"""
测试X-s-common生成算法并验证子评论API获取功能
"""

import json
import time
import requests
import hashlib
import base64
from urllib.parse import urlencode
from xiaohongshu_xs_common_generator import XiaohongshuXSCommonGenerator


class XiaohongshuSubCommentTester:
    """小红书子评论API测试器"""
    
    def __init__(self):
        self.xs_common_generator = XiaohongshuXSCommonGenerator()
        
        # 设置一些测试数据
        self.xs_common_generator.set_sign_random("test_random_123")
        self.xs_common_generator.set_device_fingerprint("test_device_fp", "test_suffix")
        
        # API配置
        self.base_url = "https://edith.xiaohongshu.com"
        
        # 请求头模板
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Referer": "https://www.xiaohongshu.com/",
            "Origin": "https://www.xiaohongshu.com",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "sec-ch-ua": '"Chromium";v="91", " Not A;Brand";v="99", "Google Chrome";v="91"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
        }
        
        # 测试用的Cookie（需要用户提供最新的）
        self.cookie = ""
        
    def set_cookie(self, cookie_str: str):
        """设置Cookie"""
        self.cookie = cookie_str
        self.headers["Cookie"] = cookie_str
        
    def generate_xs_header(self, url: str, data: dict = None) -> str:
        """
        生成X-s头部参数
        这里使用简化的X-s生成逻辑，实际使用时需要替换为真实的X-s生成算法
        """
        timestamp = str(int(time.time() * 1000))
        
        # 简化的X-s生成逻辑（示例）
        # 实际使用时需要替换为真实的X-s生成算法
        x_s_data = {
            "timestamp": timestamp,
            "url": url,
            "data": data or {}
        }
        
        # 使用SHA256生成X-s
        x_s_input = json.dumps(x_s_data, separators=(',', ':'), sort_keys=True)
        x_s = hashlib.sha256(x_s_input.encode()).hexdigest()[:32]
        
        return f"XYS_{x_s}"
        
    def test_sub_comment_api(self, note_id: str, root_comment_id: str, num: int = 10, cursor: str = ""):
        """
        测试子评论API获取功能
        
        Args:
            note_id: 笔记ID
            root_comment_id: 根评论ID
            num: 获取数量
            cursor: 分页游标
        """
        
        # 构建请求URL
        params = {
            "note_id": note_id,
            "root_comment_id": root_comment_id,
            "num": num,
            "cursor": cursor,
            "image_formats": "jpg,webp,avif",
            "top_comment_id": "",
            "xsec_token": "ABMARfqKuxx76hZj-CQH0D9AIHxh8oCmV_RTOxyE_DIpI="
        }
        
        url = f"{self.base_url}/api/sns/web/v2/comment/sub/page?{urlencode(params)}"
        
        print(f"🚀 测试子评论API")
        print(f"URL: {url}")
        print(f"参数: {params}")
        
        # 生成X-s-common
        xs_common = self.xs_common_generator.generate_xs_common(url)
        
        if xs_common:
            print(f"✅ 生成X-s-common: {xs_common}")
            print(f"长度: {len(xs_common)}")
            
            # 分析X-s-common结构
            analysis = self.xs_common_generator.analyze_xs_common(xs_common)
            if analysis["success"]:
                print("📋 X-s-common参数分析:")
                for key, value in analysis["analysis"].items():
                    if value:
                        print(f"   {key}: {value}")
        else:
            print("❌ X-s-common生成失败")
            return False
            
        # 生成X-s
        xs = self.generate_xs_header(url, params)
        print(f"✅ 生成X-s: {xs}")
        
        # 设置请求头
        request_headers = self.headers.copy()
        request_headers["X-s"] = xs
        request_headers["X-s-common"] = xs_common
        request_headers["X-t"] = str(int(time.time() * 1000))
        
        print(f"📋 完整请求头:")
        for key, value in request_headers.items():
            if key in ["X-s", "X-s-common", "X-t"]:
                print(f"   {key}: {value}")
        
        # 发送请求
        try:
            print(f"\n🔄 发送请求...")
            response = requests.get(url, headers=request_headers, timeout=10)
            
            print(f"📡 响应状态: {response.status_code}")
            print(f"📋 响应头: {dict(response.headers)}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"✅ 请求成功!")
                    
                    # 分析响应数据
                    if "data" in data:
                        comments = data["data"].get("comments", [])
                        total_count = data["data"].get("total_count", 0)
                        
                        print(f"📊 子评论数量: {len(comments)}")
                        print(f"📊 总子评论数: {total_count}")
                        
                        if comments:
                            print(f"\n📝 前3条子评论:")
                            for i, comment in enumerate(comments[:3]):
                                print(f"   {i+1}. {comment.get('user', {}).get('nickname', 'Unknown')}: {comment.get('content', 'No content')}")
                        
                        # 检查是否有更多数据
                        has_more = data["data"].get("has_more", False)
                        cursor = data["data"].get("cursor", "")
                        
                        if has_more:
                            print(f"🔄 还有更多数据，下一页游标: {cursor}")
                        else:
                            print(f"📄 没有更多数据")
                            
                        return True
                    else:
                        print(f"❌ 响应数据格式异常: {data}")
                        return False
                        
                except json.JSONDecodeError as e:
                    print(f"❌ JSON解析失败: {e}")
                    print(f"📄 响应内容: {response.text[:500]}")
                    return False
            else:
                print(f"❌ 请求失败: {response.status_code}")
                print(f"📄 响应内容: {response.text[:500]}")
                
                # 分析失败原因
                if response.status_code == 406:
                    print(f"🔍 406错误分析:")
                    print(f"   - X-s-common可能不正确")
                    print(f"   - X-s参数可能不正确")
                    print(f"   - Cookie可能已过期")
                    print(f"   - 请求参数可能缺失")
                elif response.status_code == 401:
                    print(f"🔍 401错误分析:")
                    print(f"   - 认证失败，Cookie可能已过期")
                elif response.status_code == 403:
                    print(f"🔍 403错误分析:")
                    print(f"   - 访问被拒绝，可能被识别为爬虫")
                    
                return False
                
        except requests.RequestException as e:
            print(f"❌ 请求异常: {e}")
            return False
            
    def test_with_real_data(self):
        """使用真实数据测试"""
        # 使用之前提供的真实数据
        note_id = "68a35fc0000000001c009cd9"
        root_comment_id = "68a83b5900000000260052c3"
        cursor = "68a83ccd000000002700255f"
        
        print(f"🧪 使用真实数据测试")
        print(f"笔记ID: {note_id}")
        print(f"根评论ID: {root_comment_id}")
        print(f"游标: {cursor}")
        
        return self.test_sub_comment_api(note_id, root_comment_id, num=10, cursor=cursor)


def main():
    """主测试函数"""
    print("🔍 小红书子评论API测试器")
    print("=" * 60)
    
    tester = XiaohongshuSubCommentTester()
    
    # 使用之前提供的Cookie进行测试
    cookie = "gid=yj8D24fWSDv0yj8D24fK069V0yIY6AFDTDxSxyU1kTyk2428MD7AC4888W2q2Yy8fJ0KjyDJ; xsecappid=xhs-pc-web; abRequestId=f425aaf4-2614-55c8-b8d1-262c611be2ab; a1=198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479; webId=fc4fb0dccb1a480d5f17359394c861d7; webBuild=4.79.0; unread={%22ub%22:%2268b56bf2000000001c004134%22%2C%22ue%22:%2268a3fe26000000001c0126d1%22%2C%22uc%22:20}; web_session=040069b3ed6ebed4fbe38d058d3a4bf7c6f823; loadts=1756911545822; websectiga=10f9a40ba454a07755a08f27ef8194c53637eba4551cf9751c009d9afb564467"
    
    if cookie:
        tester.set_cookie(cookie)
        print("✅ Cookie已设置")
    else:
        print("⚠️ 未提供Cookie，将使用测试模式（可能会失败）")
        print("💡 建议提供真实的Cookie以获得准确的测试结果")
    
    print(f"\n{'='*60}")
    
    # 执行测试
    success = tester.test_with_real_data()
    
    print(f"\n{'='*60}")
    if success:
        print("🎉 测试成功！X-s-common生成算法工作正常")
        print("✅ 子评论API可以正常获取数据")
    else:
        print("❌ 测试失败！需要进一步调试")
        print("🔍 建议检查:")
        print("   - Cookie是否有效")
        print("   - X-s生成算法是否正确")
        print("   - X-s-common生成算法是否正确")
        print("   - 请求参数是否完整")


if __name__ == "__main__":
    main()