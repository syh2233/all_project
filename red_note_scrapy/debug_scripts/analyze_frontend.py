#!/usr/bin/env python3
"""
分析小红书前端JS代码找出正确的子评论API路径
"""

import requests
import json
import re
import time
from urllib.parse import urlparse, parse_qs

def analyze_frontend_code():
    """分析小红书前端JS代码"""
    
    print("分析小红书前端JS代码...\n")
    
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
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            html_content = response.text
            print(f"HTML内容长度: {len(html_content)} 字符")
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
    
    print(f"找到 {len(js_urls)} 个JS文件:")
    for i, js_url in enumerate(js_urls[:10], 1):  # 只显示前10个
        print(f"  {i}. {js_url}")
    
    if len(js_urls) > 10:
        print(f"  ... 还有 {len(js_urls) - 10} 个JS文件")
    
    print("\n" + "="*50 + "\n")
    
    # 搜索API相关的JS文件
    print("3. 搜索API相关的JS文件:")
    
    api_keywords = [
        'comment',
        'sub',
        'reply',
        'sns',
        'api',
        'edith'
    ]
    
    relevant_js_files = []
    
    for js_url in js_urls:
        # 检查URL中是否包含API相关关键词
        if any(keyword in js_url.lower() for keyword in api_keywords):
            relevant_js_files.append(js_url)
    
    print(f"找到 {len(relevant_js_files)} 个可能相关的JS文件:")
    for i, js_url in enumerate(relevant_js_files, 1):
        print(f"  {i}. {js_url}")
    
    print("\n" + "="*50 + "\n")
    
    # 分析相关JS文件
    print("4. 分析相关JS文件内容:")
    
    api_patterns = [
        r'/api/sns/web/v2/comment/[^"\s]+',
        r'/api/[^"\s]*comment[^"\s]*',
        r'sub[_-]?comment',
        r'reply[_-]?comment',
        r'child[_-]?comment',
        r'comment[_-]?sub',
        r'comment[_-]?reply'
    ]
    
    found_apis = set()
    
    for js_url in relevant_js_files[:5]:  # 只分析前5个文件
        print(f"\n分析JS文件: {js_url}")
        
        # 构建完整的JS URL
        if js_url.startswith('//'):
            js_url = 'https:' + js_url
        elif js_url.startswith('/'):
            js_url = 'https://www.xiaohongshu.com' + js_url
        
        try:
            js_response = session.get(js_url, headers=headers, timeout=10)
            if js_response.status_code == 200:
                js_content = js_response.text
                print(f"  JS文件大小: {len(js_content)} 字符")
                
                # 搜索API路径
                for pattern in api_patterns:
                    matches = re.findall(pattern, js_content)
                    for match in matches:
                        if match not in found_apis:
                            found_apis.add(match)
                            print(f"  发现API路径: {match}")
            else:
                print(f"  获取JS文件失败: {js_response.status_code}")
        except Exception as e:
            print(f"  分析JS文件出错: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 汇总发现的API路径
    print("5. 汇总发现的API路径:")
    
    if found_apis:
        print("发现的API路径:")
        for i, api in enumerate(found_apis, 1):
            print(f"  {i}. {api}")
    else:
        print("未发现明显的API路径")
    
    print("\n" + "="*50 + "\n")
    
    # 分析页面中的API调用
    print("6. 分析页面中的API调用:")
    
    # 搜索HTML中的API调用
    html_api_patterns = [
        r'/api/sns/web/v2/comment/[^"\s>]+',
        r'"/api/[^"]*comment[^"]*"',
        r'/api/[^"\s>]*comment[^"\s>]*'
    ]
    
    html_apis = set()
    
    for pattern in html_api_patterns:
        matches = re.findall(pattern, html_content)
        for match in matches:
            # 清理匹配结果
            clean_match = match.strip('"').strip("'")
            if clean_match not in html_apis:
                html_apis.add(clean_match)
                print(f"  发现API调用: {clean_match}")
    
    print("\n" + "="*50 + "\n")
    
    # 测试发现的API路径
    print("7. 测试发现的API路径:")
    
    test_apis = list(found_apis) + list(html_apis)
    
    # 基础请求头
    base_headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,en-GB;q=0.6',
        'origin': 'https://www.xiaohongshu.com',
        'referer': 'https://www.xiaohongshu.com/',
        'sec-ch-ua': '"Not;A=Brand";v="99", "Microsoft Edge";v="139", "Chromium";v="139"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0',
    }
    
    # 测试参数
    comment_id = "68a048ef000000003002a604"
    
    for api_path in test_apis:
        if not api_path.startswith('/api/'):
            continue
            
        print(f"\n测试API: {api_path}")
        
        # 构建完整URL
        if api_path.startswith('http'):
            full_url = api_path
        else:
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
            response = session.get(test_url, headers=base_headers, timeout=10)
            print(f"  状态码: {response.status_code}")
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"  成功: {data.get('success', False)}")
                    if data.get('success', False):
                        comments = data.get('data', {}).get('comments', [])
                        print(f"  子评论数量: {len(comments)}")
                    else:
                        print(f"  错误信息: {data.get('msg', 'Unknown error')}")
                        print(f"  错误代码: {data.get('code', 'Unknown')}")
                except:
                    print(f"  响应不是JSON格式: {response.text[:100]}")
            else:
                print(f"  失败: {response.text[:100]}")
        except Exception as e:
            print(f"  错误: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 结论
    print("8. 结论:")
    print("基于以上分析，")
    if found_apis or html_apis:
        print("1. 发现了多个可能的API路径")
        print("2. 需要进一步测试这些路径")
        print("3. 可能需要特定的认证参数")
    else:
        print("1. 未发现明确的子评论API路径")
        print("2. 可能需要深入分析更多JS文件")
        print("3. 可能需要动态分析页面行为")
    
    print("\n建议:")
    print("1. 使用浏览器开发者工具监控网络请求")
    print("2. 分析页面加载时的API调用")
    print("3. 查看点击'查看回复'时的网络请求")
    print("4. 可能需要模拟用户交互行为")

if __name__ == "__main__":
    # 禁用SSL警告
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    analyze_frontend_code()