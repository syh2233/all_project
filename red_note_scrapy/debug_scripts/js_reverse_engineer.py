#!/usr/bin/env python3
"""
基于JS代码分析的X-s参数逆向工程
专注于手动分析前端JavaScript代码
"""

import requests
import json
import time
import re
import base64
import hashlib
import hmac
from urllib.parse import urlparse, parse_qs, urlencode

class JSReverseEngineer:
    """JS代码手动分析器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False
        self.session.timeout = 10
        
        # 新的cookie
        self.new_cookie = "gid=yj8D24fWSDv0yj8D24fK069V0yIY6AFDTDxSxyU1kTyk2428MD7AC4888W2q2Yy8fJ0KjyDJ; xsecappid=xhs-pc-web; abRequestId=f425aaf4-2614-55c8-b8d1-262c611be2ab; a1=198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479; webId=fc4fb0dccb1a480d5f17359394c861d7; web_session=040069b3ed6ebed4fbe30e25ad3a4b127faeca; webBuild=4.79.0; unread=%7B%22ub%22%3A%2268b56bf2000000001c004134%22%2C%22ue%22%3A%2268a3fe26000000001c0126d1%22%2C%22uc%22%3A20%7D; acw_tc=0a4a453a17569070897088137ec524bb28ede595ddc525595031d81456a33f; websectiga=2845367ec3848418062e761c09db7caf0e8b79d132ccdd1a4f8e64a11d0cac0d; sec_poison_id=b4c4d07b-3d95-4e2e-b6fc-42a65ed18bb4; loadts=1756907500892"
        
        # 测试参数
        self.note_id = "68a048c1000000001d01838e"
        self.root_comment_id = "68a048ef000000003002a604"
        
        # 从前端分析得到的JS代码片段
        self.js_code_fragments = {
            "vendor_js": "vendor-dynamic.77f9fe85.js",
            "key_functions": [
                "subComment",
                "SubComment", 
                "replyComment"
            ],
            "sign_patterns": [
                "X-s",
                "x-s-common",
                "xsec_token"
            ]
        }
        
    def analyze_real_xs_format(self):
        """分析真实X-s的格式特征"""
        print("🔍 分析真实X-s格式特征")
        print("="*60)
        
        # 真实的X-s值
        real_xs = "XYS_2UQhPsHCH0c1Pjh9HjIj2erjwjQhyoPTqBPT49pjHjIj2eHjwjQgynEDJ74AHjIj2ePjwjQTJdPIP/ZlgMrU4SmH4emPLfkj4DpCn/QEndG3JnMsJLprPepLpez9tAS+aDQbzDzwqer9+BpBLrYg20+64BRG8SQdJaTOGDEwy9IM4DzP+B+GLSr9/bYD8oprwgzN+nGItFcUz9Y7G7p82LLI4URP8AqUJrpCJdk7874Bpbcl+LRhqrSbzDSc+Mk6N7kCG9EkJ7GU+FzG/9k38rp98pYfLgkE4nHIPnMBqbcMpBWA49brHjIj2ecjwjHjKc=="
        
        print(f"真实X-s值: {real_xs}")
        print(f"长度: {len(real_xs)}")
        
        # 分析格式
        if real_xs.startswith("XYS_"):
            print("✅ 确认XYS_前缀")
            base64_part = real_xs[4:]
            print(f"Base64部分长度: {len(base64_part)}")
            
            # 尝试解码
            try:
                decoded = base64.b64decode(base64_part)
                print(f"解码后长度: {len(decoded)}")
                
                # 分析字节特征
                self._analyze_byte_patterns(decoded)
                
                # 尝试不同的解码方式
                self._try_different_decodings(decoded)
                
            except Exception as e:
                print(f"Base64解码失败: {e}")
    
    def _analyze_byte_patterns(self, decoded_bytes):
        """分析字节模式"""
        print("\n字节模式分析:")
        
        # 统计字节频率
        byte_freq = {}
        for byte in decoded_bytes:
            byte_freq[byte] = byte_freq.get(byte, 0) + 1
        
        # 显示最频繁的字节
        sorted_bytes = sorted(byte_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        print("最频繁的字节:")
        for byte, count in sorted_bytes:
            print(f"  0x{byte:02x}: {count}次 ({count/len(decoded_bytes)*100:.1f}%)")
        
        # 分析字节范围
        ranges = {
            "0x00-0x1F": 0,  # 控制字符
            "0x20-0x7E": 0,  # 可打印ASCII
            "0x7F-0xFF": 0,  # 扩展ASCII
        }
        
        for byte in decoded_bytes:
            if byte <= 0x1F:
                ranges["0x00-0x1F"] += 1
            elif byte <= 0x7E:
                ranges["0x20-0x7E"] += 1
            else:
                ranges["0x7F-0xFF"] += 1
        
        print("\n字节范围分布:")
        for range_name, count in ranges.items():
            print(f"  {range_name}: {count} ({count/len(decoded_bytes)*100:.1f}%)")
    
    def _try_different_decodings(self, decoded_bytes):
        """尝试不同的解码方式"""
        print("\n尝试不同解码方式:")
        
        # 尝试作为字符串解码
        encodings = ['utf-8', 'gbk', 'gb2312', 'latin-1', 'ascii']
        for encoding in encodings:
            try:
                text = decoded_bytes.decode(encoding)
                # 检查是否包含可读字符
                readable_chars = sum(1 for c in text if c.isprintable() and not c.isspace())
                if readable_chars > len(text) * 0.3:  # 30%以上可读字符
                    print(f"  {encoding}: {text[:100]}...")
            except:
                continue
        
        # 尝试作为数字数组解析
        print("\n尝试作为数字数组:")
        if len(decoded_bytes) % 4 == 0:
            # 尝试解析为32位整数数组
            import struct
            try:
                int_array = struct.unpack(f'{len(decoded_bytes)//4}I', decoded_bytes)
                print(f"  32位整数数组: {int_array[:10]}...")
            except:
                pass
        
        # 尝试解析为16位整数数组
        if len(decoded_bytes) % 2 == 0:
            try:
                short_array = struct.unpack(f'{len(decoded_bytes)//2}H', decoded_bytes)
                print(f"  16位整数数组: {short_array[:10]}...")
            except:
                pass
    
    def reverse_engineer_xs_algorithm(self):
        """逆向工程X-s算法"""
        print("\n🔬 逆向工程X-s算法")
        print("="*60)
        
        # 分析可能的算法组件
        timestamp = str(int(time.time() * 1000))
        url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page"
        user_id = "198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479"
        
        print("可能的算法组件:")
        print(f"  时间戳: {timestamp}")
        print(f"  URL: {url}")
        print(f"  用户ID: {user_id}")
        print(f"  笔记ID: {self.note_id}")
        print(f"  评论ID: {self.root_comment_id}")
        
        # 尝试常见的加密算法
        print("\n尝试常见加密算法:")
        
        algorithms = [
            ("MD5", lambda x: hashlib.md5(x.encode()).hexdigest()),
            ("SHA1", lambda x: hashlib.sha1(x.encode()).hexdigest()),
            ("SHA256", lambda x: hashlib.sha256(x.encode()).hexdigest()),
            ("SHA512", lambda x: hashlib.sha512(x.encode()).hexdigest()),
        ]
        
        # 不同的输入组合
        inputs = [
            url,
            f"{timestamp}{url}",
            f"{user_id}{timestamp}",
            f"{url}{user_id}{timestamp}",
            f"{timestamp}{user_id}{url}",
            f"{self.note_id}{self.root_comment_id}{timestamp}",
            f"{timestamp}{self.note_id}{self.root_comment_id}",
        ]
        
        for algo_name, algo_func in algorithms:
            print(f"\n{algo_name}算法:")
            for i, input_str in enumerate(inputs, 1):
                try:
                    result = algo_func(input_str)
                    print(f"  输入{i}: {result}")
                except:
                    pass
        
        # 尝试HMAC
        print("\n尝试HMAC算法:")
        possible_keys = [
            user_id,
            self.note_id,
            self.root_comment_id,
            "xiaohongshu",
            "xhs",
            "x-s",
        ]
        
        for key in possible_keys:
            print(f"\nHMAC密钥: {key}")
            for i, input_str in enumerate(inputs, 1):
                try:
                    result = hmac.new(key.encode(), input_str.encode(), hashlib.sha256).hexdigest()
                    print(f"  输入{i}: {result}")
                except:
                    pass
    
    def analyze_xs_structure(self):
        """分析X-s的结构"""
        print("\n🏗️ 分析X-s的结构")
        print("="*60)
        
        real_xs = "XYS_2UQhPsHCH0c1Pjh9HjIj2erjwjQhyoPTqBPT49pjHjIj2eHjwjQgynEDJ74AHjIj2ePjwjQTJdPIP/ZlgMrU4SmH4emPLfkj4DpCn/QEndG3JnMsJLprPepLpez9tAS+aDQbzDzwqer9+BpBLrYg20+64BRG8SQdJaTOGDEwy9IM4DzP+B+GLSr9/bYD8oprwgzN+nGItFcUz9Y7G7p82LLI4URP8AqUJrpCJdk7874Bpbcl+LRhqrSbzDSc+Mk6N7kCG9EkJ7GU+FzG/9k38rp98pYfLgkE4nHIPnMBqbcMpBWA49brHjIj2ecjwjHjKc=="
        
        # 分析Base64部分
        base64_part = real_xs[4:]
        
        # 尝试分段解码
        print("尝试分段解码:")
        
        # 尝试不同的分段长度
        segment_lengths = [16, 32, 64, 128]
        
        for seg_len in segment_lengths:
            if len(base64_part) >= seg_len:
                segment = base64_part[:seg_len]
                try:
                    decoded = base64.b64decode(segment)
                    print(f"  {seg_len}字节段: {decoded.hex()}")
                except:
                    print(f"  {seg_len}字节段: 解码失败")
        
        # 尝试找到重复模式
        print("\n寻找重复模式:")
        decoded = base64.b64decode(base64_part)
        
        # 查找重复的子串
        for pattern_len in range(2, 20):
            if len(decoded) >= pattern_len * 2:
                pattern = decoded[:pattern_len]
                found = True
                for i in range(pattern_len, len(decoded) - pattern_len, pattern_len):
                    if decoded[i:i+pattern_len] != pattern:
                        found = False
                        break
                if found:
                    print(f"  发现重复模式: {pattern.hex()} (长度{pattern_len})")
    
    def create_manual_xs_generator(self):
        """创建手动X-s生成器"""
        print("\n🛠️ 创建手动X-s生成器")
        print("="*60)
        
        # 基于分析的发现，尝试构建生成器
        print("基于分析的发现构建生成器:")
        
        # 真实X-s的特征
        real_xs = "XYS_2UQhPsHCH0c1Pjh9HjIj2erjwjQhyoPTqBPT49pjHjIj2eHjwjQgynEDJ74AHjIj2ePjwjQTJdPIP/ZlgMrU4SmH4emPLfkj4DpCn/QEndG3JnMsJLprPepLpez9tAS+aDQbzDzwqer9+BpBLrYg20+64BRG8SQdJaTOGDEwy9IM4DzP+B+GLSr9/bYD8oprwgzN+nGItFcUz9Y7G7p82LLI4URP8AqUJrpCJdk7874Bpbcl+LRhqrSbzDSc+Mk6N7kCG9EkJ7GU+FzG/9k38rp98pYfLgkE4nHIPnMBqbcMpBWA49brHjIj2ecjwjHjKc=="
        
        # 分析特征
        print("特征分析:")
        print("  - 前缀: XYS_")
        print("  - Base64编码")
        print("  - 长度约324字符")
        print("  - 包含特定字节模式")
        
        # 尝试模拟生成
        print("\n尝试模拟生成:")
        
        timestamp = str(int(time.time() * 1000))
        user_id = "198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479"
        
        # 创建复合输入
        composite_input = f"{timestamp}{user_id}{self.note_id}{self.root_comment_id}"
        
        # 尝试不同的加密方法
        methods = [
            ("直接SHA256", hashlib.sha256(composite_input.encode()).hexdigest()),
            ("双重SHA256", hashlib.sha256(hashlib.sha256(composite_input.encode()).hexdigest().encode()).hexdigest()),
            ("SHA512", hashlib.sha512(composite_input.encode()).hexdigest()),
            ("MD5+SHA256", hashlib.sha256(hashlib.md5(composite_input.encode()).hexdigest().encode()).hexdigest()),
        ]
        
        for method_name, result in methods:
            # 尝试Base64编码
            b64_result = base64.b64encode(result.encode()).decode()
            fake_xs = f"XYS_{b64_result}"
            
            print(f"  {method_name}:")
            print(f"    原始: {result[:32]}...")
            print(f"    Base64: {b64_result[:32]}...")
            print(f"    X-s: {fake_xs[:50]}...")
            
            # 测试这个生成的X-s
            if self._test_generated_xs(fake_xs):
                print(f"    ✅ 成功！")
                return method_name, fake_xs
            else:
                print(f"    ❌ 失败")
        
        return None, None
    
    def _test_generated_xs(self, xs_value):
        """测试生成的X-s值"""
        sub_url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page"
        
        # 构建参数
        params = {
            'note_id': self.note_id,
            'root_comment_id': self.root_comment_id,
            'num': '10',
            'cursor': '',
            'image_formats': 'jpg,webp,avif',
            'xsec_token': 'ABIyAXG1J9ckAl0VbljygE3I8b6TZ0k5P4jORY-kCIzzw%3D'
        }
        
        # 构建URL
        url_with_params = sub_url + '?' + urlencode(params)
        
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
            'cookie': self.new_cookie,
            'x-b3-traceid': 'js_reverse_test',
            'x-xray-traceid': 'js_reverse_test',
            'X-s': xs_value,
            'X-t': str(int(time.time() * 1000)),
            'x-s-common': xs_value
        }
        
        try:
            response = self.session.get(url_with_params, headers=headers)
            return response.status_code == 200
        except:
            return False

def main():
    """主函数"""
    print("🔬 基于JS代码的X-s参数逆向工程")
    print("拒绝自动化，坚持手动分析原则")
    print("="*60)
    
    engineer = JSReverseEngineer()
    
    # 分析真实X-s格式
    engineer.analyze_real_xs_format()
    
    # 逆向工程X-s算法
    engineer.reverse_engineer_xs_algorithm()
    
    # 分析X-s结构
    engineer.analyze_xs_structure()
    
    # 创建手动X-s生成器
    method_name, xs_value = engineer.create_manual_xs_generator()
    
    print("\n" + "="*60)
    print("📝 逆向工程总结")
    print("="*60)
    
    if method_name:
        print(f"🎉 成功逆向X-s生成算法")
        print(f"🔧 方法: {method_name}")
        print(f"🔑 生成的X-s: {xs_value}")
    else:
        print("❌ X-s生成算法仍未破解")
        print("🔍 需要更深入的分析:")
        print("  - 分析完整的JS代码文件")
        print("  - 理解加密算法的具体实现")
        print("  - 可能需要特定的密钥或盐值")
        print("  - 可能涉及复杂的参数组合")
    
    print("\n💡 逆向工程师的信念:")
    print("  - 每一个加密算法都有其规律")
    print("  - 混淆代码只是表象，逻辑才是本质")
    print("  - 给我足够的时间，我能找到每一个参数的生成方法")

if __name__ == "__main__":
    # 禁用SSL警告
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    main()