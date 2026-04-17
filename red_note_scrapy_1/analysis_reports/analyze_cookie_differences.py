#!/usr/bin/env python3
"""
分析真实Cookie与模拟Cookie的差异
识别哪些参数需要真实用户状态
"""

import urllib.parse

def analyze_cookies():
    """分析cookie差异"""
    print("=== Cookie差异分析 ===\n")
    
    # 真实Cookie
    real_cookie = "gid=yj8D24fWSDv0yj8D24fK069V0yIY6AFDTDxSxyU1kTyk2428MD7AC4888W2q2Yy8fJ0KjyDJ; xsecappid=xhs-pc-web; abRequestId=f425aaf4-2614-55c8-b8d1-262c611be2ab; a1=198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479; webId=fc4fb0dccb1a480d5f17359394c861d7; web_session=040069b3ed6ebed4fbe38d058d3a4bf7c6f823; webBuild=4.79.0; unread={%22ub%22:%2268b56bf2000000001c004134%22%2C%22ue%22:%2268a3fe26000000001c0126d1%22%2C%22uc%22:20}; acw_tc=0a0bb06417569972818746546efc5ea03db04c40ae9fc7661d3469c5ecf69c; websectiga=29098a4cf41f76ee3f8db19051aaa60c0fc7c5e305572fec762da32d457d76ae; sec_poison_id=e5ec492d-6a0b-4426-bf20-1bce11819c65; loadts=1756997606669"
    
    # 模拟Cookie
    simulated_cookie = "gid=yj8D24fWSDv0yj8D24fK069V0yIY6AFDTDxSxyU1kTyk2428MD7AC4888W2q2Yy8fJ0KjyDJ; xsecappid=xhs-pc-web; abRequestId=968b15fa-12b6-4e50-84ce-b493ba1a71f3-1155-5034; a1=198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow85000061059; webId=fc4fb0dccb1a480d5f17359394c861d7; web_session=040069b3ed6ebed4fbe38d058d3a4bf7c6f86293e0a663b4987a; webBuild=4.79.0; unread={%22ub%22:%2268b56bf2000000001c004134%22%2C%22ue%22:%2268a3fe26000000001c0126d1%22%2C%22uc%22:20}; acw_tc=0a354770175704740629481b61a7d9875e4bc; websectiga=e57bb6389f7615a84e3ff72150681bb643a18b8067edc14b3c2289f3d3341cd5; sec_poison_id=6a438bac-545f-487e-99ca-8212a08449d3; loadts=1757047406294"
    
    # 解析Cookie
    def parse_cookie(cookie_str):
        cookie_dict = {}
        for part in cookie_str.split('; '):
            if '=' in part:
                key, value = part.split('=', 1)
                cookie_dict[key] = value
        return cookie_dict
    
    real_cookies = parse_cookie(real_cookie)
    simulated_cookies = parse_cookie(simulated_cookie)
    
    print("真实Cookie参数:")
    for key, value in real_cookies.items():
        print(f"  {key}: {value}")
    
    print(f"\n模拟Cookie参数:")
    for key, value in simulated_cookies.items():
        print(f"  {key}: {value}")
    
    # 分析差异
    print(f"\n=== 差异分析 ===")
    print("参数对比:")
    
    critical_params = []
    
    for key in real_cookies:
        if key in simulated_cookies:
            real_val = real_cookies[key]
            sim_val = simulated_cookies[key]
            
            if real_val != sim_val:
                print(f"  🔴 {key}:")
                print(f"    真实: {real_val}")
                print(f"    模拟: {sim_val}")
                print(f"    差异: 值完全不同")
                
                # 判断参数类型
                if key in ['a1', 'web_session', 'gid']:
                    critical_params.append(key)
                    print(f"    ⚠️  这是关键认证参数，需要真实用户状态")
                elif key in ['websectiga', 'sec_poison_id']:
                    print(f"    ⚠️  这是安全参数，可能与用户会话绑定")
                elif key in ['abRequestId', 'acw_tc', 'loadts']:
                    print(f"    ℹ️  这是动态参数，每次请求都不同")
            else:
                print(f"  ✅ {key}: 值相同")
        else:
            print(f"  ❌ {key}: 模拟Cookie中缺失")
    
    # 分析关键参数特征
    print(f"\n=== 关键参数分析 ===")
    print("需要真实用户状态的参数:")
    
    for param in critical_params:
        real_val = real_cookies[param]
        print(f"\n  {param}:")
        print(f"    真实值: {real_val}")
        print(f"    长度: {len(real_val)}")
        
        if param == 'a1':
            print(f"    特征: 主要认证令牌，包含用户身份信息")
            print(f"    格式: 198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479")
            print(f"    分析: 后6位644479可能是用户ID或会话标识")
        elif param == 'web_session':
            print(f"    特征: 用户会话标识，长期有效")
            print(f"    格式: 040069b3ed6ebed4fbe38d058d3a4bf7c6f823")
            print(f"    分析: 固定前缀 + 会话标识")
        elif param == 'gid':
            print(f"    特征: 全局标识符，超长有效期")
            print(f"    格式: yj8D24fWSDv0yj8D24fK069V0yIY6AFDTDxSxyU1kTyk2428MD7AC4888W2q2Yy8fJ0KjyDJ")
            print(f"    分析: 复杂的固定格式，包含用户信息")
    
    # 结论
    print(f"\n=== 结论 ===")
    print("🚨 关键发现:")
    print("1. a1、web_session、gid 这三个参数是核心认证参数")
    print("2. 这些参数在真实Cookie中具有长期有效性")
    print("3. 模拟生成的参数无法通过服务器验证")
    print("4. 服务器返回'登录已过期'说明认证参数验证失败")
    
    print(f"\n💡 解决方案:")
    print("1. 短期: 使用真实的Cookie值")
    print("2. 中期: 实现Cookie提取和保存机制")
    print("3. 长期: 集成真实登录流程")
    
    return critical_params

if __name__ == "__main__":
    critical_params = analyze_cookies()
    print(f"\n需要真实用户状态的关键参数: {critical_params}")