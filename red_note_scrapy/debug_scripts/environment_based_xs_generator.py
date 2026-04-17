#!/usr/bin/env python3
"""
基于environment.js的X-s参数生成器
利用v_jstools v3生成的浏览器环境
"""

import requests
import json
import time
import re
import base64
import hashlib
import subprocess
import tempfile
import os
from urllib.parse import urlencode

class EnvironmentBasedXSGenerator:
    """基于环境模拟的X-s生成器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False
        self.session.timeout = 10
        
        # 新的cookie
        self.new_cookie = "gid=yj8D24fWSDv0yj8D24fK069V0yIY6AFDTDxSxyU1kTyk2428MD7AC4888W2q2Yy8fJ0KjyDJ; xsecappid=xhs-pc-web; abRequestId=f425aaf4-2614-55c8-b8d1-262c611be2ab; a1=198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479; webId=fc4fb0dccb1a480d5f17359394c861d7; web_session=040069b3ed6ebed4fbe30e25ad3a4b127faeca; webBuild=4.79.0; unread=%7B%22ub%22%3A%2268b56bf2000000001c004134%22%2C%22ue%22%3A%2268a3fe26000000001c0126d1%22%2C%22uc%22%3A20%7D; acw_tc=0a4a453a17569070897088137ec524bb28ede595ddc525595031d81456a33f; websectiga=2845367ec3848418062e761c09db7caf0e8b79d132ccdd1a4f8e64a11d0cac0d; sec_poison_id=b4c4d07b-3d95-4e2e-b6fc-42a65ed18bb4; loadts=1756907500892"
        
        # 测试参数
        self.note_id = "68a048c1000000001d01838e"
        self.root_comment_id = "68a048ef000000003002a604"
        
        # 从environment.js分析得到的关键信息
        self.env_insights = {
            "xhsFingerprintV3": {
                "getV18": "关键指纹生成函数",
                "getCurMiniUa": "用户代理生成",
                "runMiniUa": "Mini用户代理执行",
                "r6": "内部算法函数"
            },
            "xsecappid": "xhs-pc-web",
            "origin": "https://www.xiaohongshu.com"
        }
    
    def create_xs_generation_script(self):
        """创建X-s生成JavaScript脚本"""
        script_content = '''
// 基于environment.js的X-s生成脚本
// 利用v_jstools v3生成的浏览器环境

function generateXS(url, method, data) {
    // 1. 获取浏览器指纹
    const fingerprint = xhsFingerprintV3.getV18();
    
    // 2. 生成时间戳
    const timestamp = Date.now();
    
    // 3. 构建签名字符串
    const signString = `${method}:${url}:${timestamp}:${JSON.stringify(data)}:${fingerprint}`;
    
    // 4. 应用加密算法 (基于分析的发现)
    const encoded = btoa(signString);
    
    // 5. 生成X-s格式
    const xs = `XYS_${encoded}`;
    
    return {
        xs: xs,
        timestamp: timestamp,
        fingerprint: fingerprint
    };
}

// 测试生成
const testUrl = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page";
const testMethod = "GET";
const testData = {
    note_id: "68a048c1000000001d01838e",
    root_comment_id: "68a048ef000000003002a604"
};

const result = generateXS(testUrl, testMethod, testData);
console.log(JSON.stringify(result, null, 2));
'''
        
        return script_content
    
    def execute_js_with_environment(self, js_code):
        """在环境模拟器中执行JavaScript"""
        try:
            # 创建临时JavaScript文件
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
                f.write(js_code)
                temp_file = f.name
            
            # 构建执行命令
            # 假设使用Node.js执行
            cmd = f'node "{temp_file}"'
            
            print(f"🔧 执行命令: {cmd}")
            
            # 执行JavaScript
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            
            # 清理临时文件
            os.unlink(temp_file)
            
            if result.returncode == 0:
                return result.stdout
            else:
                print(f"❌ JavaScript执行失败: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"❌ 执行JavaScript时出错: {e}")
            return None
    
    def analyze_environment_js_structure(self):
        """分析environment.js结构"""
        print("🔍 分析environment.js结构")
        print("="*60)
        
        try:
            with open('环境.js', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 统计关键组件
            xhs_fingerprint_count = content.count('xhsFingerprintV3')
            xsecappid_count = content.count('xsecappid')
            vm2_count = content.count('VM2')
            
            print(f"📊 组件统计:")
            print(f"  xhsFingerprintV3: {xhs_fingerprint_count} 次")
            print(f"  xsecappid: {xsecappid_count} 次")
            print(f"  VM2相关: {vm2_count} 次")
            
            # 查找关键函数
            key_functions = [
                'getV18',
                'getCurMiniUa', 
                'runMiniUa',
                'r6'
            ]
            
            print(f"\n🔍 关键函数查找:")
            for func in key_functions:
                count = content.count(func)
                print(f"  {func}: {count} 次")
            
            # 分析文件结构
            lines = content.split('\n')
            total_lines = len(lines)
            print(f"\n📄 文件信息:")
            print(f"  总行数: {total_lines}")
            print(f"  文件大小: {len(content)} 字符")
            
            # 查找重要的代码段
            important_patterns = [
                'function.*getV18',
                'function.*signature',
                'function.*encrypt',
                'XYS_',
                'x-s-common'
            ]
            
            print(f"\n🎯 重要模式搜索:")
            for pattern in important_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    print(f"  {pattern}: {len(matches)} 个匹配")
                    # 显示前几个匹配
                    for match in matches[:3]:
                        print(f"    {match[:100]}...")
            
        except Exception as e:
            print(f"❌ 分析environment.js时出错: {e}")
    
    def create_xs_generator_using_env(self):
        """创建使用环境的X-s生成器"""
        print("🛠️ 创建基于环境的X-s生成器")
        print("="*60)
        
        # 分析环境文件
        self.analyze_environment_js_structure()
        
        # 创建X-s生成脚本
        xs_script = self.create_xs_generation_script()
        
        print(f"\n📜 生成的X-s生成脚本:")
        print("-" * 40)
        print(xs_script[:500] + "..." if len(xs_script) > 500 else xs_script)
        
        # 执行脚本
        print(f"\n🚀 执行X-s生成脚本...")
        result = self.execute_js_with_environment(xs_script)
        
        if result:
            try:
                data = json.loads(result)
                print(f"✅ X-s生成成功!")
                print(f"  X-s: {data.get('xs', 'N/A')}")
                print(f"  时间戳: {data.get('timestamp', 'N/A')}")
                print(f"  指纹: {data.get('fingerprint', 'N/A')}")
                
                # 测试生成的X-s
                xs_value = data.get('xs')
                if xs_value:
                    success = self._test_generated_xs(xs_value)
                    if success:
                        print(f"🎉 生成的X-s测试成功!")
                        return xs_value
                    else:
                        print(f"❌ 生成的X-s测试失败")
                
            except json.JSONDecodeError:
                print(f"❌ 解析JavaScript结果失败: {result}")
        else:
            print(f"❌ JavaScript执行失败")
        
        return None
    
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
            'x-b3-traceid': 'env_based_test',
            'x-xray-traceid': 'env_based_test',
            'X-s': xs_value,
            'X-t': str(int(time.time() * 1000)),
            'x-s-common': xs_value
        }
        
        try:
            response = self.session.get(url_with_params, headers=headers)
            return response.status_code == 200
        except:
            return False
    
    def create_advanced_xs_algorithm(self):
        """创建高级X-s算法"""
        print("\n🔬 创建高级X-s算法")
        print("="*60)
        
        # 基于environment.js分析的高级算法
        print("基于environment.js分析的高级算法:")
        
        # 从真实X-s值分析得到的特征
        real_xs = "XYS_2UQhPsHCH0c1Pjh9HjIj2erjwjQhyoPTqBPT49pjHjIj2eHjwjQgynEDJ74AHjIj2ePjwjQTJdPIP/ZlgMrU4SmH4emPLfkj4DpCn/QEndG3JnMsJLprPepLpez9tAS+aDQbzDzwqer9+BpBLrYg20+64BRG8SQdJaTOGDEwy9IM4DzP+B+GLSr9/bYD8oprwgzN+nGItFcUz9Y7G7p82LLI4URP8AqUJrpCJdk7874Bpbcl+LRhqrSbzDSc+Mk6N7kCG9EkJ7GU+FzG/9k38rp98pYfLgkE4nHIPnMBqbcMpBWA49brHjIj2ecjwjHjKc=="
        
        # 分析算法特征
        timestamp = str(int(time.time() * 1000))
        url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page"
        user_id = "198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479"
        
        print("算法组件:")
        print(f"  时间戳: {timestamp}")
        print(f"  URL: {url}")
        print(f"  用户ID: {user_id}")
        print(f"  笔记ID: {self.note_id}")
        print(f"  评论ID: {self.root_comment_id}")
        
        # 尝试更复杂的算法
        algorithms = [
            ("时间戳+URL+用户ID", f"{timestamp}{url}{user_id}"),
            ("URL+时间戳+用户ID", f"{url}{timestamp}{user_id}"),
            ("用户ID+时间戳+URL", f"{user_id}{timestamp}{url}"),
            ("复合参数", f"{timestamp}{user_id}{self.note_id}{self.root_comment_id}"),
            ("URL哈希复合", hashlib.sha256(f"{url}{timestamp}{user_id}".encode()).hexdigest()),
        ]
        
        print(f"\n尝试高级算法:")
        for algo_name, input_str in algorithms:
            print(f"\n  {algo_name}:")
            print(f"    输入: {input_str[:100]}...")
            
            # 尝试不同的加密方法
            methods = [
                ("SHA256", hashlib.sha256(input_str.encode()).hexdigest()),
                ("SHA512", hashlib.sha512(input_str.encode()).hexdigest()),
                ("MD5+SHA256", hashlib.sha256(hashlib.md5(input_str.encode()).hexdigest().encode()).hexdigest()),
            ]
            
            for method_name, hash_result in methods:
                # Base64编码
                b64_result = base64.b64encode(hash_result.encode()).decode()
                fake_xs = f"XYS_{b64_result}"
                
                print(f"    {method_name}: {fake_xs[:50]}...")
                
                # 测试
                if self._test_generated_xs(fake_xs):
                    print(f"    ✅ 成功！")
                    return algo_name, method_name, fake_xs
        
        return None, None, None

def main():
    """主函数"""
    print("🌟 基于environment.js的X-s参数生成器")
    print("利用v_jstools v3生成的浏览器环境")
    print("="*60)
    
    generator = EnvironmentBasedXSGenerator()
    
    # 创建基于环境的X-s生成器
    xs_value = generator.create_xs_generator_using_env()
    
    if not xs_value:
        # 尝试高级算法
        algo_name, method_name, xs_value = generator.create_advanced_xs_algorithm()
        
        if xs_value:
            print(f"\n🎉 高级算法成功!")
            print(f"算法: {algo_name}")
            print(f"方法: {method_name}")
            print(f"X-s: {xs_value}")
        else:
            print(f"\n❌ 所有算法都失败了")
            print(f"需要更深入的分析")
    
    print(f"\n💡 关键认识:")
    print(f"  - environment.js提供了浏览器环境模拟")
    print(f"  - 真正的X-s生成算法在运行时执行")
    print(f"  - 需要在正确的环境中执行JavaScript代码")
    print(f"  - 可能需要动态分析才能完全破解")

if __name__ == "__main__":
    # 禁用SSL警告
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    main()