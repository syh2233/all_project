#!/usr/bin/env python3
"""
深入调试真实请求
分析为什么真实请求数据也返回406
"""

import json
import time
import base64
import hashlib
import hmac
import requests
from urllib.parse import urlencode
import re


class DeepDebugTester:
    """深入调试测试器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False
        self.session.timeout = 10
        
        # 用户提供的真实数据
        self.real_data = {
            'url': 'https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page',
            'params': {
                'note_id': '68a048c1000000001d01838e',
                'root_comment_id': '68afc3820000000030031abb',
                'num': '10',
                'cursor': '68afca010000000030024344',
                'image_formats': 'jpg,webp,avif',
                'top_comment_id': '',
                'xsec_token': 'ABIyAXG1J9ckAl0VbljygE3I8b6TZ0k5P4jORY-kCIzzw%3D'
            },
            'headers': {
                'accept': 'application/json, text/plain, */*',
                'accept-encoding': 'gzip, deflate, br, zstd',
                'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,en-GB;q=0.6',
                'cookie': 'gid=yj8D24fWSDv0yj8D24fK069V0yIY6AFDTDxSxyU1kTyk2428MD7AC4888W2q2Yy8fJ0KjyDJ; xsecappid=xhs-pc-web; abRequestId=f425aaf4-2614-55c8-b8d1-262c611be2ab; a1=198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479; webId=fc4fb0dccb1a480d5f17359394c861d7; webBuild=4.79.0; unread={%22ub%22:%2268b56bf2000000001c004134%22%2C%22ue%22:%2268a3fe26000000001c0126d1%22%2C%22uc%22:20}; web_session=040069b3ed6ebed4fbe38d058d3a4bf7c6f823; acw_tc=0ad6fbc617569107128742232e696e7b433faff25686acd79e6530ace1a727; loadts=1756911545822; websectiga=10f9a40ba454a07755a08f27ef8194c53637eba4551cf9751c009d9afb564467; sec_poison_id=bf67a3e0-d1ed-48ea-b10b-654b54b846e9',
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
                'x-s': 'XYS_2UQhPsHCH0c1Pjh9HjIj2erjwjQhyoPTqBPT49pjHjIj2eHjwjQgynEDJ74AHjIj2ePjwjQTJdPIP/ZlgMrU4SmH4rMHJrGE20pk8pYLLSYc+Fu6P0Dl4B8e4o4gyLRz+LQgLjVlPMmdzA+94piInniIJLkdn/+V4fzk8r+INMbVyFEgzAmOzfEE4oScwnbGN7mT4DEk40SgPrS6zri6JeWUcfzkJrSwypkV4Am+2e8oaSztJ9l+nri3PS4C+pD6n/pD4LEL2b+ILMSzy7khy9kgzrTFyBYCzrSBnfHFPFTcPd8cPDP9HjIj2ecjwjHjKc==',
                'x-s-common': '2UQAPsHC+aIjqArjwjHjNsQhPsHCH0rjNsQhPaHCH0c1Pjh9HjIj2eHjwjQgynEDJ74AHjIj2ePjwjQhyoPTqBPT49pjHjIj2ecjwjHFN0qEN0ZjNsQh+aHCH0rEweDIwBP9G0rFPA41PoD98/Q7qeSfy9QVyn+Tyn4I8BkfG9rlJ7qh+/ZIPeZ9+ecF+ADjNsQh+jHCHjHVHdW7H0ijHjIj2eWjwjQQPAYUaBzdq9k6qB4Q4fpA8b878FSet9RQzLlTcSiM+/+n4MYP8F8LagY/P9Ql4FpUzfpS2BcI8nT1GFbC/L88JdbFyrSiafp/8DMra7pFLDDAa7+8J7QgabmFz7Qjp0mcwp4fanD68p40+fp8qgzELLbILrDA+9p3JpH9LLI3+LSk+d+DJfpSL98lnLYl49IUqgcMc0mrcDShtMmozBD6qM8FyFSh8o+h4g4U+obFyLSi4nbQz/+SPFlnPrDApSzQcA4SPopFJeQmzBMA/o8Szb+NqM+c4ApQzg8Ayp8FaDRl4AYs4g4fLomD8pzBpFRQ2ezLanSM+Skc47Qc4gcMag8VGLlj87PAqgzhagYSqAbn4FYQy7pTanTQ2npx87+8NM4L89L78p+l4BL6ze4AzB+IygmS8Bp8qDzFaLP98Lzn4AQQzLEAL7bFJBEVL7pwyS8Fag868nTl4e+0n04ApfuF8FSbL7SQyrpELLQl4LShyBEl20YdanTQ8fRl49TQcMkgwBuAq9zV/9pnLoqAag8m8/mf89pDzBY7aLpOqAbgtF8EqgzGanWA8/bDcnLAzDRApSm7/9pf/7+8qgcAagYLq94p+d+/4gqM/e4Nq98n494QPMQCa/PFP7Qn4Fh6pdqFcfkBG7SI/7+D8/4Apdb7tFS3a9prPrbApDlacDS9+nphPBzS8rD3cDSe87+fLo4Hag8QzSbc4FYcpdzmagWM8/8M4o8Qy9RS+dp7+LSiP7+x4gqM/db7z9Rn47pQc7kLag8a4bbSpDboJsRAygbFzDSiLozQynpSngp7J9pgG9+IpLRAzo+34LSiLdSFLo472db7cLS38g+gqgzMqLSmqM8B+dPlanQPaLLIqA8S8o+kLoz0GMm7qDSeafpxqg4panSd8gWI/BMQ4DESzBq68/mc4b+QcFTA+Sm7+0z6JgbQyrYSaL+d8p8PcnpL878SnnH9qMSc47qjNsQhwaHCP0ZFP/Lh+/LINsQhP/Zjw0ZVHdWlPaHCHfE6qfMYJsQR',
                'x-t': '1756912210589',
                'x-xray-traceid': 'cc8810694965f7f2c02f0058a1937bf1'
            }
        }
    
    def test_cookie_validity(self):
        """测试cookie有效性"""
        print("🔍 测试Cookie有效性")
        print("="*40)
        
        # 解析cookie
        cookie_str = self.real_data['headers']['cookie']
        cookie_parts = cookie_str.split('; ')
        
        print(f"Cookie包含 {len(cookie_parts)} 个部分:")
        for part in cookie_parts:
            if '=' in part:
                key, value = part.split('=', 1)
                print(f"  {key}: {value[:50]}{'...' if len(value) > 50 else ''}")
        
        # 检查关键cookie
        key_cookies = ['web_session', 'a1', 'xsecappid', 'webId']
        for key in key_cookies:
            found = any(part.startswith(key + '=') for part in cookie_parts)
            print(f"  {key}: {'✅ 存在' if found else '❌ 缺失'}")
        
        # 检查时间戳
        loadts_match = re.search(r'loadts=(\d+)', cookie_str)
        if loadts_match:
            loadts = int(loadts_match.group(1))
            current_time = int(time.time() * 1000)
            age_minutes = (current_time - loadts) / (1000 * 60)
            print(f"  loadts年龄: {age_minutes:.1f} 分钟")
            
            if age_minutes > 60:
                print("  ⚠️ loadts可能已过期")
            else:
                print("  ✅ loadts看起来新鲜")
    
    def test_timestamp_issues(self):
        """测试时间戳问题"""
        print(f"\n🔍 测试时间戳问题")
        print("="*40)
        
        original_xt = self.real_data['headers']['x-t']
        current_time = int(time.time() * 1000)
        
        print(f"原始X-t: {original_xt}")
        print(f"当前时间: {current_time}")
        print(f"时间差: {current_time - int(original_xt)} 毫秒")
        
        if abs(current_time - int(original_xt)) > 300000:  # 5分钟
            print("⚠️ 时间戳差异过大，可能已过期")
        else:
            print("✅ 时间戳看起来合理")
        
        # 测试不同的时间戳
        timestamps_to_test = [
            original_xt,  # 原始时间戳
            str(current_time),  # 当前时间戳
            str(current_time - 60000),  # 1分钟前
            str(current_time - 300000),  # 5分钟前
        ]
        
        print(f"\n测试不同时间戳:")
        for i, ts in enumerate(timestamps_to_test, 1):
            headers = self.real_data['headers'].copy()
            headers['x-t'] = ts
            headers['x-b3-traceid'] = f'timestamp_test_{i}'
            headers['x-xray-traceid'] = f'timestamp_test_{i}'
            
            try:
                full_url = self.real_data['url'] + '?' + urlencode(self.real_data['params'])
                response = self.session.get(full_url, headers=headers)
                print(f"  测试{i}: {ts} -> 状态码 {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success', False):
                        print(f"    🎉 测试{i}成功!")
                        return True
            except Exception as e:
                print(f"  测试{i}: 异常 {e}")
        
        return False
    
    def test_trace_id_variations(self):
        """测试trace ID变化"""
        print(f"\n🔍 测试Trace ID变化")
        print("="*40)
        
        # 生成随机trace ID
        import random
        import string
        
        def generate_random_id(length=16):
            return ''.join(random.choices(string.hexdigits.lower(), k=length))
        
        trace_variations = [
            ("原始", self.real_data['headers']['x-b3-traceid'], self.real_data['headers']['x-xray-traceid']),
            ("随机", generate_random_id(), generate_random_id()),
            ("空", "", ""),
            ("相同", generate_random_id(), generate_random_id()),
        ]
        
        for name, b3_trace, xray_trace in trace_variations:
            headers = self.real_data['headers'].copy()
            headers['x-b3-traceid'] = b3_trace
            headers['x-xray-traceid'] = xray_trace
            headers['x-t'] = str(int(time.time() * 1000))  # 更新时间戳
            
            try:
                full_url = self.real_data['url'] + '?' + urlencode(self.real_data['params'])
                response = self.session.get(full_url, headers=headers)
                print(f"  {name}: 状态码 {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success', False):
                        print(f"    🎉 {name} trace ID成功!")
                        return True
            except Exception as e:
                print(f"  {name}: 异常 {e}")
        
        return False
    
    def test_parameter_variations(self):
        """测试参数变化"""
        print(f"\n🔍 测试参数变化")
        print("="*40)
        
        # 测试不同的参数组合
        param_variations = [
            ("原始", self.real_data['params'].copy()),
            ("无cursor", {k: v for k, v in self.real_data['params'].items() if k != 'cursor'}),
            ("无top_comment_id", {k: v for k, v in self.real_data['params'].items() if k != 'top_comment_id'}),
            ("无num", {k: v for k, v in self.real_data['params'].items() if k != 'num'}),
            ("修改cursor", {**self.real_data['params'], 'cursor': '68afca010000000030024345'}),
        ]
        
        for name, params in param_variations:
            print(f"\n测试 {name}:")
            print(f"  参数: {params}")
            
            headers = self.real_data['headers'].copy()
            headers['x-t'] = str(int(time.time() * 1000))
            headers['x-b3-traceid'] = f'param_test_{name}'
            headers['x-xray-traceid'] = f'param_test_{name}'
            
            try:
                full_url = self.real_data['url'] + '?' + urlencode(params)
                response = self.session.get(full_url, headers=headers)
                print(f"  状态码: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success', False):
                        print(f"    🎉 {name} 参数成功!")
                        return True
                    else:
                        msg = data.get('msg', 'Unknown error')
                        print(f"    失败原因: {msg}")
            except Exception as e:
                print(f"  异常: {e}")
        
        return False
    
    def test_main_comment_api(self):
        """测试主评论API确认cookie仍然有效"""
        print(f"\n🔍 测试主评论API (确认cookie有效性)")
        print("="*50)
        
        # 构建主评论API请求
        main_params = {
            'note_id': self.real_data['params']['note_id'],
            'cursor': '',
            'top_comment_id': '',
            'image_formats': 'jpg,webp,avif',
            'xsec_token': 'ABIyAXG1J9ckAl0VbljygE3I8b6TZ0k5P4jORY-kCIzzw%3D'
        }
        
        main_url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/page"
        full_url = main_url + '?' + urlencode(main_params)
        
        # 使用相同的cookie
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,en-GB;q=0.6',
            'cookie': self.real_data['headers']['cookie'],
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
            'x-t': str(int(time.time() * 1000)),
            'x-b3-traceid': 'main_api_test',
            'x-xray-traceid': 'main_api_test'
        }
        
        # 生成主评论X-s
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
        xs_value = f"XYS_{base64_result}"
        
        headers['X-s'] = xs_value
        headers['x-s-common'] = xs_value
        
        try:
            response = self.session.get(full_url, headers=headers)
            print(f"主评论API状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                success = data.get('success', False)
                print(f"主评论API成功: {success}")
                
                if success:
                    comments = data.get('data', {}).get('comments', [])
                    print(f"✅ Cookie有效，主评论API正常，获取到 {len(comments)} 条评论")
                    return True
                else:
                    msg = data.get('msg', 'Unknown error')
                    print(f"❌ 主评论API失败: {msg}")
            else:
                print(f"❌ 主评论API请求失败")
        except Exception as e:
            print(f"❌ 主评论API异常: {e}")
        
        return False
    
    def run_deep_analysis(self):
        """运行深度分析"""
        print("🌟 深入调试真实请求")
        print("="*60)
        
        # 测试cookie有效性
        self.test_cookie_validity()
        
        # 测试主评论API
        main_api_works = self.test_main_comment_api()
        
        if not main_api_works:
            print(f"\n❌ 主评论API也失败了，说明cookie可能已过期")
            return False
        
        print(f"\n✅ 主评论API正常，问题特定于子评论API")
        
        # 测试时间戳
        timestamp_success = self.test_timestamp_issues()
        if timestamp_success:
            print(f"\n🎉 找到时间戳解决方案!")
            return True
        
        # 测试trace ID
        trace_success = self.test_trace_id_variations()
        if trace_success:
            print(f"\n🎉 找到trace ID解决方案!")
            return True
        
        # 测试参数
        param_success = self.test_parameter_variations()
        if param_success:
            print(f"\n🎉 找到参数解决方案!")
            return True
        
        print(f"\n❌ 深度分析完成，未找到解决方案")
        print("💡 可能的原因:")
        print("  1. 子评论API有特殊的频率限制")
        print("  2. 需要特定的请求顺序")
        print("  3. 需要其他未知的动态参数")
        print("  4. 服务器端问题")
        
        return False


def main():
    """主函数"""
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    debugger = DeepDebugTester()
    debugger.run_deep_analysis()


if __name__ == "__main__":
    main()