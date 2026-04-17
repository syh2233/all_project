#!/usr/bin/env python3
"""
真实环境信息增强版XHS签名生成器
模拟真实浏览器环境，避免设备环境检测问题
"""

import base64
import hashlib
import json
import struct
import time
import uuid
import random
import platform
import socket
import re
from typing import Dict, Any, Optional
from urllib.parse import urlencode, urlparse
import sys
import os

class RealisticXHSSignatureGenerator:
    """
    真实环境信息增强版XHS签名生成器
    模拟真实浏览器环境，包含完整的设备指纹和会话信息
    """
    
    def __init__(self):
        self.version = "XYS"
        self.device_id = self._generate_realistic_device_id()
        self.session_id = self._generate_realistic_session_id()
        self.web_id = self._generate_web_id()
        self.trace_id = self._generate_trace_id()
        self.request_id = self._generate_request_id()
        
        # 真实的浏览器环境信息
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0"
        self.screen_info = self._get_screen_info()
        self.timezone_info = self._get_timezone_info()
        self.language_info = self._get_language_info()
        
        # 硬件信息
        self.hardware_info = self._get_hardware_info()
        self.webgl_info = self._get_webgl_info()
        self.canvas_info = self._get_canvas_info()
        
        # 网络信息
        self.network_info = self._get_network_info()
        
    def _generate_realistic_device_id(self) -> str:
        """生成真实的设备ID"""
        # 模拟真实设备ID格式
        timestamp = int(time.time() * 1000)
        random_part = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        return f"fc{timestamp % 1000000:06d}ccb1a480d5f17359394c861d{random_part}"
    
    def _generate_realistic_session_id(self) -> str:
        """生成真实的会话ID"""
        # 模拟真实会话ID格式
        timestamp = int(time.time() * 1000)
        random_part = ''.join([random.choice('0123456789abcdef') for _ in range(12)])
        return f"040069b3ed6ebed4fbe38d058d3a4bf7c6f8{timestamp % 10000:04d}{random_part}"
    
    def _generate_web_id(self) -> str:
        """生成Web ID"""
        return f"fc4fb0dccb1a480d5f17359394c861d7"
    
    def _generate_trace_id(self) -> str:
        """生成追踪ID"""
        return ''.join([random.choice('0123456789abcdef') for _ in range(32)])
    
    def _generate_request_id(self) -> str:
        """生成请求ID"""
        return f"{uuid.uuid4()}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
    
    def _get_screen_info(self) -> Dict[str, Any]:
        """获取屏幕信息"""
        return {
            "resolution": "1920x1080",
            "color_depth": 24,
            "pixel_ratio": 1.0,
            "available_screen": "1920x1040",
            "screen_orientation": "landscape-primary"
        }
    
    def _get_timezone_info(self) -> Dict[str, Any]:
        """获取时区信息"""
        return {
            "timezone": "Asia/Shanghai",
            "timezone_offset": 480,  # UTC+8
            "timezone_name": "中国标准时间",
            "dst": False
        }
    
    def _get_language_info(self) -> Dict[str, Any]:
        """获取语言信息"""
        return {
            "languages": ["zh-CN", "zh", "en-US", "en"],
            "preferred_language": "zh-CN",
            "accept_language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,en-GB;q=0.6"
        }
    
    def _get_hardware_info(self) -> Dict[str, Any]:
        """获取硬件信息"""
        return {
            "platform": "Win32",
            "architecture": "x86_64",
            "device_memory": 8,
            "hardware_concurrency": 8,
            "cpu_class": "Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz",
            "gpu_vendor": "Intel",
            "gpu_renderer": "Intel(R) UHD Graphics 630"
        }
    
    def _get_webgl_info(self) -> Dict[str, Any]:
        """获取WebGL信息"""
        return {
            "webgl_vendor": "Google Inc. (Intel)",
            "webgl_renderer": "ANGLE (Intel, Intel(R) UHD Graphics 630 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "webgl_version": "WebGL 2.0 (OpenGL ES 3.0 Chromium)",
            "max_texture_size": 16384,
            "max_viewport_dims": [16384, 16384],
            "webgl_parameters": {
                "MAX_TEXTURE_SIZE": 16384,
                "MAX_CUBE_MAP_TEXTURE_SIZE": 16384,
                "MAX_RENDERBUFFER_SIZE": 16384
            }
        }
    
    def _get_canvas_info(self) -> Dict[str, Any]:
        """获取Canvas信息"""
        # 生成真实的Canvas指纹
        canvas_data = "canvas_fingerprint_" + self.device_id + str(int(time.time()))
        return {
            "canvas_fingerprint": hashlib.md5(canvas_data.encode()).hexdigest(),
            "canvas_hash": hashlib.sha256(canvas_data.encode()).hexdigest()[:16],
            "is_canvas_poisoned": False,
            "canvas_noise_level": 0.1
        }
    
    def _get_network_info(self) -> Dict[str, Any]:
        """获取网络信息"""
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
        except:
            hostname = "DESKTOP-UNKNOWN"
            local_ip = "192.168.1.100"
        
        return {
            "hostname": hostname,
            "local_ip": local_ip,
            "connection_type": "wifi",
            "downlink": 10.0,
            "rtt": 100,
            "effective_connection_type": "4g"
        }
    
    def _get_cookie_info(self) -> Dict[str, Any]:
        """获取Cookie信息"""
        return {
            "gid": f"g{random.randint(10000, 99999)}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{''.join([random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz') for _ in range(8)])}",
            "a1": f"198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000{random.randint(60000, 99999)}",
            "web_session": self.session_id,
            "web_build": "4.79.0",
            "webId": self.web_id,
            "xsecappid": "xhs-pc-web"
        }
    
    def _get_security_info(self) -> Dict[str, Any]:
        """获取安全信息"""
        return {
            "xsec_token_present": True,
            "cookie_integrity": "valid",
            "session_age": int(time.time() * 1000) - int(self.session_id[-13:], 16) % 1000000,
            "request_validity": True,
            "anti_spam_passed": True,
            "captcha_passed": True
        }
    
    def _get_behavior_info(self) -> Dict[str, Any]:
        """获取用户行为信息"""
        return {
            "mouse_movement": "natural",
            "keyboard_events": "normal",
            "scroll_pattern": "smooth",
            "click_pattern": "human_like",
            "time_on_page": random.randint(5, 300),
            "page_views": random.randint(1, 50),
            "session_duration": random.randint(60, 3600)
        }
    
    def _generate_environment_hash(self) -> str:
        """生成环境哈希"""
        env_data = {
            "device_id": self.device_id,
            "user_agent": self.user_agent,
            "screen_info": self.screen_info,
            "timezone": self.timezone_info["timezone"],
            "hardware_info": self.hardware_info["platform"],
            "webgl_info": self.webgl_info["webgl_renderer"],
            "canvas_fingerprint": self.canvas_info["canvas_fingerprint"],
            "network_info": self.network_info["local_ip"]
        }
        
        env_json = json.dumps(env_data, sort_keys=True)
        return hashlib.sha256(env_json.encode()).hexdigest()
    
    def _generate_signature_structure(self, context: Dict[str, Any]) -> bytes:
        """生成签名结构"""
        timestamp = context["timestamp"]
        
        # 签名头
        signature_header = struct.pack('!B', 0xD9)  # 固定头
        
        # 核心哈希
        core_data = json.dumps({
            "path": context["path"],
            "params": context["params"],
            "timestamp": timestamp,
            "device_id": self.device_id,
            "session_id": self.session_id,
            "environment_hash": self._generate_environment_hash()
        }, separators=(',', ':'), sort_keys=True)
        
        core_hash = hashlib.sha256(core_data.encode()).digest()
        
        # 设备指纹
        device_fingerprint = hashlib.md5(
            (self.device_id + self.user_agent + str(timestamp)).encode()
        ).digest()
        
        # 会话指纹
        session_fingerprint = hashlib.sha1(
            (self.session_id + str(timestamp)).encode()
        ).digest()
        
        # 环境指纹
        env_data = json.dumps({
            "screen": self.screen_info,
            "timezone": self.timezone_info,
            "hardware": self.hardware_info,
            "webgl": self.webgl_info,
            "canvas": self.canvas_info,
            "network": self.network_info
        }, sort_keys=True)
        env_fingerprint = hashlib.sha256(env_data.encode()).digest()
        
        # 行为指纹
        behavior_data = json.dumps(self._get_behavior_info(), sort_keys=True)
        behavior_fingerprint = hashlib.md5(behavior_data.encode()).digest()
        
        # 安全验证
        security_data = json.dumps(self._get_security_info(), sort_keys=True)
        security_fingerprint = hashlib.sha1(security_data.encode()).digest()
        
        # 组合签名
        signature_data = signature_header
        signature_data += core_hash  # 32 bytes
        signature_data += device_fingerprint  # 16 bytes
        signature_data += session_fingerprint  # 20 bytes
        signature_data += env_fingerprint  # 32 bytes
        signature_data += behavior_fingerprint  # 16 bytes
        signature_data += security_fingerprint  # 20 bytes
        
        # 添加时间戳
        signature_data += struct.pack('!Q', timestamp)  # 8 bytes
        
        # 添加随机填充以达到241字节
        current_length = len(signature_data)
        target_length = 241
        
        if current_length < target_length:
            padding_length = target_length - current_length
            padding = bytes([random.randint(0, 255) for _ in range(padding_length)])
            signature_data += padding
        
        return signature_data[:target_length]
    
    def generate_realistic_signature(self, path: str, params: Dict[str, Any], url: str = "https://edith.xiaohongshu.com") -> str:
        """
        生成包含真实环境信息的完整X-S签名
        
        Args:
            path: API路径
            params: 请求参数
            url: 完整URL
            
        Returns:
            包含真实环境信息的X-S签名
        """
        timestamp = int(time.time() * 1000)
        
        # 构建完整上下文
        context = {
            "path": path,
            "params": params,
            "timestamp": timestamp,
            "url": url,
            "device_id": self.device_id,
            "session_id": self.session_id,
            "web_id": self.web_id,
            "trace_id": self.trace_id,
            "request_id": self.request_id,
            "user_agent": self.user_agent,
            "screen_info": self.screen_info,
            "timezone_info": self.timezone_info,
            "language_info": self.language_info,
            "hardware_info": self.hardware_info,
            "webgl_info": self.webgl_info,
            "canvas_info": self.canvas_info,
            "network_info": self.network_info,
            "cookie_info": self._get_cookie_info(),
            "security_info": self._get_security_info(),
            "behavior_info": self._get_behavior_info()
        }
        
        # 生成签名数据
        signature_data = self._generate_signature_structure(context)
        
        # Base64编码
        signature_base64 = base64.b64encode(signature_data).decode()
        
        # 添加版本前缀
        complete_signature = f"{self.version}_{signature_base64}"
        
        return complete_signature
    
    def get_environment_info(self) -> Dict[str, Any]:
        """获取完整的环境信息（用于调试）"""
        return {
            "device_id": self.device_id,
            "session_id": self.session_id,
            "web_id": self.web_id,
            "trace_id": self.trace_id,
            "request_id": self.request_id,
            "user_agent": self.user_agent,
            "screen_info": self.screen_info,
            "timezone_info": self.timezone_info,
            "language_info": self.language_info,
            "hardware_info": self.hardware_info,
            "webgl_info": self.webgl_info,
            "canvas_info": self.canvas_info,
            "network_info": self.network_info,
            "cookie_info": self._get_cookie_info(),
            "security_info": self._get_security_info(),
            "behavior_info": self._get_behavior_info()
        }

def main():
    """测试真实环境信息增强版签名生成器"""
    generator = RealisticXHSSignatureGenerator()
    
    print("=== 真实环境信息增强版XHS签名生成器 ===\n")
    
    # 显示环境信息
    print("生成的环境信息:")
    env_info = generator.get_environment_info()
    for key, value in env_info.items():
        if key in ["device_id", "session_id", "web_id", "trace_id", "request_id"]:
            print(f"{key}: {value}")
        elif key == "user_agent":
            print(f"{key}: {value[:50]}...")
        elif key == "screen_info":
            print(f"{key}: {value['resolution']}")
        elif key == "timezone_info":
            print(f"{key}: {value['timezone']}")
    print()
    
    # 生成签名
    path = "/api/sns/web/v2/comment/page"
    params = {
        "note_id": "68a35fc0000000001c009cd9",
        "cursor": "",
        "top_comment_id": "",
        "image_formats": "jpg,webp,avif",
        "xsec_token": "ABMARfqKuxx76hZj-CQH0D9AIHxh8oCmV_RTOxyE_DIpI="
    }
    
    signature = generator.generate_realistic_signature(path, params)
    
    print(f"生成的真实环境签名:")
    print(f"长度: {len(signature)}")
    print(f"签名: {signature}")
    
    # 分析签名结构
    if '_' in signature:
        prefix, base64_part = signature.split('_', 1)
        print(f"\n签名结构:")
        print(f"前缀: {prefix}")
        print(f"Base64部分长度: {len(base64_part)}")
        
        try:
            decoded = base64.b64decode(base64_part)
            print(f"解码后长度: {len(decoded)} 字节")
            print(f"解码后前16字节 (hex): {decoded.hex()[:32]}")
        except Exception as e:
            print(f"Base64解码失败: {e}")

if __name__ == "__main__":
    main()