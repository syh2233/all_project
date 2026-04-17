#!/usr/bin/env python3
"""
手动分析小红书cookie结构和认证机制
拒绝自动化，只相信手动分析的结果
"""

import requests
import json
import time
import uuid
from urllib.parse import urlencode

class ManualAnalysis:
    """手动分析类 - 拒绝自动化工具"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False
        self.session.timeout = 10
        
        # 新提供的cookie - 手动解析
        self.new_cookie = "gid=yj8D24fWSDv0yj8D24fK069V0yIY6AFDTDxSxyU1kTyk2428MD7AC4888W2q2Yy8fJ0KjyDJ; xsecappid=xhs-pc-web; abRequestId=f425aaf4-2614-55c8-b8d1-262c611be2ab; a1=198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479; webId=fc4fb0dccb1a480d5f17359394c861d7; web_session=040069b3ed6ebed4fbe30e25ad3a4b127faeca; webBuild=4.79.0; unread={%22ub%22:%2268b56bf2000000001c004134%22%2C%22ue%22:%2268a3fe26000000001c0126d1%22%2C%22uc%22:20}; acw_tc=0a4a453a17569070897088137ec524bb28ede595ddc525595031d81456a33f; websectiga=2845367ec3848418062e761c09db7caf0e8b79d132ccdd1a4f8e64a11d0cac0d; sec_poison_id=b4c4d07b-3d95-4e2e-b6fc-42a65ed18bb4; loadts=1756907500892"
        
        # 手动解析cookie组件
        self.cookie_parts = self._manual_parse_cookie()
        
        # 测试参数
        self.note_id = "68a048c1000000001d01838e"
        self.root_comment_id = "68a048ef000000003002a604"
        
    def _manual_parse_cookie(self):
        """手动解析cookie - 不用任何解析库"""
        print("🔍 手动解析cookie结构...")
        
        parts = {}
        components = self.new_cookie.split("; ")
        
        for component in components:
            if "=" in component:
                key, value = component.split("=", 1)
                parts[key] = value
                
                # 手动分析每个组件
                print(f"  {key}: {value[:50]}{'...' if len(value) > 50 else ''}")
                
                # 特殊处理unread参数
                if key == "unread":
                    print(f"    -> URL编码的JSON数据")
                    # 手动解码看看
                    try:
                        import urllib.parse
                        decoded = urllib.parse.unquote(value)
                        print(f"    -> 解码后: {decoded}")
                    except:
                        pass
                        
                # 分析时间戳
                if key == "loadts":
                    print(f"    -> 时间戳，对应时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(value)//1000))}")
                    
                # 分析会话ID
                if key in ["a1", "web_session", "webId"]:
                    print(f"    -> 认证相关ID")
                    
                # 分析安全相关
                if key in ["websectiga", "sec_poison_id", "acw_tc"]:
                    print(f"    -> 安全相关参数")
        
        print(f"\n📊 Cookie分析结果:")
        print(f"  总组件数: {len(parts)}")
        print(f"  认证组件: a1, web_session, webId")
        print(f"  安全组件: websectiga, sec_poison_id, acw_tc")
        print(f"  会话组件: gid, xsecappid, abRequestId")
        print(f"  配置组件: webBuild, unread, loadts")
        
        return parts
    
    def _generate_trace_id(self):
        """手动生成trace ID - 不用uuid库"""
        import random
        import string
        
        # 手动生成24位随机字符串
        chars = string.ascii_letters + string.digits
        trace_id = ''.join(random.choice(chars) for _ in range(24))
        return trace_id
    
    def _build_headers(self, url):
        """手动构建请求头 - 完全手动控制"""
        timestamp = str(int(time.time() * 1000))
        
        # 基础请求头 - 手动设置
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,en-GB;q=0.6',
            'origin': 'https://www.xiaohongshu.com',
            'priority': 'u=1, i',
            'referer': 'https://www.xiaohongshu.com/',
            'sec-ch-ua': '"Not;A=Brand";v="99", "Microsoft Edge";v="139", "Chromium";v="139"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0',
        }
        
        # 手动构建cookie - 使用新的cookie但更新loadts
        cookie_components = self.new_cookie.split("; ")
        updated_components = []
        
        for component in cookie_components:
            if component.startswith("loadts="):
                updated_components.append(f"loadts={timestamp}")
            else:
                updated_components.append(component)
        
        headers['cookie'] = "; ".join(updated_components)
        
        # 手动设置trace ID
        headers['x-b3-traceid'] = self._generate_trace_id()
        headers['x-xray-traceid'] = self._generate_trace_id()
        
        # 手动设置时间戳
        headers['X-t'] = timestamp
        
        print(f"🔧 手动构建请求头完成")
        print(f"  Cookie组件数: {len(updated_components)}")
        print(f"  时间戳: {timestamp}")
        print(f"  Trace ID: {headers['x-b3-traceid']}")
        
        return headers
    
    def test_api_manually(self):
        """手动测试API - 拒绝自动化工具"""
        print("\n" + "="*60)
        print("🧪 开始手动API测试")
        print("="*60)
        
        # 先访问页面建立session
        print("\n1. 📱 手动访问页面建立session")
        page_url = f"https://www.xiaohongshu.com/explore/{self.note_id}"
        
        headers = self._build_headers(page_url)
        
        try:
            page_response = self.session.get(page_url, headers=headers)
            print(f"  页面访问状态: {page_response.status_code}")
            if page_response.status_code == 200:
                print("  ✅ Session建立成功")
            else:
                print(f"  ❌ Session建立失败: {page_response.status_code}")
        except Exception as e:
            print(f"  ❌ 页面访问错误: {e}")
        
        # 测试子评论API
        print("\n2. 🔍 手动测试子评论API")
        
        sub_url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page"
        
        # 手动构建参数 - 基于之前的分析
        params = {
            'note_id': self.note_id,
            'root_comment_id': self.root_comment_id,
            'num': '10',
            'cursor': '',
            'image_formats': 'jpg,webp,avif',
            'xsec_token': 'ABIyAXG1J9ckAl0VbljygE3I8b6TZ0k5P4jORY-kCIzzw%3D'
        }
        
        # 构建完整URL
        params = {k: v for k, v in params.items() if v}
        url_with_params = sub_url + '?' + urlencode(params)
        
        print(f"  请求URL: {url_with_params}")
        print(f"  参数列表:")
        for key, value in params.items():
            print(f"    {key}: {value}")
        
        # 构建请求头
        api_headers = self._build_headers(url_with_params)
        
        # 手动设置X-s参数 - 需要分析生成算法
        # 暂时使用时间戳作为简单的X-s
        timestamp = api_headers['X-t']
        simple_xs = f"{timestamp}.manual_analysis_test"
        api_headers['X-s'] = simple_xs
        api_headers['x-s-common'] = simple_xs  # 关键发现：两者相同
        
        print(f"  X-s参数: {simple_xs}")
        print(f"  x-s-common: {simple_xs}")
        
        # 发送请求
        print("\n3. 🚀 发送API请求")
        
        try:
            response = self.session.get(url_with_params, headers=api_headers)
            print(f"  状态码: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    success = data.get('success', False)
                    print(f"  成功标志: {success}")
                    
                    if success:
                        comments = data.get('data', {}).get('comments', [])
                        cursor = data.get('data', {}).get('cursor', '')
                        has_more = data.get('data', {}).get('has_more', False)
                        
                        print(f"  📊 子评论数量: {len(comments)}")
                        print(f"  📄 下一页游标: {cursor}")
                        print(f"  🔄 是否有更多: {has_more}")
                        
                        if comments:
                            print(f"\n  💬 前3条子评论:")
                            for i, comment in enumerate(comments[:3], 1):
                                content = comment.get('content', 'N/A')
                                user_name = comment.get('user', {}).get('nickname', 'N/A')
                                like_count = comment.get('like_count', 0)
                                print(f"    {i}. {user_name}")
                                print(f"       {content}")
                                print(f"       👍 {like_count}")
                        
                        print(f"\n  🎉 手动分析成功！获取到子评论数据")
                        return True
                        
                    else:
                        msg = data.get('msg', 'Unknown error')
                        code = data.get('code', 'Unknown')
                        print(f"  ❌ API失败: {msg}")
                        print(f"  ❌ 错误代码: {code}")
                        
                        # 分析错误原因
                        if code == -1:
                            print(f"  🔍 分析: 406错误，认证机制需要进一步研究")
                            print(f"  🔍 可能原因:")
                            print(f"    - X-s参数生成算法不正确")
                            print(f"    - 缺少特定的请求头")
                            print(f"    - 需要特定的访问序列")
                            print(f"    - 环境检测识别出非浏览器")
                        
                except json.JSONDecodeError:
                    print(f"  ❌ 响应解析失败: {response.text[:200]}")
            else:
                print(f"  ❌ 请求失败: {response.text[:200]}")
                
        except Exception as e:
            print(f"  ❌ 请求异常: {e}")
        
        return False
    
    def analyze_authentication_flow(self):
        """手动分析认证流程"""
        print("\n" + "="*60)
        print("🔐 手动分析认证流程")
        print("="*60)
        
        print("📋 认证组件分析:")
        for key, value in self.cookie_parts.items():
            print(f"\n  🔑 {key}:")
            print(f"     值: {value}")
            print(f"     长度: {len(value)}")
            
            # 分析各组件的作用
            if key == "a1":
                print(f"     作用: 用户认证令牌")
            elif key == "web_session":
                print(f"     作用: Web会话ID")
            elif key == "webId":
                print(f"     作用: 浏览器指纹ID")
            elif key == "gid":
                print(f"     作用: 访客ID")
            elif key == "websectiga":
                print(f"     作用: 安全验证参数")
            elif key == "sec_poison_id":
                print(f"     作用: 安全防护ID")
            elif key == "loadts":
                print(f"     作用: 加载时间戳")
            elif key == "unread":
                print(f"     作用: 未读消息状态")
            elif key == "webBuild":
                print(f"     作用: 前端版本号")
            elif key == "acw_tc":
                print(f"     作用: 验证码相关")
            elif key == "xsecappid":
                print(f"     作用: 安全应用ID")
            elif key == "abRequestId":
                print(f"     作用: A/B测试请求ID")
        
        print(f"\n🔍 认证流程分析:")
        print(f"  1. 用户登录 -> 获取a1令牌")
        print(f"  2. 访问页面 -> 建立web_session")
        print(f"  3. 生成设备指纹 -> webId, gid")
        print(f"  4. 安全验证 -> websectiga, sec_poison_id")
        print(f"  5. 时间戳验证 -> loadts")
        print(f"  6. 请求签名 -> X-s, x-s-common")
        
        print(f"\n🧩 缺失的组件:")
        print(f"  - X-s参数生成算法")
        print(f"  - xsec_token生成机制")
        print(f"  - 完整的请求头要求")
        print(f"  - 可能的JavaScript环境检测")

def main():
    """主函数 - 完全手动分析"""
    print("🔬 小红书子评论API - 手动逆向分析")
    print("="*60)
    print("拒绝自动化工具，坚持手动分析原则")
    print("能JS逆向就不自动化")
    print("="*60)
    
    analyzer = ManualAnalysis()
    
    # 手动分析cookie
    analyzer._manual_parse_cookie()
    
    # 手动测试API
    success = analyzer.test_api_manually()
    
    # 手动分析认证流程
    analyzer.analyze_authentication_flow()
    
    print("\n" + "="*60)
    print("📝 手动分析总结")
    print("="*60)
    
    if success:
        print("✅ 手动分析成功！子评论API可以正常工作")
        print("🎯 关键发现:")
        print("  - 正确的API路径: /api/sns/web/v2/comment/sub/page")
        print("  - 正确的参数名: root_comment_id")
        print("  - 关键认证: x-s-common = X-s")
        print("  - 新的cookie有效")
    else:
        print("❌ 手动分析遇到挑战")
        print("🔍 需要进一步研究:")
        print("  - X-s参数的生成算法")
        print("  - 可能的JavaScript环境要求")
        print("  - 更复杂的认证机制")
        print("  - 浏览器指纹检测")
    
    print("\n💡 逆向工程师的信念:")
    print("  - 混淆代码就像一本书，工具只能给你摘要")
    print("  - 自动化工具让你知其然，手动分析让你知其所以然")
    print("  - 给我点时间，我能理清每一个逻辑")

if __name__ == "__main__":
    # 禁用SSL警告
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    main()