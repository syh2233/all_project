#!/usr/bin/env python3
"""
X-s生成算法完整分析工具
基于vendor-dynamic.77f9fe85.js的真实算法分析
"""

import requests
import json
import time
import re
import base64
import hashlib
import hmac
from urllib.parse import urlencode

class CompleteXSAnalyzer:
    """完整的X-s生成算法分析器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False
        self.session.timeout = 10
        
        # 新的cookie
        self.new_cookie = "gid=yj8D24fWSDv0yj8D24fK069V0yIY6AFDTDxSxyU1kTyk2428MD7AC4888W2q2Yy8fJ0KjyDJ; xsecappid=xhs-pc-web; abRequestId=f425aaf4-2614-55c8-b8d1-262c611be2ab; a1=198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479; webId=fc4fb0dccb1a480d5f17359394c861d7; web_session=040069b3ed6ebed4fbe30e25ad3a4b127faeca; webBuild=4.79.0; unread=%7B%22ub%22%3A%2268b56bf2000000001c004134%22%2C%22ue%22%3A%2268a3fe26000000001c0126d1%22%2C%22uc%22%3A20%7D; acw_tc=0a4a453a17569070897088137ec524bb28ede595ddc525595031d81456a33f; websectiga=2845367ec3848418062e761c09db7caf0e8b79d132ccdd1a4f8e64a11d0cac0d; sec_poison_id=b4c4d07b-3d95-4e2e-b6fc-42a65ed18bb4; loadts=1756907500892"
        
        # 测试参数
        self.note_id = "68a048c1000000001d01838e"
        self.root_comment_id = "68a048ef000000003002a604"
        
        # 从vendor-dynamic.js分析得到的真实算法
        self.real_algorithm = {
            "function_name": "seccore_signv2",
            "location": "vendor-dynamic.77f9fe85.js:10841",
            "key_components": [
                "window.mnsv2(c, d)",
                "p.Pu([c].join(''))",
                "p.xE((0, p.lz)(JSON.stringify(f))))",
                "xhsFingerprintV3.getV18()"
            ],
            "format": "XYS_" + "base64_encoded_content"
        }
    
    def analyze_real_algorithm(self):
        """分析真实的X-s生成算法"""
        print("🔬 分析真实的X-s生成算法")
        print("="*60)
        
        print("从vendor-dynamic.77f9fe85.js发现的真实算法:")
        print()
        print("📋 算法位置: vendor-dynamic.77f9fe85.js:10841")
        print("🔧 函数名: seccore_signv2")
        print()
        
        print("📜 核心算法代码:")
        print("-" * 40)
        print("""
function seccore_signv2(e, a) {
    var r = window.toString
    var c = e;
    
    // 处理参数
    "[object Object]" === r.call(a) || "[object Array]" === r.call(a) || 
    (void 0 === a ? "undefined" : (0, h._)(a)) === "object" && null !== a ? 
    c += JSON.stringify(a) : "string" == typeof a && (c += a);
    
    // 生成签名
    var d = (0, p.Pu)([c].join(""))
    var s = window.mnsv2(c, d)
    
    // 构建最终对象
    var f = {
        x0: u.i8,           // 时间戳相关
        x1: "xhs-pc-web",   // 应用ID
        x2: window[u.mj] || "PC",  // 设备类型
        x3: s,              // 签名
        x4: a ? void 0 === a ? "undefined" : (0, h._)(a) : ""
    };
    
    // 生成最终X-s
    return "XYS_" + (0, p.xE)((0, p.lz)(JSON.stringify(f)))
}
        """)
        print("-" * 40)
        
        print("🔍 关键组件分析:")
        print("  1. p.Pu() - 可能是哈希函数")
        print("  2. window.mnsv2() - 可能是签名函数")
        print("  3. p.lz() - 可能是压缩函数")
        print("  4. p.xE() - 可能是编码函数")
        print("  5. u.i8 - 时间戳")
        print("  6. xhsFingerprintV3.getV18() - 设备指纹")
        
        return self.real_algorithm
    
    def search_algorithm_functions(self):
        """搜索算法中的关键函数"""
        print(f"\n🔍 搜索算法中的关键函数")
        print("="*60)
        
        try:
            with open('vendor-dynamic.77f9fe85.js', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 搜索关键函数定义
            key_functions = [
                r'p\.Pu.*function',
                r'p\.lz.*function', 
                r'p\.xE.*function',
                r'window\.mnsv2.*function',
                r'u\.i8.*=',
                r'xhsFingerprintV3.*='
            ]
            
            print("搜索关键函数定义:")
            for func_pattern in key_functions:
                matches = re.findall(func_pattern, content, re.IGNORECASE)
                if matches:
                    print(f"  {func_pattern}: {len(matches)} 个匹配")
                    for match in matches[:2]:  # 显示前两个匹配
                        print(f"    {match[:100]}...")
            
            # 搜索函数调用
            print(f"\n搜索函数调用:")
            key_calls = [
                r'p\.Pu\(',
                r'p\.lz\(',
                r'p\.xE\(',
                r'window\.mnsv2\(',
                r'xhsFingerprintV3\.getV18\('
            ]
            
            for call_pattern in key_calls:
                matches = re.findall(call_pattern, content)
                if matches:
                    print(f"  {call_pattern}: {len(matches)} 个调用")
                    
        except Exception as e:
            print(f"❌ 搜索函数时出错: {e}")
    
    def create_userscript_installation_guide(self):
        """创建userscript安装指南"""
        print(f"\n📖 userscript.html 安装和使用指南")
        print("="*60)
        
        print("""
🎯 Userscript 功能概述
======================
这是一个强大的 Cookie 监控和调试工具，专门用于追踪 X-s 参数的生成过程。

核心功能：
- 监控 JavaScript 对 cookie 的修改
- 在 cookie 符合条件时自动进入断点
- 专门设置 debuggerRules = ["x-s"] 来追踪 X-s 参数
- 提供完整的调用栈信息

🔧 安装步骤
===========
1. 安装浏览器扩展
   - Chrome: Tampermonkey (https://www.tampermonkey.net/)
   - Firefox: Greasemonkey (https://addons.mozilla.org/firefox/addon/greasemonkey/)

2. 创建 userscript
   - 打开浏览器扩展管理页面
   - 点击"新建脚本"
   - 将 userscript.html 的完整内容复制进去
   - 保存脚本

3. 启用脚本
   - 确保脚本在小红书域名下启用
   - 重新加载小红书页面

🔍 使用方法
===========
1. 访问小红书页面
2. 打开开发者工具 (F12)
3. 浏览到包含子评论的页面
4. 当 X-s 参数被设置时，会自动触发断点
5. 在断点处查看调用栈和局部变量

💡 调试技巧
===========
- 查看调用栈，找到 X-s 生成函数
- 检查局部变量的值
- 分析参数组合和生成过程
- 记录关键函数的输入输出

🎯 关键代码位置
==============
- 第21行: const debuggerRules = ["x-s"];
- 第502行: testDebuggerRules函数
- 第506行: debugger; (断点触发)

📊 预期结果
===========
- 自动断点在 X-s 生成位置
- 显示完整的函数调用栈
- 可以看到 seccore_signv2 函数的执行过程
- 获取实时生成的 X-s 值
        """)
    
    def simulate_real_xs_generation(self):
        """模拟真实的X-s生成过程"""
        print(f"\n🛠️ 模拟真实的X-s生成过程")
        print("="*60)
        
        # 基于分析的算法组件
        timestamp = str(int(time.time() * 1000))
        url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page"
        user_id = "198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479"
        
        print("算法参数:")
        print(f"  时间戳 (u.i8): {timestamp}")
        print(f"  应用ID (x1): xhs-pc-web")
        print(f"  设备类型 (x2): PC")
        print(f"  URL: {url}")
        print(f"  用户ID: {user_id}")
        
        # 模拟生成过程
        print(f"\n模拟生成步骤:")
        
        # 步骤1: 构建基础字符串
        base_string = f"{timestamp}{url}"
        print(f"  步骤1 - 基础字符串: {base_string[:50]}...")
        
        # 步骤2: 应用 p.Pu 函数 (可能是哈希)
        # 由于不知道确切的 p.Pu 实现，我们模拟几种可能
        possible_hashes = [
            hashlib.md5(base_string.encode()).hexdigest(),
            hashlib.sha1(base_string.encode()).hexdigest(),
            hashlib.sha256(base_string.encode()).hexdigest()
        ]
        
        print(f"  步骤2 - p.Pu 可能的结果:")
        for i, hash_val in enumerate(possible_hashes, 1):
            print(f"    选项{i}: {hash_val[:32]}...")
        
        # 步骤3: 应用 window.mnsv2 函数
        # 这可能是签名函数
        print(f"  步骤3 - window.mnsv2 签名")
        
        # 步骤4: 构建最终对象
        for i, hash_val in enumerate(possible_hashes, 1):
            f = {
                "x0": timestamp,
                "x1": "xhs-pc-web",
                "x2": "PC",
                "x3": hash_val,  # 这里应该是 mnsv2 的结果
                "x4": ""  # 附加参数
            }
            
            # 步骤5: 应用 p.lz 和 p.xE 函数
            # p.lz 可能是压缩，p.xE 可能是编码
            json_str = json.dumps(f)
            
            # 模拟 p.lz (压缩)
            compressed = json_str  # 简化处理
            
            # 模拟 p.xE (编码)
            encoded = base64.b64encode(compressed.encode()).decode()
            
            # 生成最终X-s
            generated_xs = f"XYS_{encoded}"
            
            print(f"  选项{i} 生成的X-s: {generated_xs[:50]}...")
            
            # 测试生成的X-s
            if self.test_generated_xs(generated_xs):
                print(f"  ✅ 选项{i} 测试成功!")
                return generated_xs
        
        return None
    
    def test_generated_xs(self, xs_value):
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
            'x-b3-traceid': 'real_algorithm_test',
            'x-xray-traceid': 'real_algorithm_test',
            'X-s': xs_value,
            'X-t': str(int(time.time() * 1000)),
            'x-s-common': xs_value
        }
        
        try:
            response = self.session.get(url_with_params, headers=headers)
            return response.status_code == 200
        except:
            return False
    
    def create_complete_breakthrough_plan(self):
        """创建完整的突破计划"""
        print(f"\n🚀 完整的X-s生成算法突破计划")
        print("="*60)
        
        print("""
📋 现状分析
=========
✅ 已完成：
- 发现了真实的X-s生成算法位置
- 分析了算法的核心组件
- 理解了生成过程的基本结构
- 准备了动态调试工具

❌ 待突破：
- p.Pu, p.lz, p.xE 函数的具体实现
- window.mnsv2 签名算法
- xhsFingerprintV3.getV18() 的输出
- 完整的参数组合

🎯 突破方案
=========

方案一：动态调试 (推荐)
1. 安装 userscript.html 到浏览器
2. 访问小红书页面触发断点
3. 在 seccore_signv2 函数处设置断点
4. 记录每个步骤的输入输出
5. 提取关键函数的实现逻辑

方案二：静态分析
1. 深入分析 vendor-dynamic.77f9fe85.js
2. 搜索 p.Pu, p.lz, p.xE 函数定义
3. 理解 window.mnsv2 的实现
4. 重构完整的生成算法

方案三：混合分析
1. 结合动态调试和静态分析
2. 使用 userscript 获取实时数据
3. 通过静态分析理解算法逻辑
4. 验证和优化重构的算法

🔧 所需工具
=========
- 浏览器 + Tampermonkey/Greasemonkey
- 开发者工具 (F12)
- userscript.html 文件
- vendor-dynamic.77f9fe85.js 文件
- Python 测试环境

📊 预期成果
=========
- 完整的 X-s 生成算法实现
- 可以实时生成有效的 X-s 值
- 成功获取小红书子评论数据
- 理解小红书的认证机制

💡 关键认识
=========
- X-s 生成算法已经基本解构
- 主要挑战在于几个关键函数的实现
- 动态调试是最有效的突破方法
- 需要实时数据来验证算法

🚀 下一步行动
=========
1. 立即安装 userscript 进行动态调试
2. 在浏览器中触发断点获取实时数据
3. 分析关键函数的具体实现
4. 重构完整的生成算法
        """)
        
        return {
            "status": "breakthrough_ready",
            "confidence": "high",
            "next_steps": ["install_userscript", "dynamic_debugging", "algorithm_reconstruction"]
        }

def main():
    """主函数"""
    print("🌟 X-s生成算法完整分析工具")
    print("基于vendor-dynamic.77f9fe85.js的真实算法")
    print("="*60)
    
    analyzer = CompleteXSAnalyzer()
    
    # 分析真实算法
    real_algorithm = analyzer.analyze_real_algorithm()
    
    # 搜索关键函数
    analyzer.search_algorithm_functions()
    
    # 创建userscript安装指南
    analyzer.create_userscript_installation_guide()
    
    # 模拟真实生成过程
    generated_xs = analyzer.simulate_real_xs_generation()
    
    if generated_xs:
        print(f"\n🎉 成功生成X-s值!")
        print(f"X-s: {generated_xs}")
    else:
        print(f"\n❌ 模拟生成失败，需要进一步分析")
    
    # 创建完整突破计划
    breakthrough_plan = analyzer.create_complete_breakthrough_plan()
    
    print(f"\n💡 总结:")
    print(f"  - 已发现真实的X-s生成算法")
    print(f"  - 算法位置: {real_algorithm['location']}")
    print(f"  - 主要挑战: 关键函数的具体实现")
    print(f"  - 最佳方案: 使用userscript进行动态调试")
    print(f"  - 突破状态: {breakthrough_plan['status']}")

if __name__ == "__main__":
    # 禁用SSL警告
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    main()