#!/usr/bin/env python3
"""
综合X-s生成算法测试
尝试多种方法找到有效的X-s生成方式
"""

import json
import time
import base64
import hashlib
import hmac
import requests
from urllib.parse import urlencode


class ComprehensiveXSGenerator:
    """综合X-s生成器测试"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False
        self.session.timeout = 10
        
        # 测试用的cookies
        self.cookie = 'gid=yj8D24fWSDv0yj8D24fK069V0yIY6AFDTDxSxyU1kTyk2428MD7AC4888W2q2Yy8fJ0KjyDJ; xsecappid=xhs-pc-web; abRequestId=f425aaf4-2614-55c8-b8d1-262c611be2ab; a1=198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479; webId=fc4fb0dccb1a480d5f17359394c861d7; webBuild=4.79.0; unread=%7B%22ub%22%3A%2268b56bf2000000001c004134%22%2C%22ue%22%3A%2268a3fe26000000001c0126d1%22%2C%22uc%22%3A20%7D; acw_tc=0a5088b217569088917503762e8bfe73414226f403ffca1e69fe74fa1b61df; web_session=040069b3ed6ebed4fbe38d058d3a4bf7c6f823; websectiga=29098a4cf41f76ee3f8db19051aaa60c0fc7c5e305572fec762da32d457d76ae; sec_poison_id=5944d42a-39e9-444e-b237-d629133962ab; loadts=1756910531213'
        
        # 真实的X-s值用于对比
        self.real_xs = "XYS_2UQhPsHCH0c1Pjh9HjIj2erjwjQhyoPTqBPT49pjHjIj2eHjwjQgynEDJ74AHjIj2ePjwjQTJdPIP/ZlgMrU4SmH4b4k8/4sGd4NcDRwnB4j/dWUnfkyyUT+ankcpB864BV32dmFL0ZIafc68/8MpBhA2Dq6a7kTnni7/AqMtMYf+n8a2rR1J/YVagYoPBQIJ9MOtAbN+MYNcDRrzMYCLebs4e+bP0Ph4B8TJAzFqBMazrRs+diAL9QBpb4iar46PnT94pHIPLky8DuMp7md/FlLLBz8J9Q7/F8P4DMszbQhJflbJsV9HjIj2ecjwjHjKc=="
        
        # 测试参数
        self.note_id = "68a048c1000000001d01838e"
        self.root_comment_id = "68a048ef000000003002a604"
        
    def generate_xs_method_1(self, url):
        """方法1: 基础HMAC-SHA256"""
        timestamp = str(int(time.time() * 1000))
        
        base_string = f"{timestamp}{url}"
        signature = hmac.new(b"xhs-secret", base_string.encode(), hashlib.sha256).hexdigest()
        
        final_obj = {
            "x0": timestamp,
            "x1": "xhs-pc-web",
            "x2": "PC",
            "x3": signature[:32],
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
    
    def generate_xs_method_2(self, url):
        """方法2: 双重哈希"""
        timestamp = str(int(time.time() * 1000))
        
        base_string = f"{timestamp}{url}"
        hash1 = hashlib.sha256(base_string.encode()).hexdigest()
        signature = hmac.new(b"xhs-secret", hash1.encode(), hashlib.sha256).hexdigest()
        
        final_obj = {
            "x0": timestamp,
            "x1": "xhs-pc-web",
            "x2": "PC",
            "x3": signature[:32],
            "x4": ""
        }
        
        json_str = json.dumps(final_obj, separators=(',', ':'))
        utf8_bytes = json_str.encode('utf-8')
        
        # 填充到目标长度
        target_length = 241
        if len(utf8_bytes) < target_length:
            padding = bytes([0x68] * (target_length - len(utf8_bytes)))
            final_bytes = utf8_bytes + padding
        else:
            final_bytes = utf8_bytes[:target_length]
        
        base64_result = base64.b64encode(final_bytes).decode()
        return f"XYS_{base64_result}"
    
    def generate_xs_method_3(self, url):
        """方法3: 包含用户ID"""
        timestamp = str(int(time.time() * 1000))
        user_id = "198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479"
        
        base_string = f"{timestamp}{url}{user_id}"
        signature = hmac.new(b"xhs-secret", base_string.encode(), hashlib.sha256).hexdigest()
        
        final_obj = {
            "x0": timestamp,
            "x1": "xhs-pc-web",
            "x2": "PC",
            "x3": signature[:32],
            "x4": ""
        }
        
        json_str = json.dumps(final_obj, separators=(',', ':'))
        utf8_bytes = json_str.encode('utf-8')
        
        # 填充到目标长度
        target_length = 241
        if len(utf8_bytes) < target_length:
            padding = bytes([0x32] * (target_length - len(utf8_bytes)))
            final_bytes = utf8_bytes + padding
        else:
            final_bytes = utf8_bytes[:target_length]
        
        base64_result = base64.b64encode(final_bytes).decode()
        return f"XYS_{base64_result}"
    
    def generate_xs_method_4(self, url):
        """方法4: 模拟真实X-s结构"""
        timestamp = str(int(time.time() * 1000))
        
        # 分析真实X-s的Base64部分
        base64_part = self.real_xs[4:]  # 去掉XYS_前缀
        decoded = base64.b64decode(base64_part)
        
        # 尝试提取时间戳部分并替换
        timestamp_bytes = timestamp.encode('utf-8')
        
        # 简单的方法：保留大部分真实数据，只替换时间戳相关部分
        modified_bytes = bytearray(decoded)
        
        # 在开头附近替换时间戳 (这是一个简化的尝试)
        for i in range(min(len(timestamp_bytes), len(modified_bytes) - 50)):
            modified_bytes[i + 20] = timestamp_bytes[i] if i < len(timestamp_bytes) else 0
        
        base64_result = base64.b64encode(modified_bytes).decode()
        return f"XYS_{base64_result}"
    
    def test_api(self, xs_value, method_name):
        """测试API"""
        print(f"\n🧪 测试方法: {method_name}")
        print(f"X-s: {xs_value[:50]}...")
        print(f"长度: {len(xs_value)}")
        
        # 构建请求参数
        params = {
            'note_id': self.note_id,
            'root_comment_id': self.root_comment_id,
            'num': '10',
            'cursor': '',
            'image_formats': 'jpg,webp,avif',
            'xsec_token': 'ABIyAXG1J9ckAl0VbljygE3I8b6TZ0k5P4jORY-kCIzzw%3D'
        }
        
        # 构建URL
        base_url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page"
        url_with_params = base_url + '?' + urlencode(params)
        
        # 构建请求头
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
            'x-b3-traceid': f'comprehensive_test_{method_name}',
            'x-xray-traceid': f'comprehensive_test_{method_name}',
            'X-s': xs_value,
            'X-t': str(int(time.time() * 1000)),
            'x-s-common': xs_value
        }
        
        try:
            response = self.session.get(url_with_params, headers=headers)
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    success = data.get('success', False)
                    print(f"API成功: {success}")
                    
                    if success:
                        comments = data.get('data', {}).get('comments', [])
                        print(f"🎉 成功获取到 {len(comments)} 条子评论!")
                        return True
                    else:
                        msg = data.get('msg', 'Unknown error')
                        print(f"❌ API失败: {msg}")
                except json.JSONDecodeError:
                    print(f"❌ 响应解析失败: {response.text[:200]}")
            else:
                print(f"❌ 请求失败: {response.text[:200]}")
                
        except Exception as e:
            print(f"❌ 请求异常: {e}")
        
        return False
    
    def run_comprehensive_test(self):
        """运行综合测试"""
        print("🌟 综合X-s生成算法测试")
        print("="*60)
        
        # 构建测试URL
        params = {
            'note_id': self.note_id,
            'root_comment_id': self.root_comment_id,
            'num': '10',
            'cursor': '',
            'image_formats': 'jpg,webp,avif',
            'xsec_token': 'ABIyAXG1J9ckAl0VbljygE3I8b6TZ0k5P4jORY-kCIzzw%3D'
        }
        
        base_url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page"
        test_url = base_url + '?' + urlencode(params)
        
        # 测试方法
        methods = [
            ("基础HMAC-SHA256", self.generate_xs_method_1),
            ("双重哈希", self.generate_xs_method_2),
            ("包含用户ID", self.generate_xs_method_3),
            ("模拟真实结构", self.generate_xs_method_4)
        ]
        
        success_count = 0
        for method_name, method_func in methods:
            try:
                xs_value = method_func(test_url)
                if self.test_api(xs_value, method_name):
                    success_count += 1
                    print(f"✅ {method_name} 成功!")
            except Exception as e:
                print(f"❌ {method_name} 出错: {e}")
        
        print(f"\n🎯 测试结果")
        print("="*50)
        print(f"成功方法数: {success_count}/{len(methods)}")
        
        if success_count > 0:
            print("🎉 找到有效的X-s生成方法!")
        else:
            print("❌ 所有方法都失败了")
            print("💡 建议:")
            print("  1. 需要更深入分析真实X-s的生成算法")
            print("  2. 可能需要动态调试获取更多信息")
            print("  3. 考虑其他可能的参数组合")
        
        return success_count > 0


def main():
    """主函数"""
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    generator = ComprehensiveXSGenerator()
    generator.run_comprehensive_test()


if __name__ == "__main__":
    main()