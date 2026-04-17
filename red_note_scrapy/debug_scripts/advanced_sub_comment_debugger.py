#!/usr/bin/env python3
"""
高级子评论调试器
深入分析子评论API的认证要求
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


class AdvancedSubCommentDebugger:
    """高级子评论调试器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False
        self.session.timeout = 10
        
        # 使用最新的cookie
        self.cookie = 'gid=yj8D24fWSDv0yj8D24fK069V0yIY6AFDTDxSxyU1kTyk2428MD7AC4888W2q2Yy8fJ0KjyDJ; xsecappid=xhs-pc-web; abRequestId=f425aaf4-2614-55c8-b8d1-262c611be2ab; a1=198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479; webId=fc4fb0dccb1a480d5f17359394c861d7; webBuild=4.79.0; unread=%7B%22ub%22:%3A%2268b56bf2000000001c004134%22%2C%22ue%22%3A%2268a3fe26000000001c0126d1%22%2C%22uc%22%3A20%7D; acw_tc=0a5088b217569088917503762e8bfe73414226f403ffca1e69fe74fa1b61df; web_session=040069b3ed6ebed4fbe38d058d3a4bf7c6f823; websectiga=29098a4cf41f76ee3f8db19051aaa60c0fc7c5e305572fec762da32d457d76ae; sec_poison_id=5944d42a-39e9-444e-b237-d629133962ab; loadts=1756910531213'
        
        # 测试参数
        self.note_id = "68a048c1000000001d01838e"
        self.root_comment_id = "68a048ef000000003002a604"
        
    def generate_advanced_xs(self, url, additional_data=None):
        """生成高级X-s变体"""
        timestamp = str(int(time.time() * 1000))
        
        # 尝试不同的签名方法
        signature_methods = [
            # 方法1: 标准HMAC-SHA256
            lambda: hmac.new(b"xhs-secret", f"{timestamp}{url}".encode(), hashlib.sha256).hexdigest(),
            # 方法2: 包含时间戳的URL
            lambda: hmac.new(b"xhs-secret", f"{url}{timestamp}".encode(), hashlib.sha256).hexdigest(),
            # 方法3: 使用note_id
            lambda: hmac.new(b"xhs-secret", f"{timestamp}{url}{self.note_id}".encode(), hashlib.sha256).hexdigest(),
            # 方法4: 使用root_comment_id
            lambda: hmac.new(b"xhs-secret", f"{timestamp}{url}{self.root_comment_id}".encode(), hashlib.sha256).hexdigest(),
            # 方法5: 使用所有参数
            lambda: hmac.new(b"xhs-secret", f"{timestamp}{url}{self.note_id}{self.root_comment_id}".encode(), hashlib.sha256).hexdigest(),
        ]
        
        results = []
        for i, method in enumerate(signature_methods):
            try:
                signature = method()
                
                final_obj = {
                    "x0": timestamp,
                    "x1": "xhs-pc-web",
                    "x2": "PC",
                    "x3": signature[:32],
                    "x4": additional_data if additional_data else ""
                }
                
                json_str = json.dumps(final_obj, separators=(',', ':'))
                utf8_bytes = json_str.encode('utf-8')
                
                # 填充到目标长度
                target_length = 241
                if len(utf8_bytes) < target_length:
                    padding = bytes([0x6a + i] * (target_length - len(utf8_bytes)))
                    final_bytes = utf8_bytes + padding
                else:
                    final_bytes = utf8_bytes[:target_length]
                
                base64_result = base64.b64encode(final_bytes).decode()
                xs_value = f"XYS_{base64_result}"
                results.append((f"方法{i+1}", xs_value))
                
            except Exception as e:
                print(f"方法{i+1}失败: {e}")
        
        return results
    
    def generate_random_xs(self, url):
        """生成随机X-s用于测试"""
        timestamp = str(int(time.time() * 1000))
        
        # 生成随机签名
        random_signature = ''.join(random.choices(string.hexdigits.lower(), k=32))
        
        final_obj = {
            "x0": timestamp,
            "x1": "xhs-pc-web",
            "x2": "PC",
            "x3": random_signature,
            "x4": ""
        }
        
        json_str = json.dumps(final_obj, separators=(',', ':'))
        utf8_bytes = json_str.encode('utf-8')
        
        # 填充到目标长度
        target_length = 241
        if len(utf8_bytes) < target_length:
            padding = bytes([0x6a] * (target_length - len(utf8_bytes)))
            final_bytes = utf8_bytes + padding
        else:
            final_bytes = utf8_bytes[:target_length]
        
        base64_result = base64.b64encode(final_bytes).decode()
        return f"XYS_{base64_result}"
    
    def test_with_different_headers(self, url, xs_value):
        """测试不同的请求头组合"""
        base_headers = {
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
            'cookie': self.cookie,
            'X-t': str(int(time.time() * 1000)),
            'X-s': xs_value,
            'x-s-common': xs_value
        }
        
        # 不同的请求头变体
        header_variations = [
            ("基础", base_headers.copy()),
            ("无x-s-common", {k: v for k, v in base_headers.items() if k != 'x-s-common'}),
            ("无x-s", {k: v for k, v in base_headers.items() if k not in ['X-s', 'x-s-common']}),
            ("无X-t", {k: v for k, v in base_headers.items() if k != 'X-t'}),
            ("仅X-s", {k: v for k, v in base_headers.items() if k in ['accept', 'user-agent', 'cookie', 'X-s']}),
        ]
        
        results = []
        for name, headers in header_variations:
            try:
                response = self.session.get(url, headers=headers)
                results.append((name, response.status_code, response.text[:100] if response.text else ""))
            except Exception as e:
                results.append((name, 0, str(e)))
        
        return results
    
    def test_xs_variations(self):
        """测试X-s变体"""
        print("🧪 测试X-s变体")
        print("="*50)
        
        # 子评论API
        params = {
            'note_id': self.note_id,
            'root_comment_id': self.root_comment_id,
            'cursor': '',
            'num': '10',
            'image_formats': 'jpg,webp,avif',
            'xsec_token': 'ABIyAXG1J9ckAl0VbljygE3I8b6TZ0k5P4jORY-kCIzzw%3D'
        }
        
        url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page"
        full_url = url + '?' + urlencode(params)
        
        # 测试不同的X-s生成方法
        print("\n1. 测试标准X-s生成方法:")
        standard_xs = self.generate_advanced_xs(full_url)
        for method_name, xs_value in standard_xs:
            print(f"\n测试 {method_name}:")
            print(f"  X-s: {xs_value[:50]}...")
            
            success, status, response = self.test_api_with_xs(full_url, xs_value)
            print(f"  状态码: {status}, 成功: {success}")
            
            if success:
                print(f"  🎉 {method_name} 成功!")
                return True
        
        # 测试随机X-s
        print(f"\n2. 测试随机X-s:")
        random_xs = self.generate_random_xs(full_url)
        success, status, response = self.test_api_with_xs(full_url, random_xs)
        print(f"  状态码: {status}, 成功: {success}")
        
        # 测试不同的请求头
        print(f"\n3. 测试不同的请求头组合:")
        working_xs = standard_xs[0][1]  # 使用第一个X-s
        header_results = self.test_with_different_headers(full_url, working_xs)
        
        for name, status, response in header_results:
            print(f"  {name}: 状态码 {status}")
            if status == 200:
                print(f"  🎉 {name} 请求头组合成功!")
                return True
        
        return False
    
    def test_api_with_xs(self, url, xs_value):
        """使用特定X-s测试API"""
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
            'cookie': self.cookie,
            'X-t': str(int(time.time() * 1000)),
            'X-s': xs_value,
            'x-s-common': xs_value
        }
        
        try:
            response = self.session.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                success = data.get('success', False)
                return success, response.status_code, response.text
            else:
                return False, response.status_code, response.text
        except Exception as e:
            return False, 0, str(e)
    
    def test_parameter_variations(self):
        """测试参数变化"""
        print(f"\n4. 测试参数变化:")
        print("="*30)
        
        base_url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page"
        
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
            # 无num参数
            {
                'note_id': self.note_id,
                'root_comment_id': self.root_comment_id,
                'cursor': '',
                'image_formats': 'jpg,webp,avif',
                'xsec_token': 'ABIyAXG1J9ckAl0VbljygE3I8b6TZ0k5P4jORY-kCIzzw%3D'
            },
            # 使用comment_id
            {
                'note_id': self.note_id,
                'comment_id': self.root_comment_id,
                'cursor': '',
                'num': '10',
                'image_formats': 'jpg,webp,avif',
                'xsec_token': 'ABIyAXG1J9ckAl0VbljygE3I8b6TZ0k5P4jORY-kCIzzw%3D'
            },
            # 无image_formats
            {
                'note_id': self.note_id,
                'root_comment_id': self.root_comment_id,
                'cursor': '',
                'num': '10',
                'xsec_token': 'ABIyAXG1J9ckAl0VbljygE3I8b6TZ0k5P4jORY-kCIzzw%3D'
            },
            # 无xsec_token
            {
                'note_id': self.note_id,
                'root_comment_id': self.root_comment_id,
                'cursor': '',
                'num': '10',
                'image_formats': 'jpg,webp,avif'
            }
        ]
        
        for i, params in enumerate(param_variations, 1):
            print(f"\n测试参数组合 {i}:")
            full_url = base_url + '?' + urlencode(params)
            
            # 生成X-s
            xs_value = self.generate_advanced_xs(full_url)[0][1]
            
            success, status, response = self.test_api_with_xs(full_url, xs_value)
            print(f"  状态码: {status}, 成功: {success}")
            
            if success:
                print(f"  🎉 参数组合 {i} 成功!")
                return True
        
        return False
    
    def analyze_error_patterns(self):
        """分析错误模式"""
        print(f"\n5. 分析错误模式:")
        print("="*30)
        
        # 测试不同的root_comment_id
        test_ids = [
            self.root_comment_id,  # 正确的ID
            "68a048ef000000003002a605",  # 修改一位
            "68a048ef000000003002a600",  # 修改结尾
            "invalid_comment_id",  # 完全无效
            "",  # 空字符串
        ]
        
        base_url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page"
        
        for i, test_id in enumerate(test_ids, 1):
            print(f"\n测试root_comment_id {i}: {test_id}")
            
            params = {
                'note_id': self.note_id,
                'root_comment_id': test_id,
                'cursor': '',
                'num': '10',
                'image_formats': 'jpg,webp,avif',
                'xsec_token': 'ABIyAXG1J9ckAl0VbljygE3I8b6TZ0k5P4jORY-kCIzzw%3D'
            }
            
            full_url = base_url + '?' + urlencode(params)
            xs_value = self.generate_advanced_xs(full_url)[0][1]
            
            success, status, response = self.test_api_with_xs(full_url, xs_value)
            print(f"  状态码: {status}")
            
            # 分析错误响应
            if status == 406:
                try:
                    error_data = json.loads(response)
                    msg = error_data.get('msg', 'Unknown error')
                    print(f"  错误信息: {msg}")
                except:
                    print(f"  响应: {response[:100]}")
    
    def run_comprehensive_test(self):
        """运行综合测试"""
        print("🌟 高级子评论调试器")
        print("="*60)
        
        # 测试X-s变体
        if self.test_xs_variations():
            print("\n🎉 找到有效的X-s生成方法!")
            return True
        
        # 测试参数变化
        if self.test_parameter_variations():
            print("\n🎉 找到有效的参数组合!")
            return True
        
        # 分析错误模式
        self.analyze_error_patterns()
        
        print(f"\n❌ 综合测试完成，未找到解决方案")
        print("💡 建议:")
        print("  1. 可能需要动态调试获取更多信息")
        print("  2. 可能需要分析实际的浏览器请求")
        print("  3. 可能需要等待cookie更新")
        print("  4. 可能需要更深入分析算法差异")
        
        return False


def main():
    """主函数"""
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    debugger = AdvancedSubCommentDebugger()
    debugger.run_comprehensive_test()


if __name__ == "__main__":
    main()