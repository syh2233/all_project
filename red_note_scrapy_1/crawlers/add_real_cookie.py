#!/usr/bin/env python3
"""
添加真实Cookie到管理器
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "generators"))

from real_cookie_manager import RealCookieManager


def add_real_cookie():
    """添加真实Cookie"""
    print("=== 添加真实Cookie ===\n")
    
    manager = RealCookieManager()
    
    print("请从小红书网站复制真实的Cookie字符串")
    print("格式应该类似于: name1=value1; name2=value2; name3=value3")
    print("必须包含以下关键参数: a1, web_session, gid")
    print()
    
    # 示例格式
    print("示例格式:")
    example_cookie = "gid=yj8D24fWSDv0yj8D24fK069V0yIY6AFDTDxSxyU1kTyk2428MD7AC4888W2q2Yy8fJ0KjyDJ; xsecappid=xhs-pc-web; a1=198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479; webId=fc4fb0dccb1a480d5f17359394c861d7; web_session=040069b3ed6ebed4fbe38d058d3a4bf7c6f823; webBuild=4.79.0; unread={%22ub%22:%2268b56bf2000000001c004134%22%2C%22ue%22:%2268a3fe26000000001c0126d1%22%2C%22uc%22:20}"
    print(f"Cookie: {example_cookie[:100]}...")
    print()
    
    # 获取用户输入
    cookie_string = input("请粘贴真实Cookie字符串: ").strip()
    
    if not cookie_string:
        print("❌ 未输入Cookie字符串")
        return False
    
    # 添加Cookie
    success = manager.add_cookie_from_string(cookie_string, "手动输入")
    
    if success:
        print("\n✅ Cookie添加成功！")
        print("现在可以运行爬虫测试了")
        
        # 显示当前所有Cookie
        print("\n📋 当前保存的Cookie:")
        manager.list_cookies()
        
        return True
    else:
        print("\n❌ Cookie添加失败")
        return False


def test_with_real_cookie():
    """使用真实Cookie测试"""
    print("\n=== 使用真实Cookie测试 ===")
    
    manager = RealCookieManager()
    cookie_string = manager.get_cookie_string()
    
    if not cookie_string:
        print("❌ 没有可用的真实Cookie")
        return False
    
    print("✅ 找到真实Cookie:")
    print(f"Cookie: {cookie_string[:100]}...")
    
    # 解析并显示关键参数
    cookie_dict = {}
    for part in cookie_string.split('; '):
        if '=' in part:
            key, value = part.split('=', 1)
            cookie_dict[key] = value
    
    print("\n📋 关键参数:")
    for key in ['a1', 'web_session', 'gid', 'webId']:
        if key in cookie_dict:
            value = cookie_dict[key]
            print(f"  {key}: {value}")
    
    return True


if __name__ == "__main__":
    print("🚀 小红书真实Cookie管理器\n")
    
    print("选择操作:")
    print("1. 添加真实Cookie")
    print("2. 查看已保存的Cookie")
    print("3. 测试真实Cookie")
    print("4. 退出")
    
    while True:
        choice = input("\n请选择 (1-4): ").strip()
        
        if choice == "1":
            add_real_cookie()
        elif choice == "2":
            manager = RealCookieManager()
            manager.list_cookies()
        elif choice == "3":
            test_with_real_cookie()
        elif choice == "4":
            print("👋 再见")
            break
        else:
            print("❌ 无效选择，请重新输入")