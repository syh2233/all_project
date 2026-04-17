#!/usr/bin/env python3
"""
分析小红书关键认证参数的变化规律
"""

import re
from datetime import datetime, timedelta


def analyze_parameter_patterns():
    """分析参数模式"""
    print("=== 小红书关键认证参数变化规律分析 ===\n")
    
    # 基于真实数据进行分析
    real_a1_values = [
        "198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479",  # 用户1登录1
        "198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow85000061059",  # 用户1登录2
        "198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow85000092396",  # 用户1登录3
        "1989539b7286fchcisbcy8u6ndue48dgwfq3ut54i50000654678"  # 用户2登录1
    ]
    
    real_web_session_values = [
        "040069b3ed6ebed4fbe38d058d3a4bf7c6f823",  # 用户1登录1
        "040069b3ed6ebed4fbe38d058d3a4bf7c6f88526e98bbf04b05b",  # 用户1登录2
        "040069b3ed6ebed4fbe38d058d3a4bf7c6f86293e0a663b4987a",  # 用户1登录3
        "040069b78925ac642ef28f338f3a4bdddd31e3"  # 用户2登录1
    ]
    
    real_gid_values = [
        "yj8D24fWSDv0yj8D24fK069V0yIY6AFDTDxSxyU1kTyk2428MD7AC4888W2q2Yy8fJ0KjyDJ",  # 用户1
        "yjYj2qjSJ4EiyjYj2qjDWi92JYKiSxS3MDSvA43Y7KIf7q28d4Yfk7888K24KWY8dK840jiy"  # 用户2
    ]
    
    print("📊 a1 参数分析:")
    print("=" * 50)
    for i, a1 in enumerate(real_a1_values, 1):
        print(f"{i}. {a1}")
        # 分析后6位
        last_6 = a1[-6:]
        user_type = "用户1" if i <= 3 else "用户2"
        print(f"   后6位: {last_6} (用户类型: {user_type})")
    
    print("\n📊 web_session 参数分析:")
    print("=" * 50)
    for i, session in enumerate(real_web_session_values, 1):
        print(f"{i}. {session}")
        # 分析固定前缀和变化部分
        prefix = session[:32]  # 固定前缀
        variable = session[32:]  # 变化部分
        user_type = "用户1" if i <= 3 else "用户2"
        print(f"   固定前缀: {prefix}")
        print(f"   变化部分: {variable} (用户类型: {user_type})")
    
    print("\n📊 gid 参数分析:")
    print("=" * 50)
    for i, gid in enumerate(real_gid_values, 1):
        print(f"{i}. {gid}")
        print(f"   长度: {len(gid)}")
        user_type = "用户1" if i == 1 else "用户2"
        print(f"   用户类型: {user_type}")
    
    print("\n🔍 变化规律总结:")
    print("=" * 50)
    
    print("✅ a1 参数:")
    print("   - 前缀不固定: 用户1前缀='198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000'")
    print("   - 用户2前缀: '1989539b7286fchcisbcy8u6ndue48dgwfq3ut54i50000'")
    print("   - 后6位变化: 可能是用户ID或会话标识")
    print("   - 每次登录: 后6位会变化")
    print("   - 不同用户: 前缀完全不同")
    
    print("\n✅ web_session 参数:")
    print("   - 前缀固定: '040069b3ed6ebed4fbe38d058d3a4bf7c6f8'")
    print("   - 后面部分变化: 每次登录都不同")
    print("   - 长度: 约38-44位")
    print("   - 有效期: 数月")
    
    print("\n✅ gid 参数:")
    print("   - 格式固定: 看起来是复杂的固定格式")
    print("   - 长度: 72位")
    print("   - 不同用户: 完全不同的值")
    print("   - 变化性: 与用户身份绑定")
    print("   - 有效期: 数年")
    
    print("🎯 关键发现 - 同账号多次登录分析:")
    print("=" * 50)
    print("❌ 重要修正: 同一账号每次登录参数都会变化！")
    print("")
    print("📊 用户1的三次登录对比:")
    print("• 登录1: a1=198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479")
    print("• 登录2: a1=198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow85000061059")
    print("• 登录3: a1=198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow85000092396")
    print("→ 前缀相同，后6位每次都变化！")
    print("")
    print("• web_session三次完全不同")
    print("• gid保持不变（与账号绑定）")
    print("")
    print("🎯 结论:")
    print("1. ❌ a1不是同账号固定不变 - 每次登录后6位都会变化")
    print("2. ❌ web_session每次登录都会完全变化")
    print("3. ✅ gid同账号固定不变")
    print("4. ❌ 无法通过程序模拟生成这些参数")
    print("")
    print("💡 程序化获取真实值的方案:")
    print("=" * 50)
    print("方案1: 自动化登录（推荐）")
    print("• 使用Selenium/Playwright模拟真实登录")
    print("• 处理验证码、短信验证等")
    print("• 提取登录后的Cookie")
    print("• 难度：⭐⭐⭐⭐")
    print("")
    print("方案2: API接口分析（困难）")
    print("• 分析登录接口的参数生成逻辑")
    print("• 逆向JavaScript加密算法")
    print("• 模拟完整的登录流程")
    print("• 难度：⭐⭐⭐⭐⭐")
    print("")
    print("方案3: 手动获取+程序管理（当前）")
    print("• 手动登录获取真实Cookie")
    print("• 程序自动管理和轮换使用")
    print("• 定期检查和更新Cookie")
    print("• 难度：⭐⭐")
    print("")
    print("🚀 建议:")
    print("1. 短期：继续使用当前的手动Cookie管理方案")
    print("2. 中期：研究Selenium自动化登录方案")
    print("3. 长期：深度逆向登录接口参数生成")
    
    print("\n💡 对爬虫的影响:")
    print("=" * 50)
    print("❌ 模拟生成无法通过服务器验证")
    print("✅ 真实登录生成的参数可以长期使用")
    print("✅ 同一用户多次登录的参数都有效")
    print("⚠️ 需要定期更新（数月有效期）")
    
    return True


def simulate_login_scenarios():
    """模拟不同登录场景"""
    print("\n=== 不同登录场景分析 ===\n")
    
    scenarios = {
        "同一用户，同一设备": {
            "description": "用户在同一台设备上多次登录",
            "a1变化": "后6位可能变化",
            "web_session变化": "完全变化",
            "gid变化": "可能不变",
            "有效性": "都有效"
        },
        "同一用户，不同设备": {
            "description": "用户在不同设备上登录",
            "a1变化": "后6位变化",
            "web_session变化": "完全变化",
            "gid变化": "可能变化",
            "有效性": "都有效"
        },
        "不同用户": {
            "description": "不同用户登录",
            "a1变化": "完全不同",
            "web_session变化": "完全不同",
            "gid变化": "完全不同",
            "有效性": "各自有效"
        }
    }
    
    for scenario, details in scenarios.items():
        print(f"📋 {scenario}:")
        print(f"   描述: {details['description']}")
        print(f"   a1变化: {details['a1变化']}")
        print(f"   web_session变化: {details['web_session变化']}")
        print(f"   gid变化: {details['gid变化']}")
        print(f"   有效性: {details['有效性']}")
        print()


if __name__ == "__main__":
    analyze_parameter_patterns()
    simulate_login_scenarios()
    
    print("🎯 重要建议:")
    print("=" * 50)
    print("1. 收集多个真实Cookie以备不时之需")
    print("2. 定期检查Cookie有效性")
    print("3. 不同设备的Cookie可以同时使用")
    print("4. 同一用户的多个Cookie都有效")
    print("5. 优先使用最近获取的Cookie")