#!/usr/bin/env python3
"""
子评论API调试工具
专门解决406错误问题
"""

import json
import time
import base64
import hashlib
import hmac
import requests
from urllib.parse import urlencode


class SubCommentDebugger:
    """子评论API调试器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False
        self.session.timeout = 10
        
        # 测试用的cookies
        self.cookie = 'gid=yj8D24fWSDv0yj8D24fK069V0yIY6AFDTDxSxyU1kTyk2428MD7AC4888W2q2Yy8fJ0KjyDJ; xsecappid=xhs-pc-web; abRequestId=f425aaf4-2614-55c8-b8d1-262c611be2ab; a1=198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479; webId=fc4fb0dccb1a480d5f17359394c861d7; webBuild=4.79.0; unread=%7B%22ub%22:%3A%2268b56bf2000000001c004134%22%2C%22ue%22%3A%2268a3fe26000000001c0126d1%22%2C%22uc%22%3A20%7D; acw_tc=0a5088b217569088917503762e8bfe73414226f403ffca1e69fe74fa1b61df; web_session=040069b3ed6ebed4fbe38d058d3a4bf7c6f823; websectiga=29098a4cf41f76ee3f8db19051aaa60c0fc7c5e305572fec762da32d457d76ae; sec_poison_id=5944d42a-39e9-444e-b237-d629133962ab; loadts=1756910531213'
        
        # 测试参数
        self.note_id = "68a048c1000000001d01838e"
        self.root_comment_id = "68a048ef000000003002a604"
        
        # 真实X-s值用于分析
        self.real_xs = "XYS_2UQhPsHCH0c1Pjh9HjIj2erjwjQhyoPTqBPT49pjHjIj2eHjwjQgynEDJ74AHjIj2ePjwjQTJdPIP/ZlgMrU4SmH4b4k8/4sGd4NcDRwnB4j/dWUnfkyyUT+ankcpB864BV32dmFL0ZIafc68/8MpBhA2Dq6a7kTnni7/AqMtMYf+n8a2rR1J/YVagYoPBQIJ9MOtAbN+MYNcDRrzMYCLebs4e+bP0Ph4B8TJAzFqBMazrRs+diAL9QBpb4iar46PnT94pHIPLky8DuMp7md/FlLLBz8J9Q7/F8P4DMszbQhJflbJsV9HjIj2ecjwjHjKc=="
        
    def analyze_api_differences(self):
        """分析主评论和子评论API的差异"""
        print("🔍 分析API差异")
        print("="*50)
        
        # 主评论API
        main_params = {
            'note_id': self.note_id,
            'cursor': '',
            'top_comment_id': '',
            'image_formats': 'jpg,webp,avif',
            'xsec_token': 'ABIyAXG1J9ckAl0VbljygE3I8b6TZ0k5P4jORY-kCIzzw%3D'
        }
        
        main_url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/page"
        main_full_url = main_url + '?' + urlencode(main_params)
        
        # 子评论API
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
        
        print("主评论API:")
        print(f"  URL: {main_full_url}")
        print(f"  参数: {main_params}")
        
        print("\n子评论API:")
        print(f"  URL: {sub_full_url}")
        print(f"  参数: {sub_params}")
        
        # 分析URL长度差异
        print(f"\nURL长度对比:")
        print(f"  主评论URL长度: {len(main_full_url)}")
        print(f"  子评论URL长度: {len(sub_full_url)}")
        print(f"  长度差异: {abs(len(main_full_url) - len(sub_full_url))}")
        
        return main_full_url, sub_full_url
    
    def generate_xs_variations(self, url):
        """生成多种X-s变体"""
        print("\n🎨 生成X-s变体")
        print("="*50)
        
        variations = []
        timestamp = str(int(time.time() * 1000))
        
        # 变体1: 基础HMAC-SHA256
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
        
        # 使用latin-1编码来处理特殊字符
        try:
            base64_result = base64.b64encode(final_bytes).decode('latin-1')
        except UnicodeDecodeError:
            base64_result = base64.b64encode(final_bytes).decode('utf-8', errors='replace')
        xs1 = f"XYS_{base64_result}"
        variations.append(("基础HMAC-SHA256", xs1))
        
        # 变体2: 包含note_id
        base_string2 = f"{timestamp}{url}{self.note_id}"
        signature2 = hmac.new(b"xhs-secret", base_string2.encode(), hashlib.sha256).hexdigest()
        
        final_obj2 = {
            "x0": timestamp,
            "x1": "xhs-pc-web",
            "x2": "PC",
            "x3": signature2[:32],
            "x4": ""
        }
        
        json_str2 = json.dumps(final_obj2, separators=(',', ':'))
        utf8_bytes2 = json_str2.encode('utf-8')
        
        if len(utf8_bytes2) < target_length:
            padding2 = bytes([0x68] * (target_length - len(utf8_bytes2)))
            final_bytes2 = utf8_bytes2 + padding2
        else:
            final_bytes2 = utf8_bytes2[:target_length]
        
        try:
            base64_result2 = base64.b64encode(final_bytes2).decode('latin-1')
        except UnicodeDecodeError:
            base64_result2 = base64.b64encode(final_bytes2).decode('utf-8', errors='replace')
        xs2 = f"XYS_{base64_result2}"
        variations.append(("包含note_id", xs2))
        
        # 变体3: 包含root_comment_id
        base_string3 = f"{timestamp}{url}{self.root_comment_id}"
        signature3 = hmac.new(b"xhs-secret", base_string3.encode(), hashlib.sha256).hexdigest()
        
        final_obj3 = {
            "x0": timestamp,
            "x1": "xhs-pc-web",
            "x2": "PC",
            "x3": signature3[:32],
            "x4": ""
        }
        
        json_str3 = json.dumps(final_obj3, separators=(',', ':'))
        utf8_bytes3 = json_str3.encode('utf-8')
        
        if len(utf8_bytes3) < target_length:
            padding3 = bytes([0x32] * (target_length - len(utf8_bytes3)))
            final_bytes3 = utf8_bytes3 + padding3
        else:
            final_bytes3 = utf8_bytes3[:target_length]
        
        try:
            base64_result3 = base64.b64encode(final_bytes3).decode('latin-1')
        except UnicodeDecodeError:
            base64_result3 = base64.b64encode(final_bytes3).decode('utf-8', errors='replace')
        xs3 = f"XYS_{base64_result3}"
        variations.append(("包含root_comment_id", xs3))
        
        # 变体4: 使用真实X-s的结构但替换时间戳
        base64_part = self.real_xs[4:]
        decoded = base64.b64decode(base64_part)
        
        # 尝试替换时间戳部分
        timestamp_bytes = timestamp.encode('utf-8')
        modified_bytes = bytearray(decoded)
        
        # 简单的时间戳替换尝试
        for i in range(min(len(timestamp_bytes), 50)):
            if i + 20 < len(modified_bytes):
                modified_bytes[i + 20] = timestamp_bytes[i] if i < len(timestamp_bytes) else 48
        
        try:
            base64_result4 = base64.b64encode(modified_bytes).decode('latin-1')
        except UnicodeDecodeError:
            base64_result4 = base64.b64encode(modified_bytes).decode('utf-8', errors='replace')
        xs4 = f"XYS_{base64_result4}"
        variations.append(("修改真实X-s", xs4))
        
        # 变体5: 不同的密钥
        secret_keys = ["xhs-secret", "xhs-key-2024", "xiaohongshu-2024", "red-book-2024"]
        for key in secret_keys:
            try:
                base_string5 = f"{timestamp}{url}"
                signature5 = hmac.new(key.encode(), base_string5.encode(), hashlib.sha256).hexdigest()
                
                final_obj5 = {
                    "x0": timestamp,
                    "x1": "xhs-pc-web",
                    "x2": "PC",
                    "x3": signature5[:32],
                    "x4": ""
                }
                
                json_str5 = json.dumps(final_obj5, separators=(',', ':'))
                utf8_bytes5 = json_str5.encode('utf-8')
                
                if len(utf8_bytes5) < target_length:
                    padding5 = bytes([0x65] * (target_length - len(utf8_bytes5)))
                    final_bytes5 = utf8_bytes5 + padding5
                else:
                    final_bytes5 = utf8_bytes5[:target_length]
                
                try:
                    base64_result5 = base64.b64encode(final_bytes5).decode('latin-1')
                except UnicodeDecodeError:
                    base64_result5 = base64.b64encode(final_bytes5).decode('utf-8', errors='replace')
                xs5 = f"XYS_{base64_result5}"
                variations.append((f"密钥-{key}", xs5))
            except Exception as e:
                print(f"密钥 {key} 失败: {e}")
        
        return variations
    
    def test_api_with_variations(self, url, variations):
        """使用多种变体测试API"""
        print(f"\n🧪 测试API: {url[:80]}...")
        print("="*50)
        
        # 构建请求头模板
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
            'X-t': str(int(time.time() * 1000))
        }
        
        success_count = 0
        for method_name, xs_value in variations:
            print(f"\n测试 {method_name}:")
            print(f"  X-s: {xs_value[:50]}...")
            print(f"  长度: {len(xs_value)}")
            
            # 构建请求头，确保X-s值可以正确编码
            headers = base_headers.copy()
            try:
                # 尝试直接使用X-s值
                headers['X-s'] = xs_value
                headers['x-s-common'] = xs_value
            except UnicodeEncodeError:
                # 如果编码失败，使用替代方案
                headers['X-s'] = xs_value.encode('utf-8').decode('latin-1', errors='replace')
                headers['x-s-common'] = xs_value.encode('utf-8').decode('latin-1', errors='replace')
            
            headers['x-b3-traceid'] = f'debug_{method_name}'
            headers['x-xray-traceid'] = f'debug_{method_name}'
            
            try:
                response = self.session.get(url, headers=headers)
                print(f"  状态码: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        success = data.get('success', False)
                        print(f"  API成功: {success}")
                        
                        if success:
                            comments = data.get('data', {}).get('comments', [])
                            print(f"  🎉 成功获取到 {len(comments)} 条评论!")
                            success_count += 1
                            
                            # 显示前2条评论
                            for i, comment in enumerate(comments[:2], 1):
                                print(f"    {i}. {comment.get('user_info', {}).get('nickname', '')}")
                                print(f"       内容: {comment.get('content', '')[:50]}...")
                        else:
                            msg = data.get('msg', 'Unknown error')
                            print(f"  ❌ API失败: {msg}")
                    except json.JSONDecodeError:
                        print(f"  ❌ 响应解析失败")
                else:
                    print(f"  ❌ 请求失败")
                    if response.text:
                        print(f"  响应: {response.text[:100]}...")
                    
            except Exception as e:
                print(f"  ❌ 请求异常: {e}")
        
        print(f"\n🎯 测试结果: {success_count}/{len(variations)} 种方法成功")
        return success_count > 0
    
    def debug_sub_comment_api(self):
        """调试子评论API"""
        print("🌟 子评论API调试器")
        print("="*60)
        
        # 分析API差异
        main_url, sub_url = self.analyze_api_differences()
        
        # 生成X-s变体
        variations = self.generate_xs_variations(sub_url)
        
        # 测试子评论API
        print(f"\n🚀 开始测试子评论API")
        success = self.test_api_with_variations(sub_url, variations)
        
        if success:
            print("\n🎉 找到有效的子评论获取方法!")
        else:
            print("\n❌ 所有方法都失败了")
            print("💡 建议:")
            print("  1. 检查cookie是否有效")
            print("  2. 验证root_comment_id是否正确")
            print("  3. 尝试不同的请求头组合")
            print("  4. 可能需要动态调试获取更多信息")
        
        return success


def main():
    """主函数"""
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    debugger = SubCommentDebugger()
    debugger.debug_sub_comment_api()


if __name__ == "__main__":
    main()