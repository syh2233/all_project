#!/usr/bin/env python3
"""
测试更新后的Cookie管理器
验证所有参数生成是否正常
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "generators"))

from xhs_cookie_manager import XHSCookieManager
import json

def test_cookie_manager():
    """测试Cookie管理器"""
    print("=== 测试更新后的Cookie管理器 ===\n")
    
    # 初始化Cookie管理器
    cookie_manager = XHSCookieManager()
    
    # 测试1: 检查所有必需参数
    print("1. 检查生成的Cookie参数:")
    cookie_dict = cookie_manager.get_cookie_dict()
    
    required_params = [
        'webId', 'a1', 'web_session', 'gid', 'abRequestId', 
        'acw_tc', 'websectiga', 'sec_poison_id', 'loadts',
        'xsecappid', 'webBuild', 'unread'
    ]
    
    missing_params = []
    for param in required_params:
        if param not in cookie_dict:
            missing_params.append(param)
        else:
            print(f"✅ {param}: {cookie_dict[param][:50]}..." if len(cookie_dict[param]) > 50 else f"✅ {param}: {cookie_dict[param]}")
    
    if missing_params:
        print(f"❌ 缺失参数: {missing_params}")
        return False
    else:
        print("✅ 所有必需参数都已生成")
    
    # 测试2: 验证unread参数格式
    print("\n2. 验证unread参数格式:")
    unread_data = cookie_dict['unread']
    print(f"unread: {unread_data}")
    
    # 尝试解码
    try:
        import urllib.parse
        decoded = urllib.parse.unquote(unread_data)
        print(f"解码后: {decoded}")
        
        # 解析JSON
        unread_json = json.loads(decoded)
        print(f"JSON结构: {unread_json}")
        
        # 检查必需字段
        if 'ub' in unread_json and 'ue' in unread_json and 'uc' in unread_json:
            print("✅ unread参数格式正确")
        else:
            print("❌ unread参数格式错误")
            return False
            
    except Exception as e:
        print(f"❌ unread参数解析失败: {e}")
        return False
    
    # 测试3: 验证Cookie字符串格式
    print("\n3. 验证Cookie字符串格式:")
    cookie_string = cookie_manager.get_cookie_string()
    print(f"Cookie字符串长度: {len(cookie_string)}")
    print(f"Cookie字符串预览: {cookie_string[:200]}...")
    
    # 检查格式
    if '; ' in cookie_string and '=' in cookie_string:
        parts = cookie_string.split('; ')
        print(f"✅ Cookie包含 {len(parts)} 个参数")
        
        # 检查关键参数
        key_params = ['unread', 'webId', 'a1', 'web_session']
        for param in key_params:
            if any(part.startswith(f"{param}=") for part in parts):
                print(f"✅ 找到 {param} 参数")
            else:
                print(f"❌ 缺少 {param} 参数")
                return False
    else:
        print("❌ Cookie字符串格式错误")
        return False
    
    # 测试4: 测试会话刷新
    print("\n4. 测试会话刷新:")
    old_session = cookie_dict['web_session']
    refreshed_cookies = cookie_manager.refresh_session()
    new_session = refreshed_cookies.get('web_session', '')
    
    if old_session != new_session:
        print("✅ 会话刷新正常工作")
    else:
        print("❌ 会话刷新失败")
        return False
    
    print("\n🎉 所有测试通过！Cookie管理器已修复")
    return True

if __name__ == "__main__":
    success = test_cookie_manager()
    if success:
        print("\n✅ Cookie管理器现在可以正常工作")
        print("✅ 包含所有必需的参数")
        print("✅ unread参数格式正确")
        print("✅ 可以用于爬虫请求")
    else:
        print("\n❌ Cookie管理器仍有问题需要修复")