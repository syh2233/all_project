#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书x-s参数生成器
基于逆向分析的seccore_signv2函数实现
"""

import json
import time
import base64
import hashlib
from typing import Dict, Any, Optional, Union


class XSGenerator:
    """小红书x-s参数生成器"""
    
    def __init__(self):
        self.version = "1.0.0"
        
    def get_real_url(self, url: str, params: Optional[Dict] = None, params_serializer: Optional[str] = None) -> str:
        """
        模拟getRealUrl函数的行为
        
        Args:
            url: 基础URL
            params: URL参数
            params_serializer: 参数序列化器
            
        Returns:
            处理后的真实URL
        """
        # 根据分析，getRealUrl在这个场景下直接返回原URL
        return url
    
    def seccore_signv2(self, url: str, data: Optional[Dict[str, Any]] = None) -> str:
        """
        核心签名函数 - seccore_signv2的Python实现
        
        Args:
            url: 请求URL
            data: 请求数据
            
        Returns:
            生成的x-s签名
        """
        # 根据调试信息，这里是关键的签名逻辑
        # 需要分析JavaScript代码中的glb['c93b4da3']函数
        
        # 构建签名输入
        if data:
            # 将数据转换为字符串
            data_str = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
        else:
            data_str = ""
        
        # 构建完整输入字符串
        sign_input = f"{url}{data_str}"
        
        # 这里需要实现真正的签名算法
        # 基于JavaScript代码分析，这是一个复杂的加密过程
        # 暂时返回一个占位符，需要进一步分析
        return self._generate_signature(sign_input)
    
    def _generate_signature(self, input_str: str) -> str:
        """
        生成签名的核心逻辑
        
        基于JavaScript代码分析，这是一个混淆的加密算法
        需要还原glb['c93b4da3']函数的逻辑
        """
        # TODO: 实现真正的签名算法
        # 这里需要分析JavaScript代码中的混淆逻辑
        
        # 暂时的占位实现
        # 实际实现需要还原JavaScript中的加密逻辑
        hash_obj = hashlib.md5(input_str.encode('utf-8'))
        signature = base64.b64encode(hash_obj.digest()).decode('utf-8')
        
        # 添加小红书x-s的前缀
        return f"XYS_{signature}"
    
    def generate_xs_headers(self, url: str, params: Optional[Dict] = None, 
                           data: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        """
        生成x-s相关的请求头
        
        Args:
            url: 请求URL
            params: URL参数
            data: 请求数据
            
        Returns:
            包含x-s和x-t的请求头字典
        """
        # 获取真实URL
        real_url = self.get_real_url(url, params)
        
        # 生成x-s签名
        xs = self.seccore_signv2(real_url, data)
        
        # 生成x-t时间戳
        xt = str(int(time.time() * 1000))
        
        return {
            "X-s": xs,
            "X-t": xt
        }
    
    def test_generation(self):
        """测试x-s生成功能"""
        # 使用调试中获取的真实参数进行测试
        test_url = "/api/sec/v1/sbtsource"
        test_data = {
            "callFrom": "web",
            "appId": "xhs-pc-web"
        }
        
        print("🧪 测试x-s生成功能")
        print(f"URL: {test_url}")
        print(f"Data: {test_data}")
        
        # 生成请求头
        headers = self.generate_xs_headers(test_url, data=test_data)
        
        print(f"生成的X-s: {headers['X-s']}")
        print(f"生成的X-t: {headers['X-t']}")
        
        return headers


def main():
    """主函数"""
    generator = XSGenerator()
    
    # 运行测试
    headers = generator.test_generation()
    
    print("\n📋 完整请求头:")
    for key, value in headers.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()