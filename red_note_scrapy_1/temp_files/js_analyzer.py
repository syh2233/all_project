#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JavaScript混淆代码分析器
专门用于分析vendor-dynamic.77f9fe85.js中的混淆逻辑
"""

import re
import json
from typing import Dict, List, Tuple, Optional


class JSAnalyzer:
    """JavaScript混淆代码分析器"""
    
    def __init__(self, js_file_path: str):
        self.js_file_path = js_file_path
        self.js_content = ""
        self.load_js_file()
        
    def load_js_file(self):
        """加载JavaScript文件"""
        try:
            with open(self.js_file_path, 'r', encoding='utf-8') as f:
                self.js_content = f.read()
            print(f"✅ 成功加载JavaScript文件: {self.js_file_path}")
        except Exception as e:
            print(f"❌ 加载JavaScript文件失败: {e}")
            
    def extract_c93b4da3_function(self) -> Optional[str]:
        """
        提取glb['c93b4da3']函数的代码
        
        Returns:
            函数代码字符串
        """
        # 查找函数定义
        pattern = r"glb\['c93b4da3'\]=function\([^}]*\{[^}]*\}"
        matches = re.findall(pattern, self.js_content, re.DOTALL)
        
        if matches:
            return matches[0]
        return None
    
    def extract_seccore_signv2(self) -> Optional[str]:
        """
        提取seccore_signv2函数代码
        
        Returns:
            函数代码字符串
        """
        pattern = r"function seccore_signv2\([^}]*\{[^}]*\}"
        matches = re.findall(pattern, self.js_content, re.DOTALL)
        
        if matches:
            return matches[0]
        return None
    
    def extract_obfuscated_arrays(self) -> Dict[str, List[str]]:
        """
        提取混淆的数组定义
        
        Returns:
            混淆数组字典
        """
        arrays = {}
        
        # 查找数组定义模式
        array_pattern = r"var _0x[a-f0-9]+=\[([^\]]+)\];"
        matches = re.findall(array_pattern, self.js_content)
        
        for i, match in enumerate(matches):
            # 提取数组元素
            elements = re.findall(r"'([^']*)'", match)
            arrays[f"array_{i}"] = elements
            
        return arrays
    
    def extract_string_mapping(self) -> Dict[str, str]:
        """
        提取字符串映射关系
        
        Returns:
            字符串映射字典
        """
        mapping = {}
        
        # 查找字符串映射模式
        pattern = r"var _0x([a-f0-9]+)=function\(_0x([a-f0-9]+),_0x([a-f0-9]+)\)\{_0x([a-f0-9]+)=_0x([a-f0-9]+)-0x0;var _0x([a-f0-9]+)=_0x([a-f0-9]+)\[_0x([a-f0-9]+)\];return _0x([a-f0-9]+);\}"
        
        # 这个模式比较复杂，需要更精确的正则表达式
        # 这里先提供一个基础版本
        
        return mapping
    
    def analyze_function_flow(self) -> List[str]:
        """
        分析函数执行流程
        
        Returns:
            执行步骤列表
        """
        steps = []
        
        # 查找函数调用链
        call_pattern = r"_0x([a-f0-9]+)\("
        calls = re.findall(call_pattern, self.js_content)
        
        unique_calls = list(set(calls))
        steps.append(f"发现 {len(unique_calls)} 个不同的函数调用")
        
        return steps
    
    def generate_pseudo_code(self) -> str:
        """
        生成伪代码
        
        Returns:
            伪代码字符串
        """
        pseudo_code = """
// 小红书x-s生成算法伪代码
function generate_xs(url, data) {
    // 1. 构建输入字符串
    var input = url + JSON.stringify(data);
    
    // 2. 执行混淆的加密算法
    var result = glb['c93b4da3'](input);
    
    // 3. 添加前缀
    return "XYS_" + result;
}
"""
        return pseudo_code
    
    def analyze_sign_algorithm(self) -> Dict[str, any]:
        """
        分析签名算法特征
        
        Returns:
            算法特征字典
        """
        features = {
            "function_count": len(re.findall(r"function\s+\w+", self.js_content)),
            "array_count": len(re.findall(r"\[[^\]]+\]", self.js_content)),
            "hex_variables": len(re.findall(r"_0x[a-f0-9]+", self.js_content)),
            "string_literals": len(re.findall(r"'[^']*'", self.js_content)),
            "function_calls": len(re.findall(r"\w+\(", self.js_content))
        }
        
        return features
    
    def export_analysis_report(self, output_file: str = "analysis_report.json"):
        """
        导出分析报告
        
        Args:
            output_file: 输出文件名
        """
        report = {
            "file_path": self.js_file_path,
            "file_size": len(self.js_content),
            "features": self.analyze_sign_algorithm(),
            "pseudo_code": self.generate_pseudo_code(),
            "arrays": self.extract_obfuscated_arrays(),
            "function_flow": self.analyze_function_flow()
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"📊 分析报告已导出到: {output_file}")
        
    def run_analysis(self):
        """运行完整分析"""
        print("🔍 开始分析JavaScript混淆代码...")
        
        # 分析基本特征
        features = self.analyze_sign_algorithm()
        print(f"📈 代码特征:")
        for key, value in features.items():
            print(f"  {key}: {value}")
        
        # 提取关键函数
        c93b4da3_func = self.extract_c93b4da3_function()
        if c93b4da3_func:
            print(f"✅ 找到c93b4da3函数")
            print(f"   长度: {len(c93b4da3_func)} 字符")
        
        seccore_func = self.extract_seccore_signv2()
        if seccore_func:
            print(f"✅ 找到seccore_signv2函数")
            print(f"   长度: {len(seccore_func)} 字符")
        
        # 提取混淆数组
        arrays = self.extract_obfuscated_arrays()
        print(f"📦 找到 {len(arrays)} 个混淆数组")
        
        # 生成伪代码
        print(f"💡 生成伪代码:")
        print(self.generate_pseudo_code())
        
        # 导出报告
        self.export_analysis_report()


def main():
    """主函数"""
    js_file_path = "/mnt/c/手动D/接单/all_project/red_note_scrapy_1/browser_files/vendor-dynamic.77f9fe85.js"
    
    analyzer = JSAnalyzer(js_file_path)
    analyzer.run_analysis()


if __name__ == "__main__":
    main()