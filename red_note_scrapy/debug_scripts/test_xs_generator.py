#!/usr/bin/env python3
"""
测试版本的X-s生成器
专门用于验证我们的算法
"""

import json
import time
import base64
import hashlib
import hmac
import requests
from urllib.parse import urlencode


class TestXSGenerator:
    """测试X-s生成器"""
    
    def __init__(self):
        # 固定参数
        self.app_id = "xhs-pc-web"
        self.device_type = "PC"
        # 成功的密钥
        self.secret_key = "xhs-secret"
        
        # 测试用的session
        self.session = requests.Session()
        self.session.verify = False
        self.session.timeout = 10
    
    def generate_xs(self, url, user_id=""):
        """生成X-s参数"""
        timestamp = str(int(time.time() * 1000))
        
        # 步骤1: 构建基础字符串
        base_string = f"{timestamp}{url}"
        
        # 步骤2: 应用SHA256哈希
        hash_value = hashlib.sha256(base_string.encode()).hexdigest()
        
        # 步骤3: 应用HMAC-SHA256签名
        signature = hmac.new(
            self.secret_key.encode(), 
            base_string.encode(), 
            hashlib.sha256
        ).hexdigest()
        
        # 步骤4: 构建最终对象
        final_obj = {
            "x0": timestamp,
            "x1": self.app_id,
            "x2": self.device_type,
            "x3": signature[:32],
            "x4": ""
        }
        
        # 步骤5: JSON序列化
        json_str = json.dumps(final_obj, separators=(',', ':'))
        
        # 步骤6: UTF-8编码
        utf8_bytes = json_str.encode('utf-8')
        
        # 步骤7: 添加填充以达到目标长度
        target_length = 241
        current_length = len(utf8_bytes)
        
        if current_length < target_length:
            padding_length = target_length - current_length
            padding = bytes([0x6a] * padding_length)  # 0x6a = 'j'
            final_bytes = utf8_bytes + padding
        else:
            final_bytes = utf8_bytes[:target_length]
        
        # 步骤8: Base64编码
        base64_result = base64.b64encode(final_bytes).decode()
        
        # 步骤9: 生成最终X-s
        xs_value = f"XYS_{base64_result}"
        
        return xs_value
    
    def test_sub_comment_api(self):
        """测试子评论API"""
        print("🧪 测试子评论API")
        print("="*50)
        
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
        
        # 生成X-s
        xs_value = self.generate_xs(url_with_params)
        
        print(f"生成的X-s: {xs_value[:50]}...")
        print(f"长度: {len(xs_value)}")
        
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
            'cookie': 'gid=yj8D24fWSDv0yj8D24fK069V0yIY6AFDTDxSxyU1kTyk2428MD7AC4888W2q2Yy8fJ0KjyDJ; xsecappid=xhs-pc-web; abRequestId=f425aaf4-2614-55c8-b8d1-262c611be2ab; a1=198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479; webId=fc4fb0dccb1a480d5f17359394c861d7; webBuild=4.79.0; unread=%7B%22ub%22%3A%2268b56bf2000000001c004134%22%2C%22ue%22%3A%2268a3fe26000000001c0126d1%22%2C%22uc%22%3A20%7D; acw_tc=0a5088b217569088917503762e8bfe73414226f403ffca1e69fe74fa1b61df; web_session=040069b3ed6ebed4fbe38d058d3a4bf7c6f823; websectiga=29098a4cf41f76ee3f8db19051aaa60c0fc7c5e305572fec762da32d457d76ae; sec_poison_id=5944d42a-39e9-444e-b237-d629133962ab; loadts=1756910531213',
            'x-b3-traceid': 'test_xs_generator',
            'x-xray-traceid': 'test_xs_generator',
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
                        
                        # 显示前3条子评论
                        for i, comment in enumerate(comments[:3], 1):
                            print(f"\n{i}. {comment.get('user_info', {}).get('nickname', '')}")
                            print(f"   内容: {comment.get('content', '')}")
                            print(f"   点赞: {comment.get('like_count', 0)}")
                        
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
    # 禁用SSL警告
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    generator = TestXSGenerator()
    success = generator.test_sub_comment_api()
    
    if success:
        print("\n🎉 X-s生成算法测试成功!")
        print("✅ 可以成功获取小红书子评论数据!")
    else:
        print("\n❌ X-s生成算法需要调整")


if __name__ == "__main__":
    main()