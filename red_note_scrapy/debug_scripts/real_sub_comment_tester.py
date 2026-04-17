#!/usr/bin/env python3
"""
真实子评论API测试
使用用户提供的真实请求数据进行测试
"""

import json
import time
import base64
import hashlib
import hmac
import requests
from urllib.parse import urlencode


class RealSubCommentTester:
    """真实子评论API测试器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False
        self.session.timeout = 10
        
        # 使用用户提供的真实cookie
        self.cookie = 'gid=yj8D24fWSDv0yj8D24fK069V0yIY6AFDTDxSxyU1kTyk2428MD7AC4888W2q2Yy8fJ0KjyDJ; xsecappid=xhs-pc-web; abRequestId=f425aaf4-2614-55c8-b8d1-262c611be2ab; a1=198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479; webId=fc4fb0dccb1a480d5f17359394c861d7; webBuild=4.79.0; unread={%22ub%22:%2268b56bf2000000001c004134%22%2C%22ue%22:%2268a3fe26000000001c0126d1%22%2C%22uc%22:20}; web_session=040069b3ed6ebed4fbe38d058d3a4bf7c6f823; acw_tc=0ad6fbc617569107128742232e696e7b433faff25686acd79e6530ace1a727; loadts=1756911545822; websectiga=10f9a40ba454a07755a08f27ef8194c53637eba4551cf9751c009d9afb564467; sec_poison_id=bf67a3e0-d1ed-48ea-b10b-654b54b846e9'
        
        # 用户提供的真实参数
        self.note_id = "68a048c1000000001d01838e"
        self.root_comment_id = "68afc3820000000030031abb"
        self.cursor = "68afca010000000030024344"
        self.num = "10"
        
        # 用户提供的真实X-s值
        self.real_xs = "XYS_2UQhPsHCH0c1Pjh9HjIj2erjwjQhyoPTqBPT49pjHjIj2eHjwjQgynEDJ74AHjIj2ePjwjQTJdPIP/ZlgMrU4SmH4rMHJrGE20pk8pYLLSYc+Fu6P0Dl4B8e4o4gyLRz+LQgLjVlPMmdzA+94piInniIJLkdn/+V4fzk8r+INMbVyFEgzAmOzfEE4oScwnbGN7mT4DEk40SgPrS6zri6JeWUcfzkJrSwypkV4Am+2e8oaSztJ9l+nri3PS4C+pD6n/pD4LEL2b+ILMSzy7khy9kgzrTFyBYCzrSBnfHFPFTcPd8cPDP9HjIj2ecjwjHjKc=="
        
        # 用户提供的真实x-s-common值
        self.real_xs_common = "2UQAPsHC+aIjqArjwjHjNsQhPsHCH0rjNsQhPaHCH0c1Pjh9HjIj2eHjwjQgynEDJ74AHjIj2ePjwjQhyoPTqBPT49pjHjIj2ecjwjHFN0qEN0ZjNsQh+aHCH0rEweDIwBP9G0rFPA41PoD98/Q7qeSfy9QVyn+Tyn4I8BkfG9rlJ7qh+/ZIPeZ9+ecF+ADjNsQh+jHCHjHVHdW7H0ijHjIj2eWjwjQQPAYUaBzdq9k6qB4Q4fpA8b878FSet9RQzLlTcSiM+/+n4MYP8F8LagY/P9Ql4FpUzfpS2BcI8nT1GFbC/L88JdbFyrSiafp/8DMra7pFLDDAa7+8J7QgabmFz7Qjp0mcwp4fanD68p40+fp8qgzELLbILrDA+9p3JpH9LLI3+LSk+d+DJfpSL98lnLYl49IUqgcMc0mrcDShtMmozBD6qM8FyFSh8o+h4g4U+obFyLSi4nbQz/+SPFlnPrDApSzQcA4SPopFJeQmzBMA/o8Szb+NqM+c4ApQzg8Ayp8FaDRl4AYs4g4fLomD8pzBpFRQ2ezLanSM+Skc47Qc4gcMag8VGLlj87PAqgzhagYSqAbn4FYQy7pTanTQ2npx87+8NM4L89L78p+l4BL6ze4AzB+IygmS8Bp8qDzFaLP98Lzn4AQQzLEAL7bFJBEVL7pwyS8Fag868nTl4e+0n04ApfuF8FSbL7SQyrpELLQl4LShyBEl20YdanTQ8fRl49TQcMkgwBuAq9zV/9pnLoqAag8m8/mf89pDzBY7aLpOqAbgtF8EqgzGanWA8/bDcnLAzDRApSm7/9pf/7+8qgcAagYLq94p+d+/4gqM/e4Nq98n494QPMQCa/PFP7Qn4Fh6pdqFcfkBG7SI/7+D8/4Apdb7tFS3a9prPrbApDlacDS9+nphPBzS8rD3cDSe87+fLo4Hag8QzSbc4FYcpdzmagWM8/8M4o8Qy9RS+dp7+LSiP7+x4gqM/db7z9Rn47pQc7kLag8a4bbSpDboJsRAygbFzDSiLozQynpSngp7J9pgG9+IpLRAzo+34LSiLdSFLo472db7cLS38g+gqgzMqLSmqM8B+dPlanQPaLLIqA8S8o+kLoz0GMm7qDSeafpxqg4panSd8gWI/BMQ4DESzBq68/mc4b+QcFTA+Sm7+0z6JgbQyrYSaL+d8p8PcnpL878SnnH9qMSc47qjNsQhwaHCP0ZFP/Lh+/LINsQhP/Zjw0ZVHdWlPaHCHfE6qfMYJsQR"
        
    def test_real_request(self):
        """测试真实请求"""
        print("🧪 测试真实子评论API请求")
        print("="*60)
        
        # 构建真实的URL
        params = {
            'note_id': self.note_id,
            'root_comment_id': self.root_comment_id,
            'num': self.num,
            'cursor': self.cursor,
            'image_formats': 'jpg,webp,avif',
            'top_comment_id': '',
            'xsec_token': 'ABIyAXG1J9ckAl0VbljygE3I8b6TZ0k5P4jORY-kCIzzw%3D'
        }
        
        url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page"
        full_url = url + '?' + urlencode(params)
        
        print(f"URL: {full_url}")
        print(f"X-s: {self.real_xs[:100]}...")
        print(f"X-s-common: {self.real_xs_common[:100]}...")
        
        # 构建真实的请求头
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,en-GB;q=0.6',
            'cookie': self.cookie,
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
            'x-b3-traceid': '891583b054249abe',
            'x-s': self.real_xs,
            'x-s-common': self.real_xs_common,
            'x-t': '1756912210589',
            'x-xray-traceid': 'cc8810694965f7f2c02f0058a1937bf1'
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
                    
                    # 显示前3条评论
                    for i, comment in enumerate(comments[:3], 1):
                        print(f"  {i}. {comment.get('user_info', {}).get('nickname', '')}")
                        print(f"     内容: {comment.get('content', '')[:50]}...")
                        print(f"     点赞: {comment.get('like_count', 0)}")
                    
                    return True
                else:
                    msg = data.get('msg', 'Unknown error')
                    print(f"❌ API失败: {msg}")
            else:
                print(f"❌ 请求失败")
                if response.text:
                    print(f"响应: {response.text[:200]}")
        except Exception as e:
            print(f"❌ 请求异常: {e}")
        
        return False
    
    def test_generated_xs(self):
        """测试生成的X-s"""
        print(f"\n🧪 测试生成的X-s")
        print("="*40)
        
        # 构建URL
        params = {
            'note_id': self.note_id,
            'root_comment_id': self.root_comment_id,
            'num': self.num,
            'cursor': self.cursor,
            'image_formats': 'jpg,webp,avif',
            'top_comment_id': '',
            'xsec_token': 'ABIyAXG1J9ckAl0VbljygE3I8b6TZ0k5P4jORY-kCIzzw%3D'
        }
        
        url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page"
        full_url = url + '?' + urlencode(params)
        
        # 生成X-s
        timestamp = str(int(time.time() * 1000))
        base_string = f"{timestamp}{full_url}"
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
        
        target_length = 241
        if len(utf8_bytes) < target_length:
            padding = bytes([0x6a] * (target_length - len(utf8_bytes)))
            final_bytes = utf8_bytes + padding
        else:
            final_bytes = utf8_bytes[:target_length]
        
        base64_result = base64.b64encode(final_bytes).decode()
        generated_xs = f"XYS_{base64_result}"
        
        print(f"生成的X-s: {generated_xs[:100]}...")
        print(f"真实X-s: {self.real_xs[:100]}...")
        print(f"是否相同: {generated_xs == self.real_xs}")
        
        # 测试生成的X-s
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,en-GB;q=0.6',
            'cookie': self.cookie,
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
            'x-b3-traceid': 'test_generated',
            'x-s': generated_xs,
            'x-s-common': generated_xs,  # 注意：这里使用相同的值
            'x-t': str(int(time.time() * 1000)),
            'x-xray-traceid': 'test_generated'
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
                    print(f"🎉 生成X-s成功! 获取到 {len(comments)} 条子评论")
                    return True
                else:
                    msg = data.get('msg', 'Unknown error')
                    print(f"❌ API失败: {msg}")
            else:
                print(f"❌ 请求失败")
        except Exception as e:
            print(f"❌ 请求异常: {e}")
        
        return False
    
    def test_xs_common_difference(self):
        """测试x-s-common的差异"""
        print(f"\n🧪 测试x-s-common差异")
        print("="*40)
        
        # 构建URL
        params = {
            'note_id': self.note_id,
            'root_comment_id': self.root_comment_id,
            'num': self.num,
            'cursor': self.cursor,
            'image_formats': 'jpg,webp,avif',
            'top_comment_id': '',
            'xsec_token': 'ABIyAXG1J9ckAl0VbljygE3I8b6TZ0k5P4jORY-kCIzzw%3D'
        }
        
        url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page"
        full_url = url + '?' + urlencode(params)
        
        # 生成X-s
        timestamp = str(int(time.time() * 1000))
        base_string = f"{timestamp}{full_url}"
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
        
        target_length = 241
        if len(utf8_bytes) < target_length:
            padding = bytes([0x6a] * (target_length - len(utf8_bytes)))
            final_bytes = utf8_bytes + padding
        else:
            final_bytes = utf8_bytes[:target_length]
        
        base64_result = base64.b64encode(final_bytes).decode()
        generated_xs = f"XYS_{base64_result}"
        
        # 测试1: 使用真实X-s但生成的x-s-common
        headers1 = {
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,en-GB;q=0.6',
            'cookie': self.cookie,
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
            'x-b3-traceid': 'test_mixed_1',
            'x-s': self.real_xs,
            'x-s-common': generated_xs,  # 混合使用
            'x-t': str(int(time.time() * 1000)),
            'x-xray-traceid': 'test_mixed_1'
        }
        
        print("测试1: 真实X-s + 生成x-s-common")
        try:
            response = self.session.get(full_url, headers=headers1)
            print(f"  状态码: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"  成功: {data.get('success', False)}")
        except Exception as e:
            print(f"  异常: {e}")
        
        # 测试2: 使用生成X-s但真实的x-s-common
        headers2 = headers1.copy()
        headers2['x-s'] = generated_xs
        headers2['x-s-common'] = self.real_xs_common
        headers2['x-b3-traceid'] = 'test_mixed_2'
        headers2['x-xray-traceid'] = 'test_mixed_2'
        
        print("测试2: 生成X-s + 真实x-s-common")
        try:
            response = self.session.get(full_url, headers=headers2)
            print(f"  状态码: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"  成功: {data.get('success', False)}")
        except Exception as e:
            print(f"  异常: {e}")
    
    def analyze_real_xs(self):
        """分析真实X-s的结构"""
        print(f"\n🔍 分析真实X-s结构")
        print("="*40)
        
        print(f"真实X-s长度: {len(self.real_xs)}")
        print(f"真实x-s-common长度: {len(self.real_xs_common)}")
        
        # 分析X-s
        if self.real_xs.startswith("XYS_"):
            base64_part = self.real_xs[4:]
            try:
                decoded = base64.b64decode(base64_part)
                print(f"X-s Base64解码长度: {len(decoded)}")
                
                # 尝试解析为JSON
                try:
                    json_str = decoded.decode('utf-8', errors='ignore')
                    if json_str.startswith('{') and json_str.endswith('}'):
                        json_obj = json.loads(json_str)
                        print(f"X-s JSON结构: {list(json_obj.keys())}")
                        for key, value in json_obj.items():
                            print(f"  {key}: {value}")
                except:
                    print("X-s不是有效的JSON结构")
                
            except Exception as e:
                print(f"X-s Base64解码失败: {e}")
        
        # 分析x-s-common
        try:
            decoded_common = base64.b64decode(self.real_xs_common)
            print(f"x-s-common解码长度: {len(decoded_common)}")
            print(f"x-s-common前50字节: {decoded_common[:50]}")
        except Exception as e:
            print(f"x-s-common解码失败: {e}")
    
    def run_tests(self):
        """运行所有测试"""
        print("🌟 真实子评论API测试器")
        print("="*60)
        
        # 分析真实X-s
        self.analyze_real_xs()
        
        # 测试真实请求
        real_success = self.test_real_request()
        
        # 测试生成的X-s
        generated_success = self.test_generated_xs()
        
        # 测试x-s-common差异
        self.test_xs_common_difference()
        
        print(f"\n📊 测试结果:")
        print(f"真实X-s: {'✅ 成功' if real_success else '❌ 失败'}")
        print(f"生成X-s: {'✅ 成功' if generated_success else '❌ 失败'}")
        
        if real_success:
            print(f"\n🎉 真实X-s测试成功! 说明API本身是工作的")
            print(f"💡 下一步需要分析真实X-s的生成算法")
        elif generated_success:
            print(f"\n🎉 生成X-s测试成功! 说明我们的算法是正确的")
        else:
            print(f"\n❌ 两种方法都失败了，需要进一步分析")


def main():
    """主函数"""
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    tester = RealSubCommentTester()
    tester.run_tests()


if __name__ == "__main__":
    main()