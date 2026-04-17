#!/usr/bin/env python3
"""
子评论API测试工具
使用工作的X-s生成器测试子评论API
"""

import json
import time
import base64
import hashlib
import hmac
import requests
from urllib.parse import urlencode


class SubCommentTester:
    """子评论API测试器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False
        self.session.timeout = 10
        
        # 使用最新的cookie
        self.cookie = 'gid=yj8D24fWSDv0yj8D24fK069V0yIY6AFDTDxSxyU1kTyk2428MD7AC4888W2q2Yy8fJ0KjyDJ; xsecappid=xhs-pc-web; abRequestId=f425aaf4-2614-55c8-b8d1-262c611be2ab; a1=198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479; webId=fc4fb0dccb1a480d5f17359394c861d7; webBuild=4.79.0; unread=%7B%22ub%22:%3A%2268b56bf2000000001c004134%22%2C%22ue%22%3A%2268a3fe26000000001c0126d1%22%2C%22uc%22%3A20%7D; acw_tc=0a5088b217569088917503762e8bfe73414226f403ffca1e69fe74fa1b61df; web_session=040069b3ed6ebed4fbe38d058d3a4bf7c6f823; websectiga=29098a4cf41f76ee3f8db19051aaa60c0fc7c5e305572fec762da32d457d76ae; sec_poison_id=5944d42a-39e9-444e-b237-d629133962ab; loadts=1756910531213'
        
        # 测试参数
        self.note_id = "68a048c1000000001d01838e"
        self.root_comment_id = "68a048ef000000003002a604"
        
    def generate_working_xs(self, url, user_id=""):
        """使用工作的X-s生成算法"""
        timestamp = str(int(time.time() * 1000))
        base_string = f"{timestamp}{url}"
        
        # 使用已知工作的密钥
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
    
    def test_main_comment_api(self):
        """测试主评论API确认X-s生成器工作"""
        print("🧪 测试主评论API")
        print("="*50)
        
        # 主评论API
        params = {
            'note_id': self.note_id,
            'cursor': '',
            'top_comment_id': '',
            'image_formats': 'jpg,webp,avif',
            'xsec_token': 'ABIyAXG1J9ckAl0VbljygE3I8b6TZ0k5P4jORY-kCIzzw%3D'
        }
        
        url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/page"
        full_url = url + '?' + urlencode(params)
        
        # 生成X-s
        xs_value = self.generate_working_xs(full_url)
        
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
            'X-t': str(int(time.time() * 1000)),
            'X-s': xs_value,
            'x-s-common': xs_value
        }
        
        try:
            response = self.session.get(full_url, headers=headers)
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                success = data.get('success', False)
                print(f"API成功: {success}")
                
                if success:
                    comments = data.get('data', {}).get('comments', [])
                    print(f"✅ 主评论API正常，获取到 {len(comments)} 条评论")
                    return True
                else:
                    msg = data.get('msg', 'Unknown error')
                    print(f"❌ API失败: {msg}")
            else:
                print(f"❌ 请求失败: {response.text[:100]}")
        except Exception as e:
            print(f"❌ 请求异常: {e}")
        
        return False
    
    def test_sub_comment_api(self):
        """测试子评论API"""
        print("\n🧪 测试子评论API")
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
        
        print(f"子评论URL: {full_url}")
        
        # 生成X-s
        xs_value = self.generate_working_xs(full_url)
        print(f"生成的X-s: {xs_value[:100]}...")
        print(f"X-s长度: {len(xs_value)}")
        
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
            'X-t': str(int(time.time() * 1000)),
            'X-s': xs_value,
            'x-s-common': xs_value
        }
        
        try:
            response = self.session.get(full_url, headers=headers)
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                success = data.get('success', False)
                print(f"API成功: {success}")
                
                if success:
                    comments = data.get('data', {}).get('comments', [])
                    print(f"🎉 成功获取到 {len(comments)} 条子评论!")
                    
                    # 显示前2条评论
                    for i, comment in enumerate(comments[:2], 1):
                        print(f"  {i}. {comment.get('user_info', {}).get('nickname', '')}")
                        print(f"     内容: {comment.get('content', '')[:50]}...")
                    
                    return True
                else:
                    msg = data.get('msg', 'Unknown error')
                    print(f"❌ API失败: {msg}")
                    
                    # 分析错误详情
                    if '406' in msg:
                        print("💡 406错误分析:")
                        print("  - 可能是X-s生成算法不匹配子评论API")
                        print("  - 可能需要额外的请求头参数")
                        print("  - 可能是root_comment_id参数问题")
            else:
                print(f"❌ 请求失败")
                if response.text:
                    print(f"响应: {response.text[:200]}")
        except Exception as e:
            print(f"❌ 请求异常: {e}")
        
        return False
    
    def test_alternative_approaches(self):
        """测试替代方案"""
        print("\n🔧 测试替代方案")
        print("="*50)
        
        # 方案1: 不同的参数组合
        param_variations = [
            # 原始参数
            {
                'note_id': self.note_id,
                'root_comment_id': self.root_comment_id,
                'cursor': '',
                'num': '10',
                'image_formats': 'jpg,webp,avif',
                'xsec_token': 'ABIyAXG1J9ckAl0VbljygE3I8b6TZ0k5P4jORY-kCIzzw%3D'
            },
            # 不带num参数
            {
                'note_id': self.note_id,
                'root_comment_id': self.root_comment_id,
                'cursor': '',
                'image_formats': 'jpg,webp,avif',
                'xsec_token': 'ABIyAXG1J9ckAl0VbljygE3I8b6TZ0k5P4jORY-kCIzzw%3D'
            },
            # 使用comment_id而不是root_comment_id
            {
                'note_id': self.note_id,
                'comment_id': self.root_comment_id,
                'cursor': '',
                'num': '10',
                'image_formats': 'jpg,webp,avif',
                'xsec_token': 'ABIyAXG1J9ckAl0VbljygE3I8b6TZ0k5P4jORY-kCIzzw%3D'
            }
        ]
        
        base_url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page"
        
        for i, params in enumerate(param_variations, 1):
            print(f"\n测试方案 {i}:")
            print(f"参数: {params}")
            
            full_url = base_url + '?' + urlencode(params)
            xs_value = self.generate_working_xs(full_url)
            
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
                response = self.session.get(full_url, headers=headers)
                print(f"  状态码: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    success = data.get('success', False)
                    if success:
                        comments = data.get('data', {}).get('comments', [])
                        print(f"  ✅ 方案{i}成功! 获取到 {len(comments)} 条子评论")
                        return True
                    else:
                        msg = data.get('msg', 'Unknown error')
                        print(f"  ❌ 方案{i}失败: {msg}")
                else:
                    print(f"  ❌ 方案{i}请求失败")
            except Exception as e:
                print(f"  ❌ 方案{i}异常: {e}")
        
        return False
    
    def run_tests(self):
        """运行所有测试"""
        print("🌟 子评论API测试器")
        print("="*60)
        
        # 首先测试主评论API确认X-s生成器工作
        main_success = self.test_main_comment_api()
        if not main_success:
            print("❌ 主评论API测试失败，X-s生成器可能有问题")
            return False
        
        # 测试子评论API
        sub_success = self.test_sub_comment_api()
        if sub_success:
            print("🎉 子评论API测试成功!")
            return True
        
        # 测试替代方案
        alt_success = self.test_alternative_approaches()
        if alt_success:
            print("🎉 替代方案测试成功!")
            return True
        
        print("\n❌ 所有测试都失败了")
        print("💡 建议:")
        print("  1. 检查root_comment_id是否正确")
        print("  2. 可能需要不同的X-s生成算法")
        print("  3. 可能需要额外的请求头参数")
        print("  4. 可能需要动态调试获取更多信息")
        
        return False


def main():
    """主函数"""
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    tester = SubCommentTester()
    tester.run_tests()


if __name__ == "__main__":
    main()