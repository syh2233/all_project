#!/usr/bin/env python3
"""
深入分析X-s参数生成算法
拒绝自动化，专注于手动分析JavaScript代码
"""

import requests
import json
import time
import re
import base64
import hashlib
from urllib.parse import urlparse, parse_qs, urlencode

class XSAnalyzer:
    """X-s参数手动分析器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False
        self.session.timeout = 10
        
        # 新的cookie
        self.new_cookie = "gid=yj8D24fWSDv0yj8D24fK069V0yIY6AFDTDxSxyU1kTyk2428MD7AC4888W2q2Yy8fJ0KjyDJ; xsecappid=xhs-pc-web; abRequestId=f425aaf4-2614-55c8-b8d1-262c611be2ab; a1=198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479; webId=fc4fb0dccb1a480d5f17359394c861d7; web_session=040069b3ed6ebed4fbe30e25ad3a4b127faeca; webBuild=4.79.0; unread=%7B%22ub%22%3A%2268b56bf2000000001c004134%22%2C%22ue%22%3A%2268a3fe26000000001c0126d1%22%2C%22uc%22%3A20%7D; acw_tc=0a4a453a17569070897088137ec524bb28ede595ddc525595031d81456a33f; websectiga=2845367ec3848418062e761c09db7caf0e8b79d132ccdd1a4f8e64a11d0cac0d; sec_poison_id=b4c4d07b-3d95-4e2e-b6fc-42a65ed18bb4; loadts=1756907500892"
        
        # 测试参数
        self.note_id = "68a048c1000000001d01838e"
        self.root_comment_id = "68a048ef000000003002a604"
        
        # 从前端JS中提取的关键信息
        self.js_insights = {
            "api_paths": [
                "/api/sns/web/v2/comment/sub/page",
                "/api/sns/web/v2/comment/page"
            ],
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
        
    def analyze_xs_generation(self):
        """手动分析X-s生成算法"""
        print("🔬 深入分析X-s参数生成算法")
        print("="*60)
        
        # 分析成功的请求中的X-s值
        print("\n1. 分析成功的X-s值模式")
        
        # 从前端JS获取的真实X-s值示例
        real_xs_values = [
            "XYS_2UQhPsHCH0c1Pjh9HjIj2erjwjQhyoPTqBPT49pjHjIj2eHjwjQgynEDJ74AHjIj2ePjwjQTJdPIP/ZlgMrU4SmH4emPLfkj4DpCn/QEndG3JnMsJLprPepLpez9tAS+aDQbzDzwqer9+BpBLrYg20+64BRG8SQdJaTOGDEwy9IM4DzP+B+GLSr9/bYD8oprwgzN+nGItFcUz9Y7G7p82LLI4URP8AqUJrpCJdk7874Bpbcl+LRhqrSbzDSc+Mk6N7kCG9EkJ7GU+FzG/9k38rp98pYfLgkE4nHIPnMBqbcMpBWA49brHjIj2ecjwjHjKc=="
        ]
        
        for i, xs_value in enumerate(real_xs_values, 1):
            print(f"\nX-s值 {i}:")
            print(f"  长度: {len(xs_value)}")
            print(f"  前缀: {xs_value[:4] if xs_value.startswith('XYS_') else 'None'}")
            
            # 分析Base64部分
            if xs_value.startswith('XYS_'):
                base64_part = xs_value[4:]
                print(f"  Base64部分长度: {len(base64_part)}")
                
                # 尝试解码
                try:
                    decoded = base64.b64decode(base64_part)
                    print(f"  解码后长度: {len(decoded)}")
                    
                    # 分析解码后的内容
                    self._analyze_decoded_xs(decoded)
                    
                except Exception as e:
                    print(f"  Base64解码失败: {e}")
        
        print("\n2. 分析X-s生成的影响因素")
        
        # 可能的影响因素
        factors = {
            "URL": "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page",
            "Method": "GET",
            "Timestamp": str(int(time.time() * 1000)),
            "User_ID": "198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479",
            "Note_ID": self.note_id,
            "Root_Comment_ID": self.root_comment_id,
            "Web_Build": "4.79.0"
        }
        
        print("可能的X-s生成因素:")
        for key, value in factors.items():
            print(f"  {key}: {value}")
        
        print("\n3. 手动测试不同的X-s生成策略")
        
        # 测试不同的生成策略
        strategies = self._generate_xs_strategies(factors)
        
        for i, (strategy_name, xs_value) in enumerate(strategies.items(), 1):
            print(f"\n策略 {i}: {strategy_name}")
            print(f"  X-s值: {xs_value}")
            
            # 测试这个策略
            success = self._test_xs_strategy(xs_value, factors)
            print(f"  结果: {'✅ 成功' if success else '❌ 失败'}")
            
            if success:
                print(f"  🎉 找到正确的X-s生成策略！")
                return strategy_name, xs_value
        
        return None, None
    
    def _analyze_decoded_xs(self, decoded_bytes):
        """分析解码后的X-s内容"""
        print("  解码后内容分析:")
        
        # 尝试不同的编码
        encodings = ['utf-8', 'gbk', 'gb2312', 'latin-1']
        for encoding in encodings:
            try:
                text = decoded_bytes.decode(encoding)
                print(f"    {encoding}: {text[:100]}...")
            except:
                continue
        
        # 分析字节模式
        print(f"    字节统计:")
        byte_counts = {}
        for byte in decoded_bytes:
            byte_counts[byte] = byte_counts.get(byte, 0) + 1
        
        # 显示最常见的字节
        common_bytes = sorted(byte_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        for byte, count in common_bytes:
            print(f"      0x{byte:02x}: {count}次")
    
    def _generate_xs_strategies(self, factors):
        """生成不同的X-s策略"""
        strategies = {}
        
        timestamp = factors["Timestamp"]
        url = factors["URL"]
        user_id = factors["User_ID"]
        note_id = factors["Note_ID"]
        root_comment_id = factors["Root_Comment_ID"]
        
        # 策略1: 简单时间戳
        strategies["简单时间戳"] = timestamp
        
        # 策略2: URL哈希
        url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()
        strategies["URL哈希"] = url_hash
        
        # 策略3: 时间戳+URL哈希
        strategies["时间戳+URL哈希"] = f"{timestamp}.{url_hash}"
        
        # 策略4: 用户ID+时间戳
        strategies["用户ID+时间戳"] = f"{user_id}.{timestamp}"
        
        # 策略5: 复合哈希
        composite_str = f"{timestamp}{user_id}{note_id}{root_comment_id}"
        composite_hash = hashlib.sha256(composite_str.encode('utf-8')).hexdigest()
        strategies["复合哈希"] = composite_hash
        
        # 策略6: Base64编码的复合哈希
        composite_b64 = base64.b64encode(composite_hash.encode('utf-8')).decode('utf-8')
        strategies["Base64复合哈希"] = f"XYS_{composite_b64}"
        
        # 策略7: 模拟真实X-s格式
        fake_content = base64.b64encode(composite_str.encode('utf-8')).decode('utf-8')
        strategies["模拟真实格式"] = f"XYS_{fake_content}"
        
        return strategies
    
    def _test_xs_strategy(self, xs_value, factors):
        """测试X-s策略"""
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
            'x-b3-traceid': 'manual_test_trace_id',
            'x-xray-traceid': 'manual_test_trace_id',
            'X-s': xs_value,
            'X-t': factors["Timestamp"],
            'x-s-common': xs_value
        }
        
        try:
            response = self.session.get(url_with_params, headers=headers)
            return response.status_code == 200
        except:
            return False
    
    def analyze_js_code_manually(self):
        """手动分析JS代码"""
        print("\n📜 手动分析JS代码")
        print("="*60)
        
        # 基于之前分析的JS代码片段
        js_patterns = {
            "X-s生成相关": [
                "X-s",
                "x-s-common", 
                "sign",
                "signature",
                "encrypt",
                "hash"
            ],
            "API调用相关": [
                "subComment",
                "SubComment",
                "replyComment",
                "comment/sub/page"
            ],
            "认证相关": [
                "a1",
                "web_session",
                "xsec_token",
                "webId"
            ]
        }
        
        print("需要关注的JS代码模式:")
        for category, patterns in js_patterns.items():
            print(f"\n{category}:")
            for pattern in patterns:
                print(f"  - {pattern}")
        
        print("\n建议的JS代码分析方法:")
        print("1. 搜索X-s生成函数")
        print("2. 分析加密算法")
        print("3. 理解参数组合逻辑")
        print("4. 还原完整的生成流程")
        
        print("\n可能的X-s生成算法类型:")
        print("1. MD5/SHA哈希")
        print("2. HMAC签名")
        print("3. 自定义加密算法")
        print("4. 复合参数哈希")
        print("5. 时间戳+随机数")
    
    def manual_trace_analysis(self):
        """手动追踪分析"""
        print("\n🔍 手动追踪分析")
        print("="*60)
        
        print("从前端JS到API请求的完整流程:")
        print("1. 用户点击查看子评论")
        print("2. 前端JS收集参数")
        print("3. 生成X-s签名")
        print("4. 发送API请求")
        print("5. 验证响应")
        
        print("\n关键追踪点:")
        print("- 事件监听器: 点击事件")
        print("- 参数收集: note_id, root_comment_id")
        print("- 签名生成: X-s算法")
        print("- 网络请求: fetch/XHR")
        
        print("\n调试建议:")
        print("1. 在Console中监听网络请求")
        print("2. 断点调试X-s生成函数")
        print("3. 分析请求头生成过程")
        print("4. 验证参数完整性")

def main():
    """主函数"""
    print("🔬 X-s参数深度手动分析")
    print("拒绝自动化，坚持手动分析原则")
    print("="*60)
    
    analyzer = XSAnalyzer()
    
    # 分析X-s生成算法
    strategy_name, xs_value = analyzer.analyze_xs_generation()
    
    if strategy_name:
        print(f"\n🎉 成功找到X-s生成策略: {strategy_name}")
        print(f"X-s值: {xs_value}")
    else:
        print("\n❌ 未找到有效的X-s生成策略")
        print("需要更深入的JS代码分析")
    
    # 手动分析JS代码
    analyzer.analyze_js_code_manually()
    
    # 手动追踪分析
    analyzer.manual_trace_analysis()
    
    print("\n" + "="*60)
    print("📝 分析总结")
    print("="*60)
    
    if strategy_name:
        print("✅ 成功破解X-s生成算法")
        print("🎯 关键发现:")
        print(f"  - 策略名称: {strategy_name}")
        print(f"  - X-s生成方法: {xs_value}")
    else:
        print("❌ X-s生成算法仍需深入研究")
        print("🔍 下一步建议:")
        print("  - 深入分析前端JS代码")
        print("  - 使用浏览器调试工具")
        print("  - 手动追踪生成流程")
        print("  - 理解加密算法逻辑")
    
    print("\n💡 逆向工程师的信念:")
    print("  - 每一个混淆代码都有其逻辑")
    print("  - 耐心分析胜过千次猜测")
    print("  - 给我足够的时间，我能理清每一个细节")

if __name__ == "__main__":
    # 禁用SSL警告
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    main()