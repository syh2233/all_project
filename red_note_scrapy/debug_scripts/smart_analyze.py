#!/usr/bin/env python3
"""
智能分析小红书JS文件中的API调用
"""

import requests
import json
import re
import time
from urllib.parse import urlparse, parse_qs
import base64

def smart_analyze_js():
    """智能分析JS文件"""
    
    print("智能分析小红书JS文件...\n")
    
    # 目标笔记URL
    note_id = "68a048c1000000001d01838e"
    page_url = f"https://www.xiaohongshu.com/explore/{note_id}"
    
    # 基础请求头
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,en-GB;q=0.6',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Not;A=Brand";v="99", "Microsoft Edge";v="139", "Chromium";v="139"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0',
    }
    
    session = requests.Session()
    session.verify = False
    session.timeout = 10
    
    print("1. 获取页面HTML:")
    try:
        response = session.get(page_url, headers=headers, timeout=10)
        if response.status_code == 200:
            html_content = response.text
            print("页面获取成功")
        else:
            print(f"获取页面失败: {response.status_code}")
            return
    except Exception as e:
        print(f"获取页面出错: {e}")
        return
    
    print("\n" + "="*50 + "\n")
    
    # 提取所有JS文件URL
    print("2. 提取JS文件URL:")
    js_pattern = r'<script[^>]*src="([^"]*\.js[^"]*)"[^>]*>'
    js_urls = re.findall(js_pattern, html_content)
    
    print(f"找到 {len(js_urls)} 个JS文件")
    
    # 分析所有JS文件
    print("\n3. 分析JS文件内容:")
    
    # 更全面的API搜索模式
    api_patterns = [
        # 标准API路径
        r'/api/sns/web/v2/comment/[a-zA-Z_/-]+',
        r'/api/[^"\'\s\)]*comment[^"\'\s\)]*',
        r'/api/[^"\'\s\)]*sub[^"\'\s\)]*',
        r'/api/[^"\'\s\)]*reply[^"\'\s\)]*',
        
        # 混淆的API路径
        r'[\'"`]\/api\/[^\'"`\s]+[\'"`]',
        r'[\'"`]\/sns\/[^\'"`\s]+[\'"`]',
        r'[\'"`]\/v2\/[^\'"`\s]+[\'"`]',
        
        # 函数调用中的API
        r'\.get\([\'"`]([^\'"`]+)[\'"`]',
        r'\.post\([\'"`]([^\'"`]+)[\'"`]',
        r'fetch\([\'"`]([^\'"`]+)[\'"`]',
        r'ajax\([\'"`]([^\'"`]+)[\'"`]',
        
        # 字符串拼接的API
        r'[a-zA-Z_$][a-zA-Z0-9_$]*\s*\+\s*[\'"`]\/api\/',
        r'[\'"`]\/api\/[\'"`]\s*\+\s*[a-zA-Z_$][a-zA-Z0-9_$]*',
        
        # URL参数
        r'note_id[\'"`]?\s*[:=]\s*[\'"`]([^\'"`]+)[\'"`]',
        r'comment_id[\'"`]?\s*[:=]\s*[\'"`]([^\'"`]+)[\'"`]',
        r'cursor[\'"`]?\s*[:=]\s*[\'"`]([^\'"`]+)[\'"`]',
        
        # 关键词搜索
        r'subComment|sub_comment|subcomment',
        r'replyComment|reply_comment|replycomment',
        r'childComment|child_comment|childcomment',
        r'commentList|comment_list|commentlist',
        r'getSubComment|get_sub_comment|getsubcomment',
        r'getReply|get_reply|getreply',
        r'loadMore|load_more|loadmore',
    ]
    
    found_apis = set()
    found_functions = set()
    found_variables = set()
    
    for i, js_url in enumerate(js_urls, 1):
        print(f"\n分析JS文件 {i}/{len(js_urls)}: {js_url}")
        
        # 构建完整的JS URL
        if js_url.startswith('//'):
            js_url = 'https:' + js_url
        elif js_url.startswith('/'):
            js_url = 'https://www.xiaohongshu.com' + js_url
        
        try:
            js_response = session.get(js_url, headers=headers, timeout=10)
            if js_response.status_code == 200:
                js_content = js_response.text
                print(f"  文件大小: {len(js_content)} 字符")
                
                # 搜索API相关内容
                for pattern in api_patterns:
                    matches = re.findall(pattern, js_content, re.IGNORECASE)
                    for match in matches:
                        # 清理和分类匹配结果
                        clean_match = match.strip()
                        
                        # 分类结果
                        if '/api/' in clean_match:
                            if clean_match not in found_apis:
                                found_apis.add(clean_match)
                                print(f"  发现API路径: {clean_match}")
                        elif any(keyword in clean_match.lower() for keyword in ['comment', 'sub', 'reply']):
                            if clean_match not in found_functions:
                                found_functions.add(clean_match)
                                print(f"  发现函数/方法: {clean_match}")
                        else:
                            if clean_match not in found_variables:
                                found_variables.add(clean_match)
                                print(f"  发现变量/参数: {clean_match}")
                
                # 搜索可能的混淆代码
                # 查找Base64编码的内容
                base64_pattern = r'[A-Za-z0-9+/=]{100,}'
                base64_matches = re.findall(base64_pattern, js_content)
                if base64_matches:
                    print(f"  发现 {len(base64_matches)} 个可能的Base64编码字符串")
                
                # 查找16进制字符串
                hex_pattern = r'\\x[0-9a-fA-F]{2}'
                hex_matches = re.findall(hex_pattern, js_content)
                if hex_matches:
                    print(f"  发现 {len(hex_matches)} 个16进制转义字符")
                
                # 查找Unicode转义
                unicode_pattern = r'\\u[0-9a-fA-F]{4}'
                unicode_matches = re.findall(unicode_pattern, js_content)
                if unicode_matches:
                    print(f"  发现 {len(unicode_matches)} 个Unicode转义字符")
                
            else:
                print(f"  获取JS文件失败: {js_response.status_code}")
        except Exception as e:
            print(f"  分析JS文件出错: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 汇总分析结果
    print("4. 汇总分析结果:")
    
    if found_apis:
        print("\n发现的API路径:")
        for i, api in enumerate(found_apis, 1):
            print(f"  {i}. {api}")
    
    if found_functions:
        print(f"\n发现的函数/方法 ({len(found_functions)} 个):")
        for i, func in enumerate(list(found_functions)[:10], 1):  # 只显示前10个
            print(f"  {i}. {func}")
        if len(found_functions) > 10:
            print(f"  ... 还有 {len(found_functions) - 10} 个")
    
    if found_variables:
        print(f"\n发现的变量/参数 ({len(found_variables)} 个):")
        for i, var in enumerate(list(found_variables)[:10], 1):  # 只显示前10个
            print(f"  {i}. {var}")
        if len(found_variables) > 10:
            print(f"  ... 还有 {len(found_variables) - 10} 个")
    
    print("\n" + "="*50 + "\n")
    
    # 推测可能的API路径
    print("5. 推测可能的API路径:")
    
    # 基于已知的API路径模式推测
    possible_apis = [
        "/api/sns/web/v2/comment/sub_comment/page",
        "/api/sns/web/v2/comment/subcomment/page", 
        "/api/sns/web/v2/comment/reply/page",
        "/api/sns/web/v2/comment/reply/list",
        "/api/sns/web/v2/comment/child/page",
        "/api/sns/web/v2/comment/child/list",
        "/api/sns/web/v2/comment/sub/list",
        "/api/sns/web/v2/comment/replies",
        "/api/sns/web/v2/comment/sub_comments",
        "/api/sns/web/v2/comment/get_sub",
        "/api/sns/web/v2/comment/fetch_sub",
        "/api/sns/web/v2/comment/load_sub",
    ]
    
    # 基于函数名推测
    for func in found_functions:
        func_lower = func.lower()
        if 'sub' in func_lower and 'comment' in func_lower:
            possible_apis.append(f"/api/sns/web/v2/comment/{func}/page")
        elif 'reply' in func_lower:
            possible_apis.append(f"/api/sns/web/v2/comment/{func}/page")
        elif 'child' in func_lower and 'comment' in func_lower:
            possible_apis.append(f"/api/sns/web/v2/comment/{func}/page")
    
    # 去重
    possible_apis = list(set(possible_apis))
    
    print("推测的API路径:")
    for i, api in enumerate(possible_apis, 1):
        print(f"  {i}. {api}")
    
    print("\n" + "="*50 + "\n")
    
    # 测试推测的API路径
    print("6. 测试推测的API路径:")
    
    # 测试参数
    comment_id = "68a048ef000000003002a604"
    
    # 简化的请求头
    test_headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,en-GB;q=0.6',
        'origin': 'https://www.xiaohongshu.com',
        'referer': 'https://www.xiaohongshu.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0',
    }
    
    success_apis = []
    
    for api_path in possible_apis[:10]:  # 只测试前10个
        print(f"\n测试API: {api_path}")
        
        # 构建完整URL
        full_url = f"https://edith.xiaohongshu.com{api_path}"
        
        # 准备参数
        params = {
            'note_id': note_id,
            'comment_id': comment_id,
            'cursor': '',
            'image_formats': 'jpg,webp,avif'
        }
        
        # 构建查询字符串
        from urllib.parse import urlencode
        query_string = urlencode({k: v for k, v in params.items() if v})
        test_url = f"{full_url}?{query_string}"
        
        try:
            response = session.get(test_url, headers=test_headers, timeout=10)
            print(f"  状态码: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    success = data.get('success', False)
                    print(f"  成功: {success}")
                    
                    if success:
                        comments = data.get('data', {}).get('comments', [])
                        print(f"  子评论数量: {len(comments)}")
                        success_apis.append(api_path)
                    else:
                        msg = data.get('msg', 'Unknown error')
                        code = data.get('code', 'Unknown')
                        print(f"  错误信息: {msg}")
                        print(f"  错误代码: {code}")
                        
                        # 如果是406错误，可能是正确的API但需要认证
                        if code == -1:
                            print("  -> 可能是正确的API，但需要认证")
                            success_apis.append(api_path)
                except:
                    print(f"  响应不是JSON格式")
            elif response.status_code == 406:
                print("  -> 406错误，可能是正确的API但需要认证")
                success_apis.append(api_path)
            else:
                print(f"  失败: {response.text[:100]}")
        except Exception as e:
            print(f"  错误: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 最终结论
    print("7. 最终结论:")
    
    if success_apis:
        print("发现可能的子评论API路径:")
        for i, api in enumerate(success_apis, 1):
            print(f"  {i}. {api}")
        
        print("\n建议:")
        print("1. 这些API路径返回406错误，说明路径正确但需要认证")
        print("2. 需要进一步分析认证机制")
        print("3. 可能需要特定的请求头或参数")
        print("4. 建议使用浏览器开发者工具验证")
    else:
        print("未发现有效的子评论API路径")
        print("建议:")
        print("1. 需要更深入的分析")
        print("2. 可能需要动态分析页面行为")
        print("3. 可能需要模拟用户交互")
    
    print("\n下一步行动:")
    print("1. 在浏览器中打开对应页面")
    print("2. 打开开发者工具 -> Network 选项卡")
    print("3. 点击'查看回复'按钮")
    print("4. 观察网络请求，找到正确的API路径")
    print("5. 分析请求头和参数")

if __name__ == "__main__":
    # 禁用SSL警告
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    smart_analyze_js()