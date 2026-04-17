#!/usr/bin/env python3
"""
小红书X-s-common参数生成算法
基于vendor-dynamic.77f9fe85.js中的xsCommon函数逆向工程
"""

import json
import time
import hashlib
import base64
import urllib.parse
from typing import Dict, Any, Optional


class XiaohongshuXSCommonGenerator:
    """小红书X-s-common参数生成器"""
    
    def __init__(self):
        # 需要X-s-common的URL模式列表
        self.xs_common_urls = [
            r"/api/sns/web/v2/comment/sub/page",
            r"/api/sec/v1/shield/webprofile",
            # 可以添加更多需要X-s-common的URL模式
        ]
        
        # 从JavaScript代码中提取的常量
        self.platform = "xhs-pc-web"
        self.device_type = "PC"
        
        # 随机数种子（可以从页面中提取）
        self.xhs_sign_random = ""
        
        # 设备指纹相关
        self.device_fingerprint = None
        self.fingerprint_suffix = ""
        
    def set_sign_random(self, random_str: str):
        """设置随机数字符串"""
        self.xhs_sign_random = random_str
        
    def set_device_fingerprint(self, fingerprint: str, suffix: str = ""):
        """设置设备指纹"""
        self.device_fingerprint = fingerprint
        self.fingerprint_suffix = suffix
        
    def _url_hash(self, url: str) -> str:
        """
        对应JavaScript中的 p.Pu([l].join(""))
        生成URL的哈希值
        """
        # 使用SHA256哈希，对应JavaScript中的Pu函数
        return hashlib.sha256(url.encode()).hexdigest()[:32]
    
    def _random_sign(self, random_str: str) -> str:
        """
        对应JavaScript中的 p.tb(string)
        生成随机数的签名
        """
        if not random_str:
            return ""
        # 使用MD5哈希，对应JavaScript中的tb函数
        return hashlib.md5(random_str.encode()).hexdigest()
    
    def _utf8_encode(self, text: str) -> list:
        """
        对应JavaScript中的 p.lz
        UTF-8编码为字节数组
        """
        # JavaScript的encodeUtf8函数返回字节数组
        return list(text.encode('utf-8'))
    
    def _base64_encode(self, data: list) -> str:
        """
        对应JavaScript中的 p.xE
        Base64编码字节数组
        """
        # 标准Base64字符表
        base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        
        def triplet_to_base64(triplet):
            """将3字节转换为4个Base64字符"""
            return (base64_chars[triplet >> 18 & 63] + 
                    base64_chars[triplet >> 12 & 63] + 
                    base64_chars[triplet >> 6 & 63] + 
                    base64_chars[63 & triplet])
        
        def encode_chunk(data, start, end):
            """编码数据块"""
            result = []
            for i in range(start, end, 3):
                if i + 2 < len(data):
                    triplet = (data[i] << 16 & 0xff0000) + (data[i + 1] << 8 & 65280) + (255 & data[i + 2])
                    result.append(triplet_to_base64(triplet))
                else:
                    # 处理剩余的字节
                    remaining = len(data) - i
                    if remaining == 1:
                        byte = data[i]
                        result.append(base64_chars[byte >> 2] + base64_chars[byte << 4 & 63] + "==")
                    elif remaining == 2:
                        triplet = (data[i] << 8) + data[i + 1]
                        result.append(base64_chars[triplet >> 10] + base64_chars[triplet >> 4 & 63] + 
                                      base64_chars[triplet << 2 & 63] + "=")
            return "".join(result)
        
        # 分块编码数据
        data_len = len(data)
        chunk_size = 16383  # 与JavaScript实现一致
        remainder = data_len % 3
        result_chunks = []
        
        # 编码完整块
        for i in range(0, data_len - remainder, chunk_size):
            end = min(i + chunk_size, data_len - remainder)
            result_chunks.append(encode_chunk(data, i, end))
        
        # 编码剩余部分
        if remainder == 1:
            byte = data[data_len - 1]
            result_chunks.append(base64_chars[byte >> 2] + base64_chars[byte << 4 & 63] + "==")
        elif remainder == 2:
            triplet = (data[data_len - 2] << 8) + data[data_len - 1]
            result_chunks.append(base64_chars[triplet >> 10] + base64_chars[triplet >> 4 & 63] + 
                                  base64_chars[triplet << 2 & 63] + "=")
        
        return "".join(result_chunks)
    
    def needs_xs_common(self, url: str) -> bool:
        """检查URL是否需要X-s-common"""
        import re
        for pattern in self.xs_common_urls:
            if re.search(pattern, url):
                return True
        return False
    
    def generate_xs_common(self, url: str, include_device_fingerprint: bool = True) -> Optional[str]:
        """
        生成X-s-common参数
        
        Args:
            url: 请求的URL
            include_device_fingerprint: 是否包含设备指纹
            
        Returns:
            X-s-common字符串，如果URL不需要X-s-common则返回None
        """
        if not self.needs_xs_common(url):
            return None
            
        try:
            # 构建基础参数对象
            params = {
                "x0": str(int(time.time() * 1000)),  # 时间戳（毫秒）
                "x1": self.platform,                    # 平台标识
                "x2": self.device_type,                # 设备类型
                "x3": self._url_hash(url),            # URL哈希
                "x4": self._random_sign(self.xhs_sign_random)  # 随机数签名
            }
            
            # 如果需要设备指纹且有设备指纹数据
            if (include_device_fingerprint and 
                self.device_fingerprint is not None):
                
                params["x8"] = self.device_fingerprint
                
                # 生成复合签名 x9
                if self.fingerprint_suffix:
                    composite_str = f"{self.fingerprint_suffix}{self.device_fingerprint}"
                    params["x9"] = self._random_sign(composite_str)
            
            # 序列化为JSON字符串
            json_str = json.dumps(params, separators=(',', ':'), ensure_ascii=False)
            
            # UTF-8编码为字节数组
            utf8_encoded = self._utf8_encode(json_str)
            
            # Base64编码
            xs_common = self._base64_encode(utf8_encoded)
            
            return xs_common
            
        except Exception as e:
            print(f"生成X-s-common失败: {e}")
            return None
    
    def analyze_xs_common(self, xs_common_str: str) -> Dict[str, Any]:
        """
        分析X-s-common字符串的结构
        """
        try:
            # 使用标准Base64解码
            decoded_bytes = base64.b64decode(xs_common_str)
            json_str = decoded_bytes.decode('utf-8')
            
            # 解析JSON
            params = json.loads(json_str)
            
            return {
                "success": True,
                "params": params,
                "analysis": {
                    "timestamp": params.get("x0"),
                    "platform": params.get("x1"),
                    "device_type": params.get("x2"),
                    "url_hash": params.get("x3"),
                    "random_sign": params.get("x4"),
                    "device_fingerprint": params.get("x8"),
                    "composite_sign": params.get("x9")
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "raw_string": xs_common_str
            }


def test_xs_common_generation():
    """测试X-s-common生成"""
    print("🧪 测试X-s-common生成算法")
    print("=" * 50)
    
    # 初始化生成器
    generator = XiaohongshuXSCommonGenerator()
    
    # 设置一些测试数据
    generator.set_sign_random("test_random_123")
    generator.set_device_fingerprint("test_device_fp", "test_suffix")
    
    # 测试URL
    test_url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page?note_id=68a35fc0000000001c009cd9&root_comment_id=68a83b5900000000260052c3&num=10&cursor="
    
    print(f"测试URL: {test_url}")
    
    # 生成X-s-common
    xs_common = generator.generate_xs_common(test_url)
    
    if xs_common:
        print(f"✅ 生成的X-s-common: {xs_common}")
        print(f"长度: {len(xs_common)}")
        
        # 分析生成的结果
        analysis = generator.analyze_xs_common(xs_common)
        if analysis["success"]:
            print("📋 参数分析:")
            for key, value in analysis["analysis"].items():
                print(f"   {key}: {value}")
        else:
            print(f"❌ 分析失败: {analysis['error']}")
    else:
        print("❌ 生成失败")


if __name__ == "__main__":
    test_xs_common_generation()