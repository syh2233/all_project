#!/usr/bin/env python3
"""
完整版XHS签名生成器 - 模拟真实长签名格式
"""

import base64
import hashlib
import json
import struct
import time
import uuid
import random
from typing import Dict, Any, Optional
from urllib.parse import urlencode, urlparse
import re

class CompleteXHSSignatureGenerator:
    """
    完整版XHS签名生成器
    生成接近真实长度的签名
    """
    
    def __init__(self):
        self.version = "XYS"
        self.device_id = self._generate_device_id()
        self.session_id = self._generate_session_id()
        
    def _generate_device_id(self) -> str:
        """生成设备ID"""
        return f"web_{uuid.uuid4().hex}"
    
    def _generate_session_id(self) -> str:
        """生成会话ID"""
        return str(uuid.uuid4())
    
    def _get_browser_fingerprint(self) -> Dict[str, str]:
        """获取浏览器指纹信息"""
        return {
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0",
            "platform": "Win32",
            "language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,en-GB;q=0.6",
            "screen_resolution": "1920x1080",
            "timezone": "Asia/Shanghai",
            "webgl_renderer": "ANGLE (Intel, Intel(R) UHD Graphics 630 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "canvas_fingerprint": self._generate_canvas_fingerprint(),
            "webgl_fingerprint": self._generate_webgl_fingerprint()
        }
    
    def _generate_canvas_fingerprint(self) -> str:
        """生成Canvas指纹"""
        canvas_data = "canvas_fingerprint_data_" + str(random.randint(10000, 99999))
        return hashlib.md5(canvas_data.encode()).hexdigest()
    
    def _generate_webgl_fingerprint(self) -> str:
        """生成WebGL指纹"""
        webgl_data = "webgl_fingerprint_data_" + str(random.randint(10000, 99999))
        return hashlib.sha1(webgl_data.encode()).hexdigest()
    
    def _extract_domain_info(self, url: str) -> Dict[str, str]:
        """提取域名信息"""
        parsed = urlparse(url)
        return {
            "domain": parsed.netloc,
            "origin": f"{parsed.scheme}://{parsed.netloc}",
            "path": parsed.path
        }
    
    def _generate_context_data(self, path: str, params: Dict[str, Any], url: str = "https://edith.xiaohongshu.com") -> Dict[str, Any]:
        """生成完整的上下文数据"""
        timestamp = int(time.time() * 1000)
        browser_fingerprint = self._get_browser_fingerprint()
        domain_info = self._extract_domain_info(url)
        
        # 生成随机盐值
        salt = ''.join([str(random.randint(0, 9)) for _ in range(16)])
        
        context = {
            # 版本和时间信息
            "version": self.version,
            "timestamp": timestamp,
            "salt": salt,
            
            # 设备和会话信息
            "device_id": self.device_id,
            "session_id": self.session_id,
            
            # 浏览器指纹
            "browser_fingerprint": browser_fingerprint,
            
            # 请求信息
            "request": {
                "path": path,
                "params": params,
                "domain": domain_info["domain"],
                "origin": domain_info["origin"]
            },
            
            # 环境信息
            "environment": {
                "web_build": "4.79.0",
                "app_id": "xhs-pc-web",
                "call_from": "web"
            },
            
            # 安全信息
            "security": {
                "xsec_token": params.get("xsec_token", ""),
                "cookie_session": "present" if "web_session" in str(params) else "absent"
            }
        }
        
        return context
    
    def _generate_signature_payload(self, context: Dict[str, Any]) -> bytes:
        """生成签名载荷"""
        # 序列化上下文数据
        context_json = json.dumps(context, separators=(',', ':'), sort_keys=True)
        
        # 生成核心哈希
        core_hash = hashlib.sha256(context_json.encode()).digest()
        
        # 生成时间戳哈希
        timestamp = context["timestamp"]
        time_hash = hashlib.md5(str(timestamp).encode()).digest()
        
        # 生成设备哈希
        device_hash = hashlib.sha1(context["device_id"].encode()).digest()
        
        # 生成会话哈希
        session_hash = hashlib.sha1(context["session_id"].encode()).digest()
        
        # 组合所有数据
        payload_structure = struct.pack(
            '!B',  # 版本字节 (1 byte)
            0x02,  # 版本号
        )
        
        payload_structure += core_hash  # 核心哈希 (32 bytes)
        payload_structure += time_hash  # 时间哈希 (16 bytes) 
        payload_structure += device_hash  # 设备哈希 (20 bytes)
        payload_structure += session_hash  # 会话哈希 (20 bytes)
        
        # 添加随机填充以达到真实签名长度
        padding_length = 241 - len(payload_structure)  # 真实签名解码后241字节
        if padding_length > 0:
            padding = bytes([random.randint(0, 255) for _ in range(padding_length)])
            payload_structure += padding
        
        return payload_structure
    
    def generate_complete_signature(self, path: str, params: Dict[str, Any], url: str = "https://edith.xiaohongshu.com") -> str:
        """
        生成完整的X-S签名
        
        Args:
            path: API路径
            params: 请求参数
            url: 完整URL
            
        Returns:
            完整的X-S签名
        """
        # 生成上下文数据
        context = self._generate_context_data(path, params, url)
        
        # 生成签名载荷
        payload = self._generate_signature_payload(context)
        
        # Base64编码
        signature_base64 = base64.b64encode(payload).decode()
        
        # 添加版本前缀
        complete_signature = f"{self.version}_{signature_base64}"
        
        return complete_signature
    
    def generate_simple_signature(self, path: str, params: Dict[str, Any]) -> str:
        """
        生成简化版签名（原版本）
        """
        param_str = json.dumps(params, separators=(',', ':'), sort_keys=True)
        input_str = f"{path}{param_str}"
        timestamp = int(time.time() * 1000)
        input_with_time = f"{input_str}{timestamp}"
        
        hash1 = hashlib.md5(input_with_time.encode()).digest()
        hash2 = hashlib.sha1(hash1).digest()
        hash3 = hashlib.sha256(hash2).digest()
        
        signature = base64.b64encode(hash3).decode()
        signature = re.sub(r'[^a-zA-Z0-9]', '', signature)
        
        return signature[:32]

def main():
    """测试完整版签名生成器"""
    generator = CompleteXHSSignatureGenerator()
    
    # 测试参数
    path = "/api/sns/web/v2/comment/page"
    params = {
        "note_id": "68a35fc0000000001c009cd9",
        "cursor": "",
        "top_comment_id": "",
        "image_formats": "jpg,webp,avif",
        "xsec_token": "ABMARfqKuxx76hZj-CQH0D9AIHxh8oCmV_RTOxyE_DIpI="
    }
    
    print("=== XHS签名生成器对比测试 ===\n")
    
    # 生成完整签名
    complete_sig = generator.generate_complete_signature(path, params)
    print(f"完整签名长度: {len(complete_sig)}")
    print(f"完整签名: {complete_sig[:100]}...")
    
    # 生成简化签名
    simple_sig = generator.generate_simple_signature(path, params)
    print(f"\n简化签名长度: {len(simple_sig)}")
    print(f"简化签名: {simple_sig}")
    
    # 分析签名结构
    if '_' in complete_sig:
        prefix, base64_part = complete_sig.split('_', 1)
        print(f"\n签名结构分析:")
        print(f"前缀: {prefix}")
        print(f"Base64部分长度: {len(base64_part)}")
        
        try:
            decoded = base64.b64decode(base64_part)
            print(f"解码后长度: {len(decoded)} 字节")
            print(f"解码后内容 (hex): {decoded.hex()[:50]}...")
        except Exception as e:
            print(f"Base64解码失败: {e}")

if __name__ == "__main__":
    main()