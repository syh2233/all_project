#!/usr/bin/env python3
"""
X-s生成差异分析器
分析主评论和子评论API的X-s生成差异
"""

import json
import time
import base64
import hashlib
import hmac
import requests
from urllib.parse import urlencode


class XsDifferenceAnalyzer:
    """X-s生成差异分析器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False
        self.session.timeout = 10
        
        # 使用最新的cookie
        self.cookie = 'gid=yj8D24fWSDv0yj8D24fK069V0yIY6AFDTDxSxyU1kTyk2428MD7AC4888W2q2Yy8fJ0KjyDJ; xsecappid=xhs-pc-web; abRequestId=f425aaf4-2614-55c8-b8d1-262c611be2ab; a1=198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479; webId=fc4fb0dccb1a480d5f17359394c861d7; webBuild=4.79.0; unread=%7B%22ub%22:%3A%2268b56bf2000000001c004134%22%2C%22ue%22%3A%2268a3fe26000000001c0126d1%22%2C%22uc%22%3A20%7D; acw_tc=0a5088b217569088917503762e8bfe73414226f403ffca1e69fe74fa1b61df; web_session=040069b3ed6ebed4fbe38d058d3a4bf7c6f823; websectiga=29098a4cf41f76ee3f8db19051aaa60c0fc7c5e305572fec762da32d457d76ae; sec_poison_id=5944d42a-39e9-444e-b237-d629133962ab; loadts=1756910531213'
        
        # 测试参数
        self.note_id = "68a048c1000000001d01838e"
        self.root_comment_id = "68a048ef000000003002a604"
        
        # 真实X-s值用于分析
        self.real_main_xs = "XYS_2UQhPsHCH0c1Pjh9HjIj2erjwjQhyoPTqBPT49pjHjIj2eHjwjQgynEDJ74AHjIj2ePjwjQTJdPIP/ZlgMrU4SmH4b4k8/4sGd4NcDRwnB4j/dWUnfkyyUT+ankcpB864BV32dmFL0ZIafc68/8MpBhA2Dq6a7kTnni7/AqMtMYf+n8a2rR1J/YVagYoPBQIJ9MOtAbN+MYNcDRrzMYCLebs4e+bP0Ph4B8TJAzFqBMazrRs+diAL9QBpb4iar46PnT94pHIPLky8DuMp7md/FlLLBz8J9Q7/F8P4DMszbQhJflbJsV9HjIj2ecjwjHjKc=="
        
    def generate_xs_variations(self, url, algorithm_type="main"):
        """生成多种X-s变体"""
        variations = []
        timestamp = str(int(time.time() * 1000))
        
        # 基础HMAC-SHA256
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
        xs1 = f"XYS_{base64_result}"
        variations.append(("基础HMAC-SHA256", xs1))
        
        # 变体1: 包含note_id
        base_string2 = f"{timestamp}{url}{self.note_id}"
        signature2 = hmac.new(b"xhs-secret", base_string2.encode(), hashlib.sha256).hexdigest()
        
        final_obj2 = {
            "x0": timestamp,
            "x1": "xhs-pc-web",
            "x2": "PC",
            "x3": signature2[:32],
            "x4": self.note_id
        }
        
        json_str2 = json.dumps(final_obj2, separators=(',', ':'))
        utf8_bytes2 = json_str2.encode('utf-8')
        
        if len(utf8_bytes2) < target_length:
            padding2 = bytes([0x68] * (target_length - len(utf8_bytes2)))
            final_bytes2 = utf8_bytes2 + padding2
        else:
            final_bytes2 = utf8_bytes2[:target_length]
        
        base64_result2 = base64.b64encode(final_bytes2).decode()
        xs2 = f"XYS_{base64_result2}"
        variations.append(("包含note_id", xs2))
        
        # 变体2: 包含root_comment_id (仅用于子评论)
        if algorithm_type == "sub":
            base_string3 = f"{timestamp}{url}{self.root_comment_id}"
            signature3 = hmac.new(b"xhs-secret", base_string3.encode(), hashlib.sha256).hexdigest()
            
            final_obj3 = {
                "x0": timestamp,
                "x1": "xhs-pc-web",
                "x2": "PC",
                "x3": signature3[:32],
                "x4": self.root_comment_id
            }
            
            json_str3 = json.dumps(final_obj3, separators=(',', ':'))
            utf8_bytes3 = json_str3.encode('utf-8')
            
            if len(utf8_bytes3) < target_length:
                padding3 = bytes([0x32] * (target_length - len(utf8_bytes3)))
                final_bytes3 = utf8_bytes3 + padding3
            else:
                final_bytes3 = utf8_bytes3[:target_length]
            
            base64_result3 = base64.b64encode(final_bytes3).decode()
            xs3 = f"XYS_{base64_result3}"
            variations.append(("包含root_comment_id", xs3))
        
        # 变体3: 不同的哈希算法
        hash_algorithms = [
            ("SHA256", hashlib.sha256),
            ("SHA1", hashlib.sha1),
            ("MD5", hashlib.md5),
            ("SHA512", hashlib.sha512)
        ]
        
        for algo_name, algo_func in hash_algorithms:
            try:
                base_string4 = f"{timestamp}{url}"
                signature4 = hmac.new(b"xhs-secret", base_string4.encode(), algo_func).hexdigest()
                
                final_obj4 = {
                    "x0": timestamp,
                    "x1": "xhs-pc-web",
                    "x2": "PC",
                    "x3": signature4[:32],
                    "x4": ""
                }
                
                json_str4 = json.dumps(final_obj4, separators=(',', ':'))
                utf8_bytes4 = json_str4.encode('utf-8')
                
                if len(utf8_bytes4) < target_length:
                    padding4 = bytes([ord(algo_name[i%2]) * 16 + 0x61 for i in range(target_length - len(utf8_bytes4))])
                    final_bytes4 = utf8_bytes4 + padding4
                else:
                    final_bytes4 = utf8_bytes4[:target_length]
                
                base64_result4 = base64.b64encode(final_bytes4).decode()
                xs4 = f"XYS_{base64_result4}"
                variations.append((f"{algo_name}-HMAC", xs4))
            except Exception as e:
                print(f"{algo_name} 算法失败: {e}")
        
        return variations
    
    def analyze_xs_structure(self, xs_value):
        """分析X-s结构"""
        print(f"X-s值分析:")
        print(f"  长度: {len(xs_value)}")
        print(f"  前缀: {xs_value[:4]}")
        
        if xs_value.startswith("XYS_"):
            base64_part = xs_value[4:]
            try:
                decoded = base64.b64decode(base64_part)
                print(f"  Base64解码长度: {len(decoded)}")
                
                # 尝试解析为JSON
                try:
                    json_str = decoded.decode('utf-8', errors='ignore')
                    if json_str.startswith('{') and json_str.endswith('}'):
                        json_obj = json.loads(json_str)
                        print(f"  JSON结构: {list(json_obj.keys())}")
                        for key, value in json_obj.items():
                            print(f"    {key}: {value}")
                except:
                    print("  不是有效的JSON结构")
                
                # 显示原始字节的前50个
                print(f"  原始字节前50: {decoded[:50]}")
                
            except Exception as e:
                print(f"  Base64解码失败: {e}")
    
    def test_api_with_xs(self, url, xs_value, api_name):
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
            return response.status_code == 200, response.status_code, response.text
        except Exception as e:
            return False, 0, str(e)
    
    def analyze_differences(self):
        """分析主评论和子评论API的差异"""
        print("🔍 X-s生成差异分析器")
        print("="*60)
        
        # 构建API URLs
        main_params = {
            'note_id': self.note_id,
            'cursor': '',
            'top_comment_id': '',
            'image_formats': 'jpg,webp,avif',
            'xsec_token': 'ABIyAXG1J9ckAl0VbljygE3I8b6TZ0k5P4jORY-kCIzzw%3D'
        }
        
        sub_params = {
            'note_id': self.note_id,
            'root_comment_id': self.root_comment_id,
            'cursor': '',
            'num': '10',
            'image_formats': 'jpg,webp,avif',
            'xsec_token': 'ABIyAXG1J9ckAl0VbljygE3I8b6TZ0k5P4jORY-kCIzzw%3D'
        }
        
        main_url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/page"
        sub_url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page"
        
        main_full_url = main_url + '?' + urlencode(main_params)
        sub_full_url = sub_url + '?' + urlencode(sub_params)
        
        print("📋 API信息对比:")
        print(f"主评论URL: {main_full_url}")
        print(f"子评论URL: {sub_full_url}")
        print(f"URL长度差异: {len(sub_full_url) - len(main_full_url)}")
        
        # 分析真实X-s结构
        print(f"\n🔍 真实主评论X-s分析:")
        self.analyze_xs_structure(self.real_main_xs)
        
        # 生成主评论X-s变体
        print(f"\n🎨 主评论X-s变体:")
        main_variations = self.generate_xs_variations(main_full_url, "main")
        
        main_success = False
        for method_name, xs_value in main_variations[:3]:  # 测试前3个变体
            success, status, response = self.test_api_with_xs(main_full_url, xs_value, "主评论")
            print(f"  {method_name}: 状态码 {status}, 成功: {success}")
            if success:
                main_success = True
        
        # 生成子评论X-s变体
        print(f"\n🎨 子评论X-s变体:")
        sub_variations = self.generate_xs_variations(sub_full_url, "sub")
        
        sub_success = False
        for method_name, xs_value in sub_variations[:3]:  # 测试前3个变体
            success, status, response = self.test_api_with_xs(sub_full_url, xs_value, "子评论")
            print(f"  {method_name}: 状态码 {status}, 成功: {success}")
            if success:
                sub_success = True
        
        # 分析差异
        print(f"\n📊 分析结果:")
        print(f"主评论API: {'✅ 工作正常' if main_success else '❌ 有问题'}")
        print(f"子评论API: {'✅ 工作正常' if sub_success else '❌ 406错误'}")
        
        if main_success and not sub_success:
            print("\n💡 子评论API 406错误分析:")
            print("  1. X-s生成算法可能需要针对子评论API调整")
            print("  2. 可能需要额外的请求头参数")
            print("  3. 可能需要不同的密钥或哈希算法")
            print("  4. 可能需要包含root_comment_id在签名中")
        
        return main_success, sub_success
    
    def test_specific_theories(self):
        """测试特定的理论"""
        print(f"\n🧪 测试特定理论:")
        print("="*40)
        
        # 理论1: 子评论API需要不同的x4参数
        sub_params = {
            'note_id': self.note_id,
            'root_comment_id': self.root_comment_id,
            'cursor': '',
            'num': '10',
            'image_formats': 'jpg,webp,avif',
            'xsec_token': 'ABIyAXG1J9ckAl0VbljygE3I8b6TZ0k5P4jORY-kCIzzw%3D'
        }
        
        sub_url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page"
        sub_full_url = sub_url + '?' + urlencode(sub_params)
        
        timestamp = str(int(time.time() * 1000))
        
        # 测试不同的x4参数
        x4_variations = [
            ("", "空字符串"),
            (self.note_id, "note_id"),
            (self.root_comment_id, "root_comment_id"),
            ("sub_comment", "固定字符串"),
            ("68a048c1000000001d01838e_68a048ef000000003002a604", "组合ID")
        ]
        
        for x4_value, description in x4_variations:
            base_string = f"{timestamp}{sub_full_url}"
            signature = hmac.new(b"xhs-secret", base_string.encode(), hashlib.sha256).hexdigest()
            
            final_obj = {
                "x0": timestamp,
                "x1": "xhs-pc-web",
                "x2": "PC",
                "x3": signature[:32],
                "x4": x4_value
            }
            
            json_str = json.dumps(final_obj, separators=(',', ':'))
            utf8_bytes = json_str.encode('utf-8')
            
            target_length = 241
            if len(utf8_bytes) < target_length:
                padding = bytes([0x6a] * (target_length - len(utf8_bytes)))
                final_bytes = utf8_bytes + padding
            else:
                final_bytes = utf8_bytes[:target_length]
            
            base64_result = base64.b64encode(final_bytes).decode()
            xs_value = f"XYS_{base64_result}"
            
            success, status, response = self.test_api_with_xs(sub_full_url, xs_value, f"子评论-x4={description}")
            print(f"  x4={description}: 状态码 {status}, 成功: {success}")
            
            if success:
                print(f"  🎉 找到有效的x4参数: {x4_value}")
                return True
        
        return False


def main():
    """主函数"""
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    analyzer = XsDifferenceAnalyzer()
    
    # 分析差异
    main_success, sub_success = analyzer.analyze_differences()
    
    # 测试特定理论
    if main_success and not sub_success:
        theory_success = analyzer.test_specific_theories()
        if theory_success:
            print("\n🎉 找到解决方案!")
        else:
            print("\n❌ 需要进一步分析")


if __name__ == "__main__":
    main()