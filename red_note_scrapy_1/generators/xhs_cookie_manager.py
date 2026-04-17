#!/usr/bin/env python3
"""
XHS Cookie 管理器
自动生成和管理Cookie，避免过期问题
"""

import json
import time
import uuid
import random
import hashlib
import base64
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import os


class XHSCookieManager:
    """XHS Cookie管理器"""
    
    def __init__(self):
        self.cookie_cache = {}
        self.session_start_time = int(time.time() * 1000)
        self.device_id = self._generate_device_id()
        self.web_id = self._generate_web_id()
        
        # 加载保存的Cookie（如果有）
        self._load_cookies()
    
    def _generate_device_id(self) -> str:
        """生成设备ID"""
        timestamp = int(time.time() * 1000)
        random_part = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        return f"fc{timestamp % 1000000:06d}ccb1a480d5f17359394c861d{random_part}"
    
    def _generate_web_id(self) -> str:
        """生成Web ID"""
        return f"fc4fb0dccb1a480d5f17359394c861d7"
    
    def _generate_session_id(self) -> str:
        """生成会话ID"""
        timestamp = int(time.time() * 1000)
        random_part = ''.join([random.choice('0123456789abcdef') for _ in range(12)])
        return f"040069b3ed6ebed4fbe38d058d3a4bf7c6f8{timestamp % 10000:04d}{random_part}"
    
    def _generate_gid(self) -> str:
        """生成GID"""
        random_part = ''.join([random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz') for _ in range(8)])
        return f"g{random.randint(10000, 99999)}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random_part}"
    
    def _generate_a1(self) -> str:
        """生成a1认证令牌"""
        # 模拟真实a1格式
        timestamp = int(time.time() * 1000)
        random_part = ''.join([random.choice('0123456789abcdef') for _ in range(16)])
        return f"198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000{random.randint(60000, 99999)}"
    
    def _generate_ab_request_id(self) -> str:
        """生成请求ID"""
        return f"{uuid.uuid4()}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
    
    def _generate_acw_tc(self) -> str:
        """生成反爬虫令牌"""
        timestamp = int(time.time() * 1000)
        random_part = ''.join([random.choice('0123456789abcdef') for _ in range(32)])
        return f"0a{random.randint(100000, 999999)}{timestamp}{random_part[:16]}"
    
    def _generate_websectiga(self) -> str:
        """生成安全令牌"""
        random_part = ''.join([random.choice('0123456789abcdef') for _ in range(64)])
        return random_part
    
    def _generate_sec_poison_id(self) -> str:
        """生成安全ID"""
        return f"{uuid.uuid4()}"
    
    def _generate_loadts(self) -> str:
        """生成加载时间戳"""
        return str(int(time.time() * 1000))
    
    def _generate_unread_data(self) -> str:
        """生成未读信息数据"""
        # 基于真实cookie格式生成 - 使用固定的格式
        user_blog_id = f"68b56bf2000000001c004134"
        user_event_id = f"68a3fe26000000001c0126d1"
        unread_count = 20
        
        # 按照真实格式构建部分编码的字符串
        # 真实格式: {%22ub%22:%2268b56bf2000000001c004134%22%2C%22ue%22:%2268a3fe26000000001c0126d1%22%2C%22uc%22:20}
        import urllib.parse
        encoded_ub = urllib.parse.quote(user_blog_id)
        encoded_ue = urllib.parse.quote(user_event_id)
        
        return f'{{%22ub%22:%22{encoded_ub}%22%2C%22ue%22:%22{encoded_ue}%22%2C%22uc%22:{unread_count}}}'
    
    def _generate_web_session(self) -> str:
        """生成web session"""
        timestamp = int(time.time() * 1000)
        random_part = ''.join([random.choice('0123456789abcdef') for _ in range(12)])
        return f"040069b3ed6ebed4fbe38d058d3a4bf7c6f8{timestamp % 10000:04d}{random_part}"
    
    def _generate_gid(self) -> str:
        """生成GID"""
        # 按照真实gid格式生成：yj8D24fWSDv0yj8D24fK069V0yIY6AFDTDxSxyU1kTyk2428MD7AC4888W2q2Yy8fJ0KjyDJ
        parts = [
            "yj8D24fWSDv0yj8D24fK069V0yIY6AFDTDxSxyU1kTyk",
            "2428MD7AC4888W2q2Yy8fJ0KjyDJ"
        ]
        return "".join(parts)
    
    def _generate_ab_request_id(self) -> str:
        """生成AB请求ID"""
        return f"{uuid.uuid4()}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
    
    def _generate_acw_tc(self) -> str:
        """生成ACW_TC"""
        timestamp = int(time.time() * 1000)
        random_part = ''.join([random.choice('0123456789abcdef') for _ in range(32)])
        return f"0a{random.randint(100000, 999999)}{timestamp}{random_part[:16]}"
    
    def _generate_websectiga(self) -> str:
        """生成Web安全令牌"""
        random_part = ''.join([random.choice('0123456789abcdef') for _ in range(64)])
        return random_part
    
    def _generate_sec_poison_id(self) -> str:
        """生成安全ID"""
        return f"{uuid.uuid4()}"
    
    def _is_session_expired(self) -> bool:
        """检查会话是否过期"""
        if 'session_created' not in self.cookie_cache:
            return True
        
        session_age = int(time.time() * 1000) - self.cookie_cache['session_created']
        # 会话有效期30分钟
        return session_age > 30 * 60 * 1000
    
    def _is_gid_expired(self) -> bool:
        """检查GID是否过期"""
        if 'gid_created' not in self.cookie_cache:
            return True
        
        gid_age = int(time.time() * 1000) - self.cookie_cache['gid_created']
        # GID有效期24小时
        return gid_age > 24 * 60 * 60 * 1000
    
    def _load_cookies(self):
        """加载保存的Cookie"""
        cookie_file = "xhs_cookies.json"
        if os.path.exists(cookie_file):
            try:
                with open(cookie_file, 'r', encoding='utf-8') as f:
                    saved_cookies = json.load(f)
                    # 检查保存的Cookie是否还有效
                    if not self._is_session_expired():
                        self.cookie_cache.update(saved_cookies)
                        print("✅ 加载了保存的Cookie")
                    else:
                        print("⚠️ 保存的Cookie已过期，重新生成")
            except Exception as e:
                print(f"⚠️ 加载Cookie失败: {e}")
    
    def _save_cookies(self):
        """保存Cookie"""
        cookie_file = "xhs_cookies.json"
        try:
            with open(cookie_file, 'w', encoding='utf-8') as f:
                json.dump(self.cookie_cache, f, ensure_ascii=False, indent=2)
            print("✅ Cookie已保存")
        except Exception as e:
            print(f"⚠️ 保存Cookie失败: {e}")
    
    def generate_fresh_cookies(self) -> Dict[str, str]:
        """生成新鲜Cookie"""
        cookies = {}
        
        # 静态Cookie（设备相关）
        if 'webId' not in self.cookie_cache:
            cookies['webId'] = self.web_id
        
        if 'a1' not in self.cookie_cache:
            cookies['a1'] = self._generate_a1()
        
        # 会话Cookie（定期刷新）
        if self._is_session_expired() or 'web_session' not in self.cookie_cache:
            cookies['web_session'] = self._generate_web_session()
            cookies['sec_poison_id'] = self._generate_sec_poison_id()
            cookies['websectiga'] = self._generate_websectiga()
            self.cookie_cache['session_created'] = int(time.time() * 1000)
        
        # GID（每日刷新）
        if self._is_gid_expired() or 'gid' not in self.cookie_cache:
            cookies['gid'] = self._generate_gid()
            self.cookie_cache['gid_created'] = int(time.time() * 1000)
        
        # 动态Cookie（每次请求生成）
        cookies['abRequestId'] = self._generate_ab_request_id()
        cookies['acw_tc'] = self._generate_acw_tc()
        cookies['loadts'] = self._generate_loadts()
        
        # 固定Cookie
        cookies['xsecappid'] = 'xhs-pc-web'
        cookies['webBuild'] = '5.11.0'
        
        # 更新缓存
        for key, value in cookies.items():
            if key not in ['abRequestId', 'acw_tc', 'loadts']:  # 不保存动态Cookie
                self.cookie_cache[key] = value
        
        # 保存Cookie
        if cookies:
            self._save_cookies()
        
        return cookies
    
    def get_cookie_string(self, include_dynamic: bool = True) -> str:
        """获取Cookie字符串"""
        fresh_cookies = self.generate_fresh_cookies()
        
        # 添加缓存的Cookie
        all_cookies = fresh_cookies.copy()
        for key, value in self.cookie_cache.items():
            if key not in all_cookies and key not in ['session_created', 'gid_created']:
                all_cookies[key] = value
        
        # 添加动态生成的unread字段
        unread_data = self._generate_unread_data()
        all_cookies['unread'] = unread_data
        
        # 按照真实cookie的顺序排列
        ordered_keys = [
            'gid', 'xsecappid', 'abRequestId', 'a1', 'webId', 'web_session', 
            'webBuild', 'unread', 'acw_tc', 'websectiga', 'sec_poison_id', 'loadts'
        ]
        
        # 构建Cookie字符串
        cookie_parts = []
        for key in ordered_keys:
            if key in all_cookies:
                if include_dynamic or key not in ['abRequestId', 'acw_tc', 'loadts']:
                    cookie_parts.append(f"{key}={all_cookies[key]}")
        
        return "; ".join(cookie_parts)
    
    def get_cookie_dict(self) -> Dict[str, str]:
        """获取Cookie字典"""
        cookie_string = self.get_cookie_string()
        cookies = {}
        
        for part in cookie_string.split('; '):
            if '=' in part:
                key, value = part.split('=', 1)
                cookies[key] = value
        
        return cookies
    
    def refresh_session(self):
        """强制刷新会话"""
        # 清除会话相关Cookie
        session_keys = ['web_session', 'sec_poison_id', 'websectiga']
        for key in session_keys:
            if key in self.cookie_cache:
                del self.cookie_cache[key]
        
        # 重新生成会话
        fresh_cookies = self.generate_fresh_cookies()
        print("✅ 会话已刷新")
        
        return fresh_cookies
    
    def clear_all_cookies(self):
        """清除所有Cookie"""
        self.cookie_cache.clear()
        if os.path.exists("xhs_cookies.json"):
            os.remove("xhs_cookies.json")
        print("✅ 所有Cookie已清除")
    
    def get_cookie_info(self) -> Dict[str, Any]:
        """获取Cookie信息"""
        return {
            'device_id': self.device_id,
            'web_id': self.web_id,
            'session_age': int(time.time() * 1000) - self.cookie_cache.get('session_created', 0),
            'gid_age': int(time.time() * 1000) - self.cookie_cache.get('gid_created', 0),
            'session_expired': self._is_session_expired(),
            'gid_expired': self._is_gid_expired(),
            'cached_cookies': len([k for k in self.cookie_cache.keys() if k not in ['session_created', 'gid_created']])
        }


def main():
    """测试Cookie管理器"""
    print("=== XHS Cookie管理器测试 ===\n")
    
    # 初始化Cookie管理器
    cookie_manager = XHSCookieManager()
    
    # 显示Cookie信息
    print("Cookie信息:")
    cookie_info = cookie_manager.get_cookie_info()
    for key, value in cookie_info.items():
        if isinstance(value, bool):
            print(f"{key}: {'是' if value else '否'}")
        else:
            print(f"{key}: {value}")
    print()
    
    # 生成Cookie字符串
    print("生成的Cookie字符串:")
    cookie_string = cookie_manager.get_cookie_string()
    print(cookie_string[:200] + "..." if len(cookie_string) > 200 else cookie_string)
    print()
    
    # 生成Cookie字典
    print("Cookie字典:")
    cookie_dict = cookie_manager.get_cookie_dict()
    for key, value in cookie_dict.items():
        print(f"{key}: {value}")
    print()
    
    # 测试会话刷新
    print("测试会话刷新...")
    refreshed_cookies = cookie_manager.refresh_session()
    print(f"刷新的Cookie数量: {len(refreshed_cookies)}")
    print()


if __name__ == "__main__":
    main()