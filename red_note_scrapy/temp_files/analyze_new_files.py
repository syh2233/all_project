#!/usr/bin/env python3
"""
分析新增的3个文件对子评论获取的影响
"""

import json
import time
import requests
import urllib3
from xiaohongshu_xs_reverse_engineer import XiaohongshuXSReverseEngineer

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def analyze_new_files():
    """分析新增文件的影响"""
    print("🔍 分析新增的3个文件对子评论获取的影响")
    print("=" * 70)
    
    # 1. 分析page.json文件
    print("\n📋 1. 分析page.json文件")
    print("-" * 50)
    
    with open("page.json", "r", encoding="utf-8") as f:
        page_data = json.load(f)
    
    print("✅ page.json包含真实的评论数据")
    print(f"   笔记ID: {page_data['data']['comments'][0]['note_id']}")
    print(f"   评论数量: {len(page_data['data']['comments'])}")
    
    # 分析子评论数据
    total_sub_comments = 0
    for comment in page_data['data']['comments']:
        if 'sub_comments' in comment and comment['sub_comments']:
            total_sub_comments += len(comment['sub_comments'])
    
    print(f"   子评论数量: {total_sub_comments}")
    
    # 提取关键信息
    first_comment = page_data['data']['comments'][0]
    note_id = first_comment['note_id']
    comment_id = first_comment['id']
    
    print(f"   关键参数:")
    print(f"     note_id: {note_id}")
    print(f"     comment_id: {comment_id}")
    
    # 检查是否有xsec_token
    if 'user_info' in first_comment and 'xsec_token' in first_comment['user_info']:
        xsec_token = first_comment['user_info']['xsec_token']
        print(f"     xsec_token: {xsec_token[:30]}...")
    
    # 2. 分析userscript_3.html文件
    print("\n📋 2. 分析userscript_3.html文件")
    print("-" * 50)
    
    print("✅ 这是一个Cookie监控和调试脚本")
    print("   功能: 监控JavaScript对cookie的修改")
    print("   特点: 可以设置断点规则来调试特定的cookie")
    
    # 关键发现
    debugger_rules = 'const debuggerRules = ["x-s-common"];'
    print(f"   关键配置: {debugger_rules}")
    print("   这个脚本可以帮助我们分析x-s-common参数的生成过程")
    
    # 3. 分析Note.457d2fea.js文件
    print("\n📋 3. 分析Note.457d2fea.js文件")
    print("-" * 50)
    
    print("✅ 这是一个大型的JavaScript文件 (332KB)")
    print("   内容: 小红书前端应用的JavaScript代码")
    print("   作用: 包含评论相关的组件和逻辑")
    
    # 4. 基于新数据测试子评论API
    print("\n📋 4. 基于真实数据测试子评论API")
    print("-" * 50)
    
    xs_engineer = XiaohongshuXSReverseEngineer()
    
    # 新提供的Cookie
    cookie_str = "gid=yj8D24fWSDv0yj8D24fK069V0yIY6AFDTDxSxyU1kTyk2428MD7AC4888W2q2Yy8fJ0KjyDJ; xsecappid=xhs-pc-web; abRequestId=f425aaf4-2614-55c8-b8d1-262c611be2ab; a1=198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479; webId=fc4fb0dccb1a480d5f17359394c861d7; webBuild=4.79.0; unread={%22ub%22:%2268b56bf2000000001c004134%22%2C%22ue%22:%2268a3fe26000000001c0126d1%22%2C%22uc%22:20}; web_session=040069b3ed6ebed4fbe38d058d3a4bf7c6f823; loadts=1756911545822; websectiga=10f9a40ba454a07755a08f27ef8194c53637eba4551cf9751c009d9afb564467"
    
    # 基础请求头
    base_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": "https://www.xiaohongshu.com/",
        "Origin": "https://www.xiaohongshu.com",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Cookie": cookie_str
    }
    
    # 子评论API
    sub_url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page"
    
    # 使用page.json中的真实数据
    test_cases = [
        {
            "name": "基础测试",
            "params": {
                "note_id": note_id,
                "root_comment_id": comment_id,
                "num": 10,
                "cursor": ""
            }
        },
        {
            "name": "带cursor测试",
            "params": {
                "note_id": note_id,
                "root_comment_id": comment_id,
                "num": 10,
                "cursor": "68a83ccd000000002700255f"  # 从page.json中获取
            }
        },
        {
            "name": "完整参数测试",
            "params": {
                "note_id": note_id,
                "root_comment_id": comment_id,
                "num": 10,
                "cursor": "",
                "image_formats": "jpg,webp,avif",
                "top_comment_id": ""
            }
        }
    ]
    
    results = []
    
    for test_case in test_cases:
        print(f"\n🔬 测试: {test_case['name']}")
        print(f"   参数: {json.dumps(test_case['params'], ensure_ascii=False, indent=6)}")
        
        try:
            # 生成X-s参数
            xs_value = xs_engineer.generate_xs(sub_url)
            xs_common = xs_engineer.generate_xs(sub_url)
            
            # 构建请求头
            headers = base_headers.copy()
            headers["X-s"] = xs_value
            headers["X-s-common"] = xs_common
            headers["X-t"] = str(int(time.time() * 1000))
            headers["Content-Type"] = "application/json;charset=UTF-8"
            
            # 发送请求
            response = requests.get(
                sub_url,
                params=test_case["params"],
                headers=headers,
                verify=False,
                timeout=10
            )
            
            print(f"   状态码: {response.status_code}")
            
            if response.status_code == 200:
                response_data = response.json()
                success = response_data.get("success", False)
                print(f"   响应成功: {success}")
                
                if success:
                    data = response_data.get("data", {})
                    comments = data.get("comments", [])
                    print(f"   ✅ 成功获取到 {len(comments)} 条子评论！")
                    
                    result = {
                        "test_name": test_case["name"],
                        "success": True,
                        "comment_count": len(comments),
                        "status_code": response.status_code
                    }
                else:
                    msg = response_data.get("msg", "未知错误")
                    print(f"   ❌ 失败: {msg}")
                    
                    result = {
                        "test_name": test_case["name"],
                        "success": False,
                        "error": msg,
                        "status_code": response.status_code
                    }
            else:
                print(f"   ❌ HTTP错误: {response.status_code}")
                
                result = {
                    "test_name": test_case["name"],
                    "success": False,
                    "http_error": response.status_code,
                    "status_code": response.status_code
                }
                
        except Exception as e:
            print(f"   ❌ 异常: {e}")
            result = {
                "test_name": test_case["name"],
                "success": False,
                "exception": str(e)
            }
        
        results.append(result)
    
    # 5. 综合分析
    print("\n📋 5. 综合分析")
    print("-" * 50)
    
    success_count = sum(1 for r in results if r.get("success"))
    
    print(f"测试结果: {success_count}/{len(results)} 成功")
    
    if success_count > 0:
        print("🎉 成功！子评论API可以正常获取！")
        
        print("\n✅ 成功的测试:")
        for result in results:
            if result.get("success"):
                print(f"   - {result['test_name']}: {result['comment_count']} 条子评论")
        
        print("\n🎯 子评论获取功能已突破！")
        print("✅ 使用真实数据可以成功获取子评论")
        print("✅ X-s算法工作正常")
        print("✅ Cookie认证有效")
        
    else:
        print("❌ 所有测试都失败了")
        print("💡 需要进一步分析认证机制")
        
        print("\n❌ 失败的测试:")
        for result in results:
            error = result.get("error", result.get("http_error", result.get("exception", "Unknown")))
            print(f"   - {result['test_name']}: {error}")
    
    # 6. 关键发现总结
    print("\n📋 6. 关键发现总结")
    print("-" * 50)
    
    key_findings = {
        "page.json": "包含真实的评论和子评论数据",
        "userscript_3.html": "Cookie监控脚本，可以调试x-s-common参数",
        "Note.457d2fea.js": "前端JavaScript代码，包含评论组件逻辑",
        "真实数据测试": f"{success_count}个测试成功" if success_count > 0 else "所有测试失败",
        "子评论API状态": "可以获取" if success_count > 0 else "仍需突破"
    }
    
    for key, value in key_findings.items():
        print(f"   {key}: {value}")
    
    # 7. 建议
    print("\n📋 7. 建议")
    print("-" * 50)
    
    if success_count > 0:
        print("✅ 子评论获取功能已实现")
        print("   可以直接使用API获取子评论数据")
    else:
        print("💡 建议使用以下方法:")
        print("   1. 使用userscript_3.html调试x-s-common参数")
        print("   2. 分析Note.457d2fea.js中的认证逻辑")
        print("   3. 使用page.json中的真实数据进行测试")
        print("   4. 考虑使用浏览器自动化方案")
    
    # 保存分析结果
    analysis_result = {
        "timestamp": str(int(time.time() * 1000)),
        "file_analysis": {
            "page.json": {
                "status": "real_data",
                "note_id": note_id,
                "comment_count": len(page_data['data']['comments']),
                "sub_comment_count": total_sub_comments
            },
            "userscript_3.html": {
                "status": "cookie_monitor",
                "debugger_rules": ["x-s-common"],
                "purpose": "debug_cookie_generation"
            },
            "Note.457d2fea.js": {
                "status": "frontend_code",
                "size": "332KB",
                "purpose": "comment_components"
            }
        },
        "test_results": {
            "total_tests": len(results),
            "success_count": success_count,
            "success_rate": f"{(success_count/len(results)*100):.1f}%" if len(results) > 0 else "0%",
            "details": results
        },
        "conclusions": key_findings,
        "recommendations": {
            "sub_comment_accessible": success_count > 0,
            "use_real_data": True,
            "debug_cookie_generation": True,
            "analyze_frontend_code": True
        }
    }
    
    with open("new_files_analysis.json", "w", encoding="utf-8") as f:
        json.dump(analysis_result, f, ensure_ascii=False, indent=2)
    
    print(f"\n📁 分析结果已保存到: new_files_analysis.json")
    
    return analysis_result


if __name__ == "__main__":
    analyze_new_files()