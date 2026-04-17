#!/usr/bin/env python3
"""
基于真实X-s值的深度分析
使用userscript.html提供的调试方法
"""

import requests
import json
import time
import re
import base64
import hashlib
import hmac
from urllib.parse import urlencode

class RealXSAnalyzer:
    """基于真实X-s值的分析器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False
        self.session.timeout = 10
        
        # 新的cookie
        self.new_cookie = "gid=yj8D24fWSDv0yj8D24fK069V0yIY6AFDTDxSxyU1kTyk2428MD7AC4888W2q2Yy8fJ0KjyDJ; xsecappid=xhs-pc-web; abRequestId=f425aaf4-2614-55c8-b8d1-262c611be2ab; a1=198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479; webId=fc4fb0dccb1a480d5f17359394c861d7; web_session=040069b3ed6ebed4fbe30e25ad3a4b127faeca; webBuild=4.79.0; unread=%7B%22ub%22%3A%2268b56bf2000000001c004134%22%2C%22ue%22%3A%2268a3fe26000000001c0126d1%22%2C%22uc%22%3A20%7D; acw_tc=0a4a453a17569070897088137ec524bb28ede595ddc525595031d81456a33f; websectiga=2845367ec3848418062e761c09db7caf0e8b79d132ccdd1a4f8e64a11d0cac0d; sec_poison_id=b4c4d07b-3d95-4e2e-b6fc-42a65ed18bb4; loadts=1756907500892"
        
        # 测试参数
        self.note_id = "68a048c1000000001d01838e"
        self.root_comment_id = "68a048ef000000003002a604"
        
        # 真实的X-s值
        self.real_xs = "XYS_2UQhPsHCH0c1Pjh9HjIj2erjwjQhyoPTqBPT49pjHjIj2eHjwjQgynEDJ74AHjIj2ePjwjQTJdPIP/ZlgMrU4SmH4b4k8/4sGd4NcDRwnB4j/dWUnfkyyUT+ankcpB864BV32dmFL0ZIafc68/8MpBhA2Dq6a7kTnni7/AqMtMYf+n8a2rR1J/YVagYoPBQIJ9MOtAbN+MYNcDRrzMYCLebs4e+bP0Ph4B8TJAzFqBMazrRs+diAL9QBpb4iar46PnT94pHIPLky8DuMp7md/FlLLBz8J9Q7/F8P4DMszbQhJflbJsV9HjIj2ecjwjHjKc=="
        
        # 从userscript.html得到的调试方法
        self.debug_method = {
            "userscript": "Cookie Monitor/Debugger Hook",
            "debugger_rules": ["x-s"],
            "breakpoint_trigger": "当X-s参数被设置时触发断点"
        }
    
    def analyze_real_xs_deeply(self):
        """深度分析真实X-s值"""
        print("🔬 深度分析真实X-s值")
        print("="*60)
        
        print(f"真实X-s值: {self.real_xs}")
        print(f"长度: {len(self.real_xs)}")
        
        # 分析格式
        if self.real_xs.startswith("XYS_"):
            print("✅ 确认XYS_前缀")
            base64_part = self.real_xs[4:]
            print(f"Base64部分长度: {len(base64_part)}")
            
            # 解码Base64
            try:
                decoded = base64.b64decode(base64_part)
                print(f"解码后长度: {len(decoded)}")
                
                # 深度分析解码后的内容
                self.deep_analyze_decoded_content(decoded)
                
                # 尝试不同的解码方式
                self.try_different_decodings(decoded)
                
            except Exception as e:
                print(f"Base64解码失败: {e}")
    
    def deep_analyze_decoded_content(self, decoded_bytes):
        """深度分析解码后的内容"""
        print(f"\n🔍 深度分析解码后的内容:")
        print(f"十六进制表示: {decoded_bytes.hex()}")
        
        # 统计字节频率
        byte_freq = {}
        for byte in decoded_bytes:
            byte_freq[byte] = byte_freq.get(byte, 0) + 1
        
        print(f"\n字节频率统计 (前20个):")
        sorted_bytes = sorted(byte_freq.items(), key=lambda x: x[1], reverse=True)[:20]
        for byte, count in sorted_bytes:
            print(f"  0x{byte:02x}: {count}次 ({count/len(decoded_bytes)*100:.1f}%)")
        
        # 分析字节范围
        ranges = {
            "0x00-0x1F (控制字符)": 0,
            "0x20-0x7E (可打印ASCII)": 0,
            "0x7F-0xFF (扩展ASCII)": 0,
        }
        
        for byte in decoded_bytes:
            if byte <= 0x1F:
                ranges["0x00-0x1F (控制字符)"] += 1
            elif byte <= 0x7E:
                ranges["0x20-0x7E (可打印ASCII)"] += 1
            else:
                ranges["0x7F-0xFF (扩展ASCII)"] += 1
        
        print(f"\n字节范围分布:")
        for range_name, count in ranges.items():
            print(f"  {range_name}: {count} ({count/len(decoded_bytes)*100:.1f}%)")
        
        # 查找重复模式
        print(f"\n查找重复模式:")
        for pattern_len in range(2, 20):
            if len(decoded_bytes) >= pattern_len * 2:
                pattern = decoded_bytes[:pattern_len]
                is_repeating = True
                for i in range(pattern_len, len(decoded_bytes) - pattern_len, pattern_len):
                    if decoded_bytes[i:i+pattern_len] != pattern:
                        is_repeating = False
                        break
                if is_repeating:
                    print(f"  发现重复模式: {pattern.hex()} (长度{pattern_len})")
        
        # 查找可能的字符串
        print(f"\n尝试提取字符串:")
        self.extract_strings_from_bytes(decoded_bytes)
    
    def extract_strings_from_bytes(self, decoded_bytes):
        """从字节中提取可能的字符串"""
        # 尝试不同的编码
        encodings = ['utf-8', 'gbk', 'gb2312', 'latin-1', 'ascii']
        
        for encoding in encodings:
            try:
                text = decoded_bytes.decode(encoding, errors='ignore')
                # 清理控制字符
                cleaned_text = ''.join(c for c in text if c.isprintable() and not c.isspace())
                
                if len(cleaned_text) > 10:  # 只显示有意义的字符串
                    print(f"  {encoding}: {cleaned_text[:50]}...")
            except:
                continue
    
    def try_different_decodings(self, decoded_bytes):
        """尝试不同的解码方式"""
        print(f"\n🔄 尝试不同的解码方式:")
        
        # 尝试作为数字数组
        try:
            # 32位整数数组
            if len(decoded_bytes) % 4 == 0:
                import struct
                int_array = struct.unpack(f'{len(decoded_bytes)//4}I', decoded_bytes)
                print(f"  32位整数数组: {int_array[:10]}...")
        except:
            pass
        
        # 16位整数数组
        try:
            if len(decoded_bytes) % 2 == 0:
                import struct
                short_array = struct.unpack(f'{len(decoded_bytes)//2}H', decoded_bytes)
                print(f"  16位整数数组: {short_array[:10]}...")
        except:
            pass
        
        # 尝试作为时间戳解析
        try:
            # 查找可能的时间戳 (13位数字)
            timestamp_str = ''.join(chr(b) for b in decoded_bytes if 0x30 <= b <= 0x39)
            if len(timestamp_str) >= 13:
                timestamp = int(timestamp_str[:13])
                print(f"  可能的时间戳: {timestamp} -> {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp/1000))}")
        except:
            pass
    
    def create_userscript_guide(self):
        """创建userscript使用指南"""
        print(f"\n📖 userscript.html 使用指南")
        print("="*60)
        
        print("这是一个强大的Cookie调试工具，可以帮助我们找到X-s生成代码:")
        print()
        print("🎯 核心功能:")
        print("  - 监控JavaScript对cookie的修改")
        print("  - 在cookie符合条件时进入断点")
        print("  - 设置了debuggerRules = ['x-s']来追踪X-s参数")
        print()
        print("🔧 使用方法:")
        print("1. 在浏览器中安装这个userscript")
        print("2. 访问小红书页面")
        print("3. 当X-s参数被设置时会自动触发断点")
        print("4. 在断点处查看调用栈，找到X-s生成代码")
        print()
        print("🔍 关键代码位置:")
        print("  - 第21行: const debuggerRules = ['x-s'];")
        print("  - 第502行: testDebuggerRules函数")
        print("  - 第506行: debugger; (断点触发)")
        print()
        print("💡 调试技巧:")
        print("  - 在断点时查看调用栈")
        print("  - 检查局部变量的值")
        print("  - 找到生成X-s的具体函数")
        print("  - 分析生成算法的参数组合")
    
    def reverse_engineer_real_xs(self):
        """基于真实X-s值逆向工程"""
        print(f"\n🔬 基于真实X-s值逆向工程")
        print("="*60)
        
        # 获取当前时间戳
        timestamp = str(int(time.time() * 1000))
        
        # 已知的参数
        known_params = {
            "timestamp": timestamp,
            "url": "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page",
            "method": "GET",
            "note_id": self.note_id,
            "root_comment_id": self.root_comment_id,
            "user_id": "198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479",
            "xsecappid": "xhs-pc-web"
        }
        
        print("已知参数:")
        for key, value in known_params.items():
            print(f"  {key}: {value}")
        
        # 基于真实X-s值的特征分析可能的算法
        print(f"\n尝试逆向工程算法:")
        
        # 分析真实X-s值的Base64部分
        base64_part = self.real_xs[4:]
        decoded = base64.b64decode(base64_part)
        
        # 尝试找到生成算法
        algorithms = [
            ("简单时间戳", timestamp),
            ("时间戳+URL", f"{timestamp}{known_params['url']}"),
            ("URL+时间戳", f"{known_params['url']}{timestamp}"),
            ("用户ID+时间戳", f"{known_params['user_id']}{timestamp}"),
            ("复合参数", f"{timestamp}{known_params['user_id']}{known_params['note_id']}{known_params['root_comment_id']}"),
            ("JSON格式", json.dumps({
                "t": timestamp,
                "u": known_params['url'],
                "n": known_params['note_id'],
                "r": known_params['root_comment_id'],
                "a": known_params['xsecappid']
            })),
        ]
        
        for algo_name, input_data in algorithms:
            print(f"\n  {algo_name}:")
            
            # 尝试不同的加密方法
            if isinstance(input_data, str):
                data_bytes = input_data.encode()
            else:
                data_bytes = str(input_data).encode()
            
            encryption_methods = [
                ("MD5", hashlib.md5(data_bytes).hexdigest()),
                ("SHA1", hashlib.sha1(data_bytes).hexdigest()),
                ("SHA256", hashlib.sha256(data_bytes).hexdigest()),
                ("SHA512", hashlib.sha512(data_bytes).hexdigest()),
                ("HMAC-SHA256", hmac.new(b"xhs-secret", data_bytes, hashlib.sha256).hexdigest()),
            ]
            
            for method_name, encrypted in encryption_methods:
                # 生成X-s
                generated_xs = f"XYS_{base64.b64encode(encrypted.encode()).decode()}"
                
                # 与真实X-s比较
                if generated_xs == self.real_xs:
                    print(f"    ✅ 找到了！{method_name}")
                    print(f"    算法: {algo_name}")
                    print(f"    输入: {input_data}")
                    return algo_name, method_name, input_data
                
                # 比较长度
                if len(generated_xs) == len(self.real_xs):
                    print(f"    {method_name}: 长度匹配")
        
        return None, None, None
    
    def test_real_xs(self):
        """测试真实X-s值"""
        print(f"\n🧪 测试真实X-s值")
        print("="*60)
        
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
            'x-b3-traceid': 'real_xs_test',
            'x-xray-traceid': 'real_xs_test',
            'X-s': self.real_xs,
            'X-t': str(int(time.time() * 1000)),
            'x-s-common': self.real_xs
        }
        
        try:
            response = self.session.get(url_with_params, headers=headers)
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    success = data.get('success', False)
                    print(f"成功标志: {success}")
                    
                    if success:
                        comments = data.get('data', {}).get('comments', [])
                        print(f"🎉 真实X-s值测试成功！")
                        print(f"📊 获取到 {len(comments)} 条子评论")
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
    print("🌟 基于真实X-s值的深度分析")
    print("使用userscript.html提供的调试方法")
    print("="*60)
    
    analyzer = RealXSAnalyzer()
    
    # 深度分析真实X-s值
    analyzer.analyze_real_xs_deeply()
    
    # 创建userscript使用指南
    analyzer.create_userscript_guide()
    
    # 逆向工程真实X-s值
    algo_name, method_name, input_data = analyzer.reverse_engineer_real_xs()
    
    if algo_name:
        print(f"\n🎉 逆向工程成功！")
        print(f"算法: {algo_name}")
        print(f"方法: {method_name}")
        print(f"输入: {input_data}")
    else:
        print(f"\n❌ 逆向工程失败，需要使用userscript进行动态分析")
    
    # 测试真实X-s值
    print(f"\n🧪 测试真实X-s值...")
    success = analyzer.test_real_xs()
    
    if success:
        print(f"✅ 真实X-s值有效！")
    else:
        print(f"❌ 真实X-s值无效，可能已过期")
    
    print(f"\n💡 下一步建议:")
    print(f"  1. 使用userscript.html进行浏览器端调试")
    print(f"  2. 在断点处查看X-s生成代码")
    print(f"  3. 分析生成算法的具体实现")
    print(f"  4. 提取关键参数和加密方法")

if __name__ == "__main__":
    # 禁用SSL警告
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    main()