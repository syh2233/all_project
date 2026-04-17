#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
核心签名算法分析器
专门分析x-s参数生成的核心逻辑
"""

import re
import json
import base64
import hashlib
from typing import Dict, List, Optional


class CoreAnalyzer:
    """核心算法分析器"""
    
    def __init__(self, js_file_path: str):
        self.js_file_path = js_file_path
        self.js_content = self._load_js_file()
        
    def _load_js_file(self) -> str:
        """加载JavaScript文件的关键部分"""
        try:
            with open(self.js_file_path, 'r', encoding='utf-8') as f:
                # 只读取前10000个字符，包含关键函数
                content = f.read(10000)
            return content
        except Exception as e:
            print(f"❌ 加载文件失败: {e}")
            return ""
    
    def extract_key_functions(self) -> Dict[str, str]:
        """提取关键函数代码片段"""
        functions = {}
        
        # 查找seccore_signv2函数
        seccore_pattern = r"function seccore_signv2\([^}]*\{[^}]*\}"
        seccore_matches = re.findall(seccore_pattern, self.js_content, re.DOTALL)
        if seccore_matches:
            functions["seccore_signv2"] = seccore_matches[0]
        
        # 查找c93b4da3函数
        c93b_pattern = r"glb\['c93b4da3'\]=function\([^}]*\{[^}]*\}"
        c93b_matches = re.findall(c93b_pattern, self.js_content, re.DOTALL)
        if c93b_matches:
            functions["c93b4da3"] = c93b_matches[0]
        
        return functions
    
    def analyze_sign_pattern(self) -> Dict[str, any]:
        """分析签名模式"""
        # 查找x-s参数的特征
        xs_pattern = r"XYS_[A-Za-z0-9+/=]+"
        xs_matches = re.findall(xs_pattern, self.js_content)
        
        # 查找Base64编码的特征
        base64_pattern = r"[A-Za-z0-9+/=]{20,}"
        base64_matches = re.findall(base64_pattern, self.js_content)
        
        # 查找时间戳相关
        timestamp_pattern = r"\+new Date|Date\.now\(\)|getTime\(\)"
        timestamp_matches = re.findall(timestamp_pattern, self.js_content)
        
        return {
            "xs_signatures_found": len(xs_matches),
            "base64_strings_found": len(base64_matches),
            "timestamp_functions": len(timestamp_matches),
            "sample_xs": xs_matches[:3] if xs_matches else [],
            "sample_base64": base64_matches[:3] if base64_matches else []
        }
    
    def generate_xs_implementation(self) -> str:
        """生成x-s参数的Python实现"""
        implementation = '''
def generate_xs_signature(url: str, data: dict = None) -> str:
    """
    基于分析结果生成x-s签名
    
    Args:
        url: 请求URL
        data: 请求数据
        
    Returns:
        x-s签名字符串
    """
    import json
    import time
    import base64
    import hashlib
    
    # 1. 构建输入字符串
    if data:
        data_str = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
    else:
        data_str = ""
    
    input_str = f"{url}{data_str}"
    
    # 2. 生成签名（这里需要实现真正的算法）
    # 基于分析，这是一个复杂的加密过程
    # 暂时使用MD5作为示例
    hash_obj = hashlib.md5(input_str.encode('utf-8'))
    signature = base64.b64encode(hash_obj.digest()).decode('utf-8')
    
    # 3. 添加小红书前缀
    return f"XYS_{signature}"
'''
        return implementation
    
    def create_test_case(self) -> str:
        """创建测试用例"""
        test_case = '''
def test_xs_generation():
    """测试x-s生成功能"""
    # 使用调试中获取的真实参数
    test_url = "/api/sec/v1/sbtsource"
    test_data = {
        "callFrom": "web", 
        "appId": "xhs-pc-web"
    }
    
    print("🧪 测试x-s生成")
    print(f"URL: {test_url}")
    print(f"Data: {test_data}")
    
    # 生成签名
    xs = generate_xs_signature(test_url, test_data)
    print(f"生成的X-s: {xs}")
    
    # 生成时间戳
    xt = str(int(time.time() * 1000))
    print(f"生成的X-t: {xt}")
    
    return {"X-s": xs, "X-t": xt}
'''
        return test_case
    
    def run_analysis(self):
        """运行分析"""
        print("🔍 分析小红书x-s签名算法...")
        
        # 分析签名模式
        patterns = self.analyze_sign_pattern()
        print(f"📊 签名模式分析:")
        for key, value in patterns.items():
            print(f"  {key}: {value}")
        
        # 提取关键函数
        functions = self.extract_key_functions()
        print(f"🔑 关键函数:")
        for name, code in functions.items():
            print(f"  {name}: {len(code)} 字符")
        
        # 生成实现
        print(f"💻 Python实现:")
        print(self.generate_xs_implementation())
        
        # 生成测试用例
        print(f"🧪 测试用例:")
        print(self.create_test_case())
        
        # 保存分析结果
        result = {
            "patterns": patterns,
            "functions": {k: len(v) for k, v in functions.items()},
            "implementation": self.generate_xs_implementation(),
            "test_case": self.create_test_case()
        }
        
        with open("analysis_result.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print("✅ 分析结果已保存到 analysis_result.json")


def main():
    """主函数"""
    js_file_path = "/mnt/c/手动D/接单/all_project/red_note_scrapy_1/browser_files/vendor-dynamic.77f9fe85.js"
    
    analyzer = CoreAnalyzer(js_file_path)
    analyzer.run_analysis()


if __name__ == "__main__":
    main()