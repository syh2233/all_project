#!/usr/bin/env python3
"""
X-s生成算法改进版本
基于真实X-s值的深度分析
"""

import json
import time
import base64
import hashlib
import hmac
import urllib.parse
import struct
import requests
from urllib.parse import urlencode

class ImprovedXSGenerator:
    """改进的X-s参数生成器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False
        self.session.timeout = 10
        
        # 固定参数
        self.app_id = "xhs-pc-web"
        self.device_type = "PC"
        
        # 真实X-s值用于分析
        self.real_xs = "XYS_2UQhPsHCH0c1Pjh9HjIj2erjwjQhyoPTqBPT49pjHjIj2eHjwjQgynEDJ74AHjIj2ePjwjQTJdPIP/ZlgMrU4SmH4b4k8/4sGd4NcDRwnB4j/dWUnfkyyUT+ankcpB864BV32dmFL0ZIafc68/8MpBhA2Dq6a7kTnni7/AqMtMYf+n8a2rR1J/YVagYoPBQIJ9MOtAbN+MYNcDRrzMYCLebs4e+bP0Ph4B8TJAzFqBMazrRs+diAL9QBpb4iar46PnT94pHIPLky8DuMp7md/FlLLBz8J9Q7/F8P4DMszbQhJflbJsV9HjIj2ecjwjHjKc=="
        
    def analyze_real_xs(self):
        """分析真实X-s值的结构"""
        print("🔍 分析真实X-s值结构")
        print("="*50)
        
        # 解码Base64部分
        base64_part = self.real_xs[4:]  # 去掉XYS_前缀
        decoded = base64.b64decode(base64_part)
        
        print(f"Base64部分长度: {len(base64_part)}")
        print(f"解码后长度: {len(decoded)}")
        print(f"解码后内容 (hex): {decoded.hex()[:100]}...")
        
        # 尝试不同的解码方式
        print("\n🔄 尝试不同解码方式:")
        
        # 尝试作为字符串解码
        for encoding in ['utf-8', 'latin-1', 'ascii']:
            try:
                text = decoded.decode(encoding, errors='strict')
                print(f"{encoding}: {text[:100]}...")
            except:
                continue
        
        # 尝试作为整数数组
        try:
            if len(decoded) % 4 == 0:
                int_array = struct.unpack(f'{len(decoded)//4}I', decoded)
                print(f"32位整数数组: {int_array[:10]}...")
        except:
            pass
        
        return decoded
    
    def create_pattern_based_xs(self):
        """基于模式匹配创建X-s"""
        print("\n🎨 基于模式匹配创建X-s")
        print("="*50)
        
        # 分析真实X-s的特征
        base64_part = self.real_xs[4:]
        
        # 观察到真实X-s的Base64部分有重复模式
        # 让我们尝试创建类似的结构
        
        timestamp = str(int(time.time() * 1000))
        
        # 创建一个包含重复模式的字节数组
        pattern = b'HjIj2e'  # 观察到的重复模式
        
        # 构建字节数组
        byte_array = bytearray()
        
        # 添加时间戳相关字节
        for char in timestamp:
            byte_array.extend(ord(char).to_bytes(2, 'big'))
        
        # 添加重复模式
        for i in range(30):  # 创建足够的长度
            byte_array.extend(pattern)
        
        # 添加一些随机变化
        for i in range(20):
            byte_array.extend((i * 7).to_bytes(1, 'big'))
        
        # 转换为Base64
        base64_result = base64.b64encode(byte_array).decode()
        
        # 生成X-s
        generated_xs = f"XYS_{base64_result}"
        
        print(f"模式匹配生成的X-s: {generated_xs[:50]}...")
        print(f"长度: {len(generated_xs)}")
        print(f"真实长度: {len(self.real_xs)}")
        
        return generated_xs
    
    def create_structured_xs(self):
        """创建结构化的X-s"""
        print("\n🏗️ 创建结构化X-s")
        print("="*50)
        
        timestamp = str(int(time.time() * 1000))
        
        # 创建一个复杂的结构化对象
        structured_data = {
            "t": timestamp,
            "a": self.app_id,
            "d": self.device_type,
            "s1": hashlib.sha256(timestamp.encode()).hexdigest()[:16],
            "s2": hashlib.sha512(self.app_id.encode()).hexdigest()[:16],
            "r1": int(timestamp) % 10000,
            "r2": int(time.time() * 1000) % 1000,
            "p1": "xhs",
            "p2": "pc",
            "p3": "web",
            "v1": "4.79.0",
            "v2": "1.0.0"
        }
        
        # 转换为JSON
        json_str = json.dumps(structured_data, separators=(',', ':'))
        
        # 多重编码
        # 第一次：UTF-8编码
        utf8_bytes = json_str.encode('utf-8')
        
        # 第二次：添加混淆字节
        confused_bytes = bytearray()
        for i, byte in enumerate(utf8_bytes):
            confused_bytes.append(byte)
            if i % 4 == 0:
                confused_bytes.append((i * 13) % 256)
        
        # 第三次：Base64编码
        base64_result = base64.b64encode(confused_bytes).decode()
        
        # 生成X-s
        generated_xs = f"XYS_{base64_result}"
        
        print(f"结构化生成的X-s: {generated_xs[:50]}...")
        print(f"长度: {len(generated_xs)}")
        print(f"真实长度: {len(self.real_xs)}")
        
        return generated_xs
    
    def create_hmac_based_xs(self):
        """创建基于HMAC的X-s"""
        print("\n🔐 创建基于HMAC的X-s")
        print("="*50)
        
        timestamp = str(int(time.time() * 1000))
        url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page"
        user_id = "198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479"
        
        # 创建复杂的签名数据
        sign_data = f"{timestamp}{url}{user_id}{self.app_id}"
        
        # 多重HMAC签名
        hmac1 = hmac.new(b"xhs-secret-key-1", sign_data.encode(), hashlib.sha256).hexdigest()
        hmac2 = hmac.new(b"xhs-secret-key-2", hmac1.encode(), hashlib.sha512).hexdigest()
        hmac3 = hmac.new(b"xhs-secret-key-3", hmac2.encode(), hashlib.sha256).hexdigest()
        
        # 构建复杂对象
        complex_obj = {
            "x0": timestamp,
            "x1": self.app_id,
            "x2": self.device_type,
            "x3": hmac1[:32],
            "x4": hmac2[:32],
            "x5": hmac3[:32],
            "x6": hashlib.md5(sign_data.encode()).hexdigest()[:16],
            "x7": int(timestamp) % 1000000,
            "x8": int(time.time() * 1000) % 100000
        }
        
        # 转换为JSON并进行特殊编码
        json_str = json.dumps(complex_obj, separators=(',', ':'))
        
        # 特殊编码：先UTF-8编码，然后添加填充
        utf8_bytes = json_str.encode('utf-8')
        
        # 添加填充以达到特定长度
        target_length = 240  # 基于真实解码后的长度
        current_length = len(utf8_bytes)
        
        if current_length < target_length:
            padding_length = target_length - current_length
            padding = bytes([(i * 17) % 256 for i in range(padding_length)])
            final_bytes = utf8_bytes + padding
        else:
            final_bytes = utf8_bytes[:target_length]
        
        # Base64编码
        base64_result = base64.b64encode(final_bytes).decode()
        
        # 生成X-s
        generated_xs = f"XYS_{base64_result}"
        
        print(f"HMAC生成的X-s: {generated_xs[:50]}...")
        print(f"长度: {len(generated_xs)}")
        print(f"真实长度: {len(self.real_xs)}")
        
        return generated_xs
    
    def test_all_methods(self):
        """测试所有生成方法"""
        print("🧪 测试所有X-s生成方法")
        print("="*60)
        
        # 分析真实X-s
        self.analyze_real_xs()
        
        # 测试不同方法
        methods = [
            ("模式匹配", self.create_pattern_based_xs),
            ("结构化", self.create_structured_xs),
            ("HMAC", self.create_hmac_based_xs)
        ]
        
        for method_name, method_func in methods:
            try:
                generated_xs = method_func()
                
                # 检查长度匹配
                if len(generated_xs) == len(self.real_xs):
                    print(f"✅ {method_name}: 长度匹配!")
                    
                    # 测试API
                    if self.test_api(generated_xs):
                        print(f"🎉 {method_name}: API测试成功!")
                        return generated_xs
                else:
                    print(f"❌ {method_name}: 长度不匹配")
                    
            except Exception as e:
                print(f"❌ {method_name}: 出错 - {e}")
        
        return None
    
    def test_api(self, xs_value):
        """测试API"""
        print(f"\n🌐 测试API请求 - {xs_value[:30]}...")
        
        # 测试参数
        note_id = "68a048c1000000001d01838e"
        root_comment_id = "68a048ef000000003002a604"
        
        # 构建请求参数
        params = {
            'note_id': note_id,
            'root_comment_id': root_comment_id,
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
            'cookie': 'gid=yj8D24fWSDv0yj8D24fK069V0yIY6AFDTDxSxyU1kTyk2428MD7AC4888W2q2Yy8fJ0KjyDJ; xsecappid=xhs-pc-web; abRequestId=f425aaf4-2614-55c8-b8d1-262c611be2ab; a1=198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479; webId=fc4fb0dccb1a480d5f17359394c861d7; web_session=040069b3ed6ebed4fbe30e25ad3a4b127faeca; webBuild=4.79.0; unread=%7B%22ub%22%3A%2268b56bf2000000001c004134%22%2C%22ue%22%3A%2268a3fe26000000001c0126d1%22%2C%22uc%22%3A20%7D; acw_tc=0a4a453a17569070897088137ec524bb28ede595ddc525595031d81456a33f; websectiga=2845367ec3848418062e761c09db7caf0e8b79d132ccdd1a4f8e64a11d0cac0d; sec_poison_id=b4c4d07b-3d95-4e2e-b6fc-42a65ed18bb4; loadts=1756907500892',
            'x-b3-traceid': 'improved_xs_test',
            'x-xray-traceid': 'improved_xs_test',
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

def main():
    """主函数"""
    print("🌟 改进的X-s生成算法")
    print("基于真实X-s值的深度分析")
    print("="*60)
    
    generator = ImprovedXSGenerator()
    
    # 测试所有方法
    success_xs = generator.test_all_methods()
    
    if success_xs:
        print(f"\n🎉 找到有效的X-s生成方法!")
        print(f"成功的X-s: {success_xs}")
    else:
        print(f"\n❌ 所有方法都失败了")
        print("💡 建议:")
        print("  1. 需要更深入的逆向工程")
        print("  2. 使用userscript进行动态调试")
        print("  3. 分析vendor-dynamic.js中的更多细节")

if __name__ == "__main__":
    # 禁用SSL警告
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    main()