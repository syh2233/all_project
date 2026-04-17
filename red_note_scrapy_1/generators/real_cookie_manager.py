#!/usr/bin/env python3
"""
真实Cookie管理器
用于保存和使用从小红书网站获取的真实Cookie
"""

import json
import os
import time
from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta


class RealCookieManager:
    """真实Cookie管理器"""
    
    def __init__(self):
        self.cookie_file = "real_xhs_cookies.json"
        self.cookies = self._load_cookies()
    
    def _load_cookies(self) -> Dict:
        """加载保存的Cookie"""
        if os.path.exists(self.cookie_file):
            try:
                with open(self.cookie_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"✅ 已加载保存的Cookie (共{len(data)}个)")
                    return data
            except Exception as e:
                print(f"⚠️ 加载Cookie失败: {e}")
        
        print("ℹ️ 没有找到保存的Cookie，请手动添加")
        return {}
    
    def _save_cookies(self):
        """保存Cookie"""
        try:
            with open(self.cookie_file, 'w', encoding='utf-8') as f:
                json.dump(self.cookies, f, ensure_ascii=False, indent=2)
            print(f"✅ Cookie已保存 (共{len(self.cookies)}个)")
        except Exception as e:
            print(f"⚠️ 保存Cookie失败: {e}")
    
    def add_cookie_from_string(self, cookie_string: str, source: str = "unknown"):
        """从字符串添加Cookie"""
        try:
            # 解析Cookie字符串
            cookie_dict = {}
            for part in cookie_string.split('; '):
                if '=' in part:
                    key, value = part.split('=', 1)
                    cookie_dict[key] = value
            
            if not cookie_dict:
                print("❌ Cookie格式错误")
                return False
            
            # 检查关键参数
            required_keys = ['a1', 'web_session', 'gid']
            missing_keys = [key for key in required_keys if key not in cookie_dict]
            
            if missing_keys:
                print(f"⚠️ Cookie缺少关键参数: {missing_keys}")
                print("这可能导致认证失败")
            
            # 保存Cookie
            cookie_id = f"cookie_{int(time.time())}"
            self.cookies[cookie_id] = {
                'cookie_dict': cookie_dict,
                'cookie_string': cookie_string,
                'source': source,
                'added_time': datetime.now().isoformat(),
                'last_used': None,
                'use_count': 0,
                'expiry_info': self._analyze_expiry(cookie_dict)
            }
            
            self._save_cookies()
            print(f"✅ Cookie添加成功 (ID: {cookie_id})")
            
            # 显示关键参数
            self._show_key_params(cookie_dict)
            
            return True
            
        except Exception as e:
            print(f"❌ 添加Cookie失败: {e}")
            return False
    
    def _analyze_expiry(self, cookie_dict: Dict) -> Dict:
        """分析Cookie过期信息"""
        expiry_info = {}
        
        # 根据参数特征分析过期时间
        for key, value in cookie_dict.items():
            if key in ['a1', 'webId']:
                expiry_info[key] = "长期有效 (数月)"
            elif key == 'web_session':
                expiry_info[key] = "长期有效 (数月)"
            elif key == 'gid':
                expiry_info[key] = "超长有效 (数年)"
            elif key in ['websectiga', 'sec_poison_id']:
                expiry_info[key] = "短期有效 (数天)"
            elif key in ['abRequestId', 'acw_tc', 'loadts']:
                expiry_info[key] = "动态生成 (每次请求)"
            else:
                expiry_info[key] = "未知"
        
        return expiry_info
    
    def _show_key_params(self, cookie_dict: Dict):
        """显示关键参数"""
        print("\n📋 关键参数:")
        key_params = ['a1', 'web_session', 'gid', 'webId']
        
        for param in key_params:
            if param in cookie_dict:
                value = cookie_dict[param]
                print(f"  {param}: {value[:20]}... (长度: {len(value)})")
    
    def get_best_cookie(self) -> Optional[Dict]:
        """获取最佳Cookie（优先选最新添加的）"""
        if not self.cookies:
            return None

        required_keys = ['a1', 'web_session', 'gid']

        # 筛选包含关键参数的Cookie，按添加时间倒序（最新优先）
        candidates = []
        for cookie_id, cookie_data in self.cookies.items():
            cookie_dict = cookie_data['cookie_dict']
            if all(key in cookie_dict for key in required_keys):
                candidates.append((cookie_id, cookie_data))

        if not candidates:
            return None

        # 按添加时间倒序，最新的排前面
        candidates.sort(key=lambda x: x[1].get('added_time', ''), reverse=True)
        best_cookie = candidates[0][1]

        # 更新使用信息
        best_cookie['last_used'] = datetime.now().isoformat()
        best_cookie['use_count'] += 1
        self._save_cookies()

        return best_cookie
    
    def get_cookie_string(self) -> Optional[str]:
        """获取Cookie字符串"""
        best_cookie = self.get_best_cookie()
        if best_cookie:
            return best_cookie['cookie_string']
        return None
    
    def get_cookie_dict(self) -> Optional[Dict]:
        """获取Cookie字典"""
        best_cookie = self.get_best_cookie()
        if best_cookie:
            return best_cookie['cookie_dict']
        return None
    
    def list_cookies(self):
        """列出所有Cookie"""
        if not self.cookies:
            print("📭 没有保存的Cookie")
            return
        
        print(f"📋 保存的Cookie (共{len(self.cookies)}个):")
        print("-" * 80)
        
        for i, (cookie_id, cookie_data) in enumerate(self.cookies.items(), 1):
            cookie_dict = cookie_data['cookie_dict']
            
            # 检查关键参数
            required_keys = ['a1', 'web_session', 'gid']
            has_required = all(key in cookie_dict for key in required_keys)
            
            status = "✅ 完整" if has_required else "⚠️ 缺失关键参数"
            
            print(f"{i}. {cookie_id}")
            print(f"   来源: {cookie_data['source']}")
            print(f"   添加时间: {cookie_data['added_time']}")
            print(f"   使用次数: {cookie_data['use_count']}")
            print(f"   最后使用: {cookie_data['last_used'] or '从未使用'}")
            print(f"   状态: {status}")
            
            if has_required:
                print(f"   关键参数: a1, web_session, gid")
            
            print("-" * 80)
    
    def remove_cookie(self, cookie_id: str):
        """删除Cookie"""
        if cookie_id in self.cookies:
            del self.cookies[cookie_id]
            self._save_cookies()
            print(f"✅ Cookie {cookie_id} 已删除")
        else:
            print(f"❌ 未找到Cookie {cookie_id}")
    
    def clear_all(self):
        """清空所有Cookie"""
        self.cookies.clear()
        if os.path.exists(self.cookie_file):
            os.remove(self.cookie_file)
        print("✅ 所有Cookie已清空")


def main():
    """测试真实Cookie管理器"""
    print("=== 真实Cookie管理器测试 ===\n")
    
    manager = RealCookieManager()
    
    # 示例：添加真实Cookie
    print("📝 请粘贴真实Cookie字符串（格式如：name1=value1; name2=value2; ...）")
    print("或者直接按回车跳过")
    
    cookie_input = input("\nCookie字符串: ").strip()
    
    if cookie_input:
        success = manager.add_cookie_from_string(cookie_input, "手动输入")
        if success:
            print("\n✅ Cookie添加成功！")
    
    # 列出所有Cookie
    print("\n📋 当前保存的Cookie:")
    manager.list_cookies()
    
    # 测试获取Cookie
    print("\n🔍 测试获取Cookie:")
    cookie_string = manager.get_cookie_string()
    if cookie_string:
        print("✅ 成功获取Cookie:")
        print(cookie_string[:100] + "...")
    else:
        print("❌ 没有可用的Cookie")


if __name__ == "__main__":
    main()