#!/usr/bin/env python3
"""
移动端API子评论爬虫
分析小红书移动端API，绕过PC端限制
"""

import json
import time
import base64
import hashlib
import hmac
import requests
from urllib.parse import urlencode
import random
import string


class MobileSubCommentCrawler:
    """移动端子评论爬虫"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False
        self.session.timeout = 10
        
        # 移动端cookie
        self.mobile_cookie = 'gid=yj8D24fWSDv0yj8D24fK069V0yIY6AFDTDxSxyU1kTyk2428MD7AC4888W2q2Yy8fJ0KjyDJ; xsecappid=xhs-pc-web; abRequestId=f425aaf4-2614-55c8-b8d1-262c611be2ab; a1=198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479; webId=fc4fb0dccb1a480d5f17359394c861d7; webBuild=4.79.0; unread={%22ub%22:%2268b56bf2000000001c004134%22%2C%22ue%22:%2268a3fe26000000001c0126d1%22%2C%22uc%22%3A20%7D; acw_tc=0a5088b217569088917503762e8bfe73414226f403ffca1e69fe74fa1b61df; web_session=040069b3ed6ebed4fbe38d058d3a4bf7c6f823; websectiga=29098a4cf41f76ee3f8db19051aaa60c0fc7c5e305572fec762da32d457d76ae; sec_poison_id=5944d42a-39e9-444e-b237-d629133962ab; loadts=1756910531213'
        
        # 测试参数
        self.note_id = "68a048c1000000001d01838e"
        self.root_comment_id = "68afc3820000000030031abb"
        
        # 移动端API端点
        self.mobile_apis = [
            "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page",  # PC端API
            "https://edith.xiaohongshu.com/api/sns/v2/comment/sub/page",      # 可能的移动端API
            "https://www.xiaohongshu.com/api/sns/v2/comment/sub/page",      # 域名变化
            "https://api.xiaohongshu.com/sns/v2/comment/sub/page",           # 纯API域名
            "https://edith.xiaohongshu.com/api/sns/mobile/v2/comment/sub/page",  # 明确移动端
        ]
        
        # 移动端User-Agent
        self.mobile_user_agents = [
            "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 11; SM-G991U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 13_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Mobile/15E148 Safari/604.1",
        ]
    
    def generate_mobile_xs(self, url, device_type="mobile"):
        """生成移动端X-s"""
        timestamp = str(int(time.time() * 1000))
        
        # 尝试不同的移动端签名方法
        signature_methods = [
            # 方法1: 标准HMAC-SHA256
            lambda: hmac.new(b"xhs-secret", f"{timestamp}{url}".encode(), hashlib.sha256).hexdigest(),
            # 方法2: 包含设备类型
            lambda: hmac.new(b"xhs-secret", f"{timestamp}{url}{device_type}".encode(), hashlib.sha256).hexdigest(),
            # 方法3: 移动端特定密钥
            lambda: hmac.new(b"xhs-mobile-secret", f"{timestamp}{url}".encode(), hashlib.sha256).hexdigest(),
            # 方法4: 不同的URL格式
            lambda: hmac.new(b"xhs-secret", f"{url}{timestamp}".encode(), hashlib.sha256).hexdigest(),
            # 方法5: 包含note_id
            lambda: hmac.new(b"xhs-secret", f"{timestamp}{url}{self.note_id}".encode(), hashlib.sha256).hexdigest(),
        ]
        
        results = []
        for i, method in enumerate(signature_methods):
            try:
                signature = method()
                
                # 移动端可能使用不同的JSON结构
                if device_type == "mobile":
                    final_obj = {
                        "x0": timestamp,
                        "x1": "xhs-mobile-web",
                        "x2": "MOBILE",
                        "x3": signature[:32],
                        "x4": ""
                    }
                else:
                    final_obj = {
                        "x0": timestamp,
                        "x1": "xhs-pc-web",
                        "x2": "PC",
                        "x3": signature[:32],
                        "x4": ""
                    }
                
                json_str = json.dumps(final_obj, separators=(',', ':'))
                utf8_bytes = json_str.encode('utf-8')
                
                # 移动端可能使用不同的填充长度
                target_length = 241
                if len(utf8_bytes) < target_length:
                    padding = bytes([0x6a] * (target_length - len(utf8_bytes)))
                    final_bytes = utf8_bytes + padding
                else:
                    final_bytes = utf8_bytes[:target_length]
                
                base64_result = base64.b64encode(final_bytes).decode()
                xs_value = f"XYS_{base64_result}"
                results.append((f"方法{i+1}", xs_value))
                
            except Exception as e:
                print(f"方法{i+1}失败: {e}")
        
        return results
    
    def test_mobile_api(self, api_url, user_agent):
        """测试移动端API"""
        print(f"\n🧪 测试移动端API: {api_url}")
        print(f"User-Agent: {user_agent}")
        
        # 构建参数
        params = {
            'note_id': self.note_id,
            'root_comment_id': self.root_comment_id,
            'cursor': '',
            'num': '10',
            'image_formats': 'jpg,webp,avif',
            'xsec_token': 'ABIyAXG1J9ckAl0VbljygE3I8b6TZ0k5P4jORY-kCIzzw%3D'
        }
        
        full_url = api_url + '?' + urlencode(params)
        
        # 生成移动端X-s
        xs_variants = self.generate_mobile_xs(full_url, "mobile")
        
        for method_name, xs_value in xs_variants:
            print(f"\n测试 {method_name}:")
            print(f"  X-s: {xs_value[:50]}...")
            
            # 移动端请求头
            headers = {
                'accept': 'application/json, text/plain, */*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'cookie': self.mobile_cookie,
                'origin': 'https://www.xiaohongshu.com',
                'referer': 'https://www.xiaohongshu.com/',
                'user-agent': user_agent,
                'x-t': str(int(time.time() * 1000)),
                'x-b3-traceid': f'mobile_test_{method_name}',
                'x-xray-traceid': f'mobile_test_{method_name}',
                'x-s': xs_value,
                'x-s-common': xs_value
            }
            
            # 移动端可能需要不同的请求头
            if 'iPhone' in user_agent or 'Mobile' in user_agent:
                headers['sec-ch-ua'] = '"Not;A=Brand";v="99", "AppleWebKit";v="537.36", "Safari";v="537.36"'
                headers['sec-ch-ua-mobile'] = '?1'
                headers['sec-ch-ua-platform'] = '"iOS"' if 'iPhone' in user_agent else '"Android"'
            else:
                headers['sec-ch-ua'] = '"Chromium";v="91", "Google Chrome";v="91", ";Not A Brand";v="99"'
                headers['sec-ch-ua-mobile'] = '?1'
                headers['sec-ch-ua-platform'] = '"Android"'
            
            try:
                response = self.session.get(full_url, headers=headers)
                print(f"  状态码: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    success = data.get('success', False)
                    print(f"  API成功: {success}")
                    
                    if success:
                        comments = data.get('data', {}).get('comments', [])
                        print(f"  🎉 {method_name} 成功! 获取到 {len(comments)} 条子评论")
                        
                        # 显示前3条评论
                        for i, comment in enumerate(comments[:3], 1):
                            print(f"    {i}. {comment.get('user_info', {}).get('nickname', '')}")
                            print(f"       内容: {comment.get('content', '')[:50]}...")
                            print(f"       点赞: {comment.get('like_count', 0)}")
                        
                        return True
                    else:
                        msg = data.get('msg', 'Unknown error')
                        print(f"  失败原因: {msg}")
                else:
                    print(f"  响应: {response.text[:200]}")
                    
            except Exception as e:
                print(f"  请求异常: {e}")
        
        return False
    
    def test_alternative_parameters(self):
        """测试替代参数"""
        print(f"\n🔍 测试替代参数")
        print("="*40)
        
        api_url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page"
        
        # 不同的参数组合
        param_variations = [
            # 标准参数
            {
                'note_id': self.note_id,
                'root_comment_id': self.root_comment_id,
                'cursor': '',
                'num': '10',
                'image_formats': 'jpg,webp,avif',
                'xsec_token': 'ABIyAXG1J9ckAl0VbljygE3I8b6TZ0k5P4jORY-kCIzzw%3D'
            },
            # 移动端参数
            {
                'note_id': self.note_id,
                'root_comment_id': self.root_comment_id,
                'cursor': '',
                'num': '10',
                'xsec_token': 'ABIyAXG1J9ckAl0VbljygE3I8b6TZ0k5P4jORY-kCIzzw%3D'
            },
            # 简化参数
            {
                'note_id': self.note_id,
                'root_comment_id': self.root_comment_id,
                'num': '10'
            },
            # 使用comment_id
            {
                'note_id': self.note_id,
                'comment_id': self.root_comment_id,
                'num': '10'
            },
            # 添加移动端标识
            {
                'note_id': self.note_id,
                'root_comment_id': self.root_comment_id,
                'num': '10',
                'client_type': 'mobile',
                'platform': 'ios'
            }
        ]
        
        for i, params in enumerate(param_variations, 1):
            print(f"\n测试参数组合 {i}:")
            print(f"  参数: {params}")
            
            full_url = api_url + '?' + urlencode(params)
            xs_value = self.generate_mobile_xs(full_url, "mobile")[0][1]
            
            headers = {
                'accept': 'application/json, text/plain, */*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'cookie': self.mobile_cookie,
                'origin': 'https://www.xiaohongshu.com',
                'referer': 'https://www.xiaohongshu.com/',
                'user-agent': self.mobile_user_agents[0],
                'x-t': str(int(time.time() * 1000)),
                'x-b3-traceid': f'param_test_{i}',
                'x-xray-traceid': f'param_test_{i}',
                'x-s': xs_value,
                'x-s-common': xs_value
            }
            
            try:
                response = self.session.get(full_url, headers=headers)
                print(f"  状态码: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    success = data.get('success', False)
                    if success:
                        comments = data.get('data', {}).get('comments', [])
                        print(f"  🎉 参数组合 {i} 成功! 获取到 {len(comments)} 条子评论")
                        return True
                    else:
                        msg = data.get('msg', 'Unknown error')
                        print(f"  失败原因: {msg}")
                        
            except Exception as e:
                print(f"  请求异常: {e}")
        
        return False
    
    def test_different_methods(self):
        """测试不同的HTTP方法"""
        print(f"\n🔍 测试不同的HTTP方法")
        print("="*40)
        
        api_url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page"
        
        params = {
            'note_id': self.note_id,
            'root_comment_id': self.root_comment_id,
            'num': '10'
        }
        
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'cookie': self.mobile_cookie,
            'origin': 'https://www.xiaohongshu.com',
            'referer': 'https://www.xiaohongshu.com/',
            'user-agent': self.mobile_user_agents[0],
            'x-t': str(int(time.time() * 1000)),
            'x-b3-traceid': 'method_test',
            'x-xray-traceid': 'method_test',
        }
        
        # 生成X-s
        full_url = api_url + '?' + urlencode(params)
        xs_value = self.generate_mobile_xs(full_url, "mobile")[0][1]
        headers['x-s'] = xs_value
        headers['x-s-common'] = xs_value
        
        # 测试GET方法
        print("测试GET方法:")
        try:
            response = self.session.get(full_url, headers=headers)
            print(f"  状态码: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                success = data.get('success', False)
                if success:
                    comments = data.get('data', {}).get('comments', [])
                    print(f"  🎉 GET方法成功! 获取到 {len(comments)} 条子评论")
                    return True
        except Exception as e:
            print(f"  GET方法异常: {e}")
        
        # 测试POST方法
        print("测试POST方法:")
        try:
            response = self.session.post(api_url, data=params, headers=headers)
            print(f"  状态码: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                success = data.get('success', False)
                if success:
                    comments = data.get('data', {}).get('comments', [])
                    print(f"  🎉 POST方法成功! 获取到 {len(comments)} 条子评论")
                    return True
        except Exception as e:
            print(f"  POST方法异常: {e}")
        
        return False
    
    def run_mobile_api_test(self):
        """运行移动端API测试"""
        print("🌟 移动端子评论API测试")
        print("="*60)
        
        # 测试不同的移动端API端点
        for api_url in self.mobile_apis:
            for user_agent in self.mobile_user_agents[:2]:  # 限制测试数量
                if self.test_mobile_api(api_url, user_agent):
                    print(f"\n🎉 找到有效的移动端API!")
                    return True
        
        # 测试替代参数
        if self.test_alternative_parameters():
            print(f"\n🎉 找到有效的参数组合!")
            return True
        
        # 测试不同的HTTP方法
        if self.test_different_methods():
            print(f"\n🎉 找到有效的HTTP方法!")
            return True
        
        print(f"\n❌ 移动端API测试完成，未找到解决方案")
        print("💡 可能的原因:")
        print("  1. 移动端API与PC端API相同")
        print("  2. 移动端需要特殊的认证方式")
        print("  3. 需要特定的APP环境模拟")
        print("  4. 移动端API可能不存在或已废弃")
        
        return False


def main():
    """主函数"""
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    crawler = MobileSubCommentCrawler()
    crawler.run_mobile_api_test()


if __name__ == "__main__":
    main()