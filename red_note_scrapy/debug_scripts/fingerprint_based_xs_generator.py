#!/usr/bin/env python3
"""
基于发现的environment.js信息创建X-s生成器
专注于xhsFingerprintV3对象的逆向工程
"""

import requests
import json
import time
import re
import base64
import hashlib
import hmac
from urllib.parse import urlencode

class FingerprintBasedXSGenerator:
    """基于指纹对象的X-s生成器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False
        self.session.timeout = 10
        
        # 新的cookie
        self.new_cookie = "gid=yj8D24fWSDv0yj8D24fK069V0yIY6AFDTDxSxyU1kTyk2428MD7AC4888W2q2Yy8fJ0KjyDJ; xsecappid=xhs-pc-web; abRequestId=f425aaf4-2614-55c8-b8d1-262c611be2ab; a1=198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479; webId=fc4fb0dccb1a480d5f17359394c861d7; web_session=040069b3ed6ebed4fbe30e25ad3a4b127faeca; webBuild=4.79.0; unread=%7B%22ub%22%3A%2268b56bf2000000001c004134%22%2C%22ue%22%3A%2268a3fe26000000001c0126d1%22%2C%22uc%22%3A20%7D; acw_tc=0a4a453a17569070897088137ec524bb28ede595ddc525595031d81456a33f; websectiga=2845367ec3848418062e761c09db7caf0e8b79d132ccdd1a4f8e64a11d0cac0d; sec_poison_id=b4c4d07b-3d95-4e2e-b6fc-42a65ed18bb4; loadts=1756907500892"
        
        # 测试参数
        self.note_id = "68a048c1000000001d01838e"
        self.root_comment_id = "68a048ef000000003002a604"
        
        # 从environment.js分析得到的指纹对象
        self.fingerprint_methods = {
            "getV18": "关键指纹生成函数",
            "getCurMiniUa": "用户代理生成",
            "runMiniUa": "Mini用户代理执行",
            "r6": "内部算法函数"
        }
    
    def extract_fingerprint_code(self):
        """从environment.js提取指纹相关代码"""
        print("🔍 从environment.js提取指纹代码")
        print("="*60)
        
        try:
            with open('环境.js', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 查找xhsFingerprintV3相关代码
            fingerprint_patterns = [
                r'xhsFingerprintV3\s*=\s*{[^}]*}',
                r'getV18\s*:\s*function[^}]*}',
                r'getCurMiniUa\s*:\s*function[^}]*}',
                r'runMiniUa\s*:\s*function[^}]*}',
                r'r6\s*:\s*function[^}]*}'
            ]
            
            print("📜 提取的指纹代码片段:")
            
            for pattern in fingerprint_patterns:
                matches = re.findall(pattern, content, re.DOTALL)
                if matches:
                    print(f"\n找到 {len(matches)} 个匹配:")
                    for i, match in enumerate(matches, 1):
                        print(f"  {i}. {match[:200]}...")
            
            # 查找其他可能的X-s生成相关代码
            xs_patterns = [
                r'XYS_',
                r'X-s\s*=',
                r'x-s-common',
                r'signature',
                r'encrypt.*function'
            ]
            
            print(f"\n🔍 X-s生成相关代码:")
            for pattern in xs_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    print(f"  {pattern}: {len(matches)} 个匹配")
                    
        except Exception as e:
            print(f"❌ 提取代码时出错: {e}")
    
    def reverse_engineer_getV18(self):
        """逆向工程getV18函数"""
        print("\n🔬 逆向工程getV18函数")
        print("="*60)
        
        print("基于分析的getV18函数特征:")
        print("  - 生成V18格式的指纹")
        print("  - 可能包含设备信息")
        print("  - 可能包含时间戳")
        print("  - 可能包含随机数")
        
        # 模拟getV18函数的输出
        timestamp = str(int(time.time() * 1000))
        user_id = "198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479"
        
        # 尝试不同的V18生成算法
        v18_algorithms = [
            ("简单时间戳", timestamp),
            ("时间戳+用户ID", f"{timestamp}{user_id}"),
            ("用户ID+时间戳", f"{user_id}{timestamp}"),
            ("哈希算法", hashlib.md5(f"{timestamp}{user_id}".encode()).hexdigest()),
            ("复合哈希", hashlib.sha256(f"{timestamp}{user_id}{self.note_id}".encode()).hexdigest()),
        ]
        
        print(f"\n尝试V18生成算法:")
        
        for algo_name, v18_value in v18_algorithms:
            print(f"\n  {algo_name}:")
            print(f"    V18值: {v18_value}")
            
            # 基于这个V18值生成X-s
            xs_value = self.generate_xs_from_v18(v18_value)
            
            if xs_value:
                print(f"    生成的X-s: {xs_value[:50]}...")
                
                # 测试
                if self.test_xs_value(xs_value):
                    print(f"    ✅ 成功！")
                    return algo_name, v18_value, xs_value
                else:
                    print(f"    ❌ 失败")
        
        return None, None, None
    
    def generate_xs_from_v18(self, v18_value):
        """基于V18值生成X-s"""
        timestamp = str(int(time.time() * 1000))
        url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page"
        
        # 构建签名字符串
        sign_components = [
            timestamp,
            url,
            self.note_id,
            self.root_comment_id,
            v18_value
        ]
        
        # 尝试不同的签名组合
        sign_strings = [
            "".join(sign_components),
            f"{timestamp}.{url}.{v18_value}",
            f"{url}.{timestamp}.{v18_value}",
            f"{v18_value}.{timestamp}.{url}",
            json.dumps({
                "t": timestamp,
                "u": url,
                "n": self.note_id,
                "r": self.root_comment_id,
                "v": v18_value
            })
        ]
        
        # 对每个签名字符串尝试不同的加密方法
        for sign_string in sign_strings:
            # 尝试不同的加密方法
            encrypted_methods = [
                hashlib.md5(sign_string.encode()).hexdigest(),
                hashlib.sha1(sign_string.encode()).hexdigest(),
                hashlib.sha256(sign_string.encode()).hexdigest(),
                hashlib.sha512(sign_string.encode()).hexdigest(),
                base64.b64encode(sign_string.encode()).decode(),
            ]
            
            for encrypted in encrypted_methods:
                # 生成X-s格式
                xs_value = f"XYS_{encrypted}"
                return xs_value
        
        return None
    
    def test_xs_value(self, xs_value):
        """测试X-s值"""
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
            'x-b3-traceid': 'fingerprint_test',
            'x-xray-traceid': 'fingerprint_test',
            'X-s': xs_value,
            'X-t': str(int(time.time() * 1000)),
            'x-s-common': xs_value
        }
        
        try:
            response = self.session.get(url_with_params, headers=headers)
            return response.status_code == 200
        except:
            return False
    
    def create_complete_xs_algorithm(self):
        """创建完整的X-s算法"""
        print("\n🛠️ 创建完整的X-s算法")
        print("="*60)
        
        # 基于真实X-s值的分析
        real_xs = "XYS_2UQhPsHCH0c1Pjh9HjIj2erjwjQhyoPTqBPT49pjHjIj2eHjwjQgynEDJ74AHjIj2ePjwjQTJdPIP/ZlgMrU4SmH4emPLfkj4DpCn/QEndG3JnMsJLprPepLpez9tAS+aDQbzDzwqer9+BpBLrYg20+64BRG8SQdJaTOGDEwy9IM4DzP+B+GLSr9/bYD8oprwgzN+nGItFcUz9Y7G7p82LLI4URP8AqUJrpCJdk7874Bpbcl+LRhqrSbzDSc+Mk6N7kCG9EkJ7GU+FzG/9k38rp98pYfLgkE4nHIPnMBqbcMpBWA49brHjIj2ecjwjHjKc=="
        
        print("分析真实X-s值:")
        print(f"  长度: {len(real_xs)}")
        print(f"  前缀: {real_xs[:4]}")
        
        # 解码Base64部分
        try:
            base64_part = real_xs[4:]
            decoded = base64.b64decode(base64_part)
            print(f"  解码后长度: {len(decoded)}")
            
            # 分析解码后的内容
            print(f"  解码后内容 (hex): {decoded.hex()[:50]}...")
            
            # 尝试找到模式
            self.analyze_decoded_pattern(decoded)
            
        except Exception as e:
            print(f"  解码失败: {e}")
        
        # 基于分析创建算法
        timestamp = str(int(time.time() * 1000))
        user_id = "198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479"
        
        print(f"\n创建算法组件:")
        print(f"  时间戳: {timestamp}")
        print(f"  用户ID: {user_id}")
        print(f"  笔记ID: {self.note_id}")
        print(f"  评论ID: {self.root_comment_id}")
        
        # 尝试模拟真实X-s的生成过程
        print(f"\n尝试模拟真实X-s生成:")
        
        # 基于字节模式创建算法
        algorithms = [
            ("时间戳+用户ID+笔记ID+评论ID", f"{timestamp}{user_id}{self.note_id}{self.root_comment_id}"),
            ("用户ID+时间戳+URL", f"{user_id}{timestamp}https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page"),
            ("复合JSON", json.dumps({
                "t": timestamp,
                "u": user_id,
                "n": self.note_id,
                "r": self.root_comment_id,
                "a": "xhs-pc-web"
            })),
            ("HMAC-SHA256", hmac.new(
                b"xhs-secret-key",
                f"{timestamp}{user_id}{self.note_id}".encode(),
                hashlib.sha256
            ).hexdigest()),
        ]
        
        for algo_name, input_data in algorithms:
            print(f"\n  {algo_name}:")
            
            # 处理输入数据
            if isinstance(input_data, str):
                data_bytes = input_data.encode()
            else:
                data_bytes = str(input_data).encode()
            
            # 尝试不同的处理方法
            processed_methods = [
                ("直接Base64", base64.b64encode(data_bytes).decode()),
                ("SHA256", hashlib.sha256(data_bytes).hexdigest()),
                ("SHA512", hashlib.sha512(data_bytes).hexdigest()),
                ("双重SHA256", hashlib.sha256(hashlib.sha256(data_bytes).hexdigest().encode()).hexdigest()),
            ]
            
            for method_name, processed_data in processed_methods:
                # 生成X-s
                xs_value = f"XYS_{processed_data}"
                
                print(f"    {method_name}: {xs_value[:50]}...")
                
                # 测试
                if self.test_xs_value(xs_value):
                    print(f"    ✅ 成功！")
                    return algo_name, method_name, xs_value
        
        return None, None, None
    
    def analyze_decoded_pattern(self, decoded_bytes):
        """分析解码后的字节模式"""
        print(f"\n分析解码后的字节模式:")
        
        # 统计字节频率
        byte_freq = {}
        for byte in decoded_bytes:
            byte_freq[byte] = byte_freq.get(byte, 0) + 1
        
        # 显示最频繁的字节
        sorted_bytes = sorted(byte_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        print(f"  最频繁的字节:")
        for byte, count in sorted_bytes:
            print(f"    0x{byte:02x}: {count}次 ({count/len(decoded_bytes)*100:.1f}%)")
        
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
        
        print(f"  字节范围分布:")
        for range_name, count in ranges.items():
            print(f"    {range_name}: {count} ({count/len(decoded_bytes)*100:.1f}%)")
        
        # 尝试找到重复模式
        print(f"  尝试找到重复模式:")
        for pattern_len in range(2, 16):
            if len(decoded_bytes) >= pattern_len * 2:
                pattern = decoded_bytes[:pattern_len]
                is_repeating = True
                for i in range(pattern_len, len(decoded_bytes) - pattern_len, pattern_len):
                    if decoded_bytes[i:i+pattern_len] != pattern:
                        is_repeating = False
                        break
                if is_repeating:
                    print(f"    发现重复模式: {pattern.hex()} (长度{pattern_len})")

def main():
    """主函数"""
    print("🌟 基于指纹对象的X-s生成器")
    print("专注于xhsFingerprintV3对象的逆向工程")
    print("="*60)
    
    generator = FingerprintBasedXSGenerator()
    
    # 提取指纹代码
    generator.extract_fingerprint_code()
    
    # 逆向工程getV18函数
    algo_name, v18_value, xs_value = generator.reverse_engineer_getV18()
    
    if not xs_value:
        # 创建完整的X-s算法
        algo_name, method_name, xs_value = generator.create_complete_xs_algorithm()
        
        if xs_value:
            print(f"\n🎉 完整算法成功!")
            print(f"算法: {algo_name}")
            print(f"方法: {method_name}")
            print(f"X-s: {xs_value}")
        else:
            print(f"\n❌ 所有算法都失败了")
            print(f"需要更深入的分析或动态调试")
    
    print(f"\n💡 关键认识:")
    print(f"  - xhsFingerprintV3.getV18()是核心函数")
    print(f"  - environment.js提供了执行环境")
    print(f"  - 需要正确的V18值才能生成有效的X-s")
    print(f"  - 可能需要浏览器环境才能正确生成")

if __name__ == "__main__":
    # 禁用SSL警告
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    main()