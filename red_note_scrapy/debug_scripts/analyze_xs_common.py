#!/usr/bin/env python3
"""
深入分析x-s-common参数的生成算法
"""

import requests
import json
import re
import time
import base64
import hashlib
from urllib.parse import urlparse, parse_qs

def analyze_xs_common():
    """分析x-s-common参数"""
    
    print("分析x-s-common参数生成算法...\n")
    
    # 你提供的x-s-common值
    xs_common_value = "XYS_2UQhPsHCH0c1Pjh9HjIj2erjwjQhyoPTqBPT49pjHjIj2eHjwjQgynEDJ74AHjIj2ePjwjQTJdPIP/ZlgMrU4SmH4emPLfkj4DpCn/QEndG3JnMsJLprPepLpez9tAS+aDQbzDzwqer9+BpBLrYg20+64BRG8SQdJaTOGDEwy9IM4DzP+B+GLSr9/bYD8oprwgzN+nGItFcUz9Y7G7p82LLI4URP8AqUJrpCJdk7874Bpbcl+LRhqrSbzDSc+Mk6N7kCG9EkJ7GU+FzG/9k38rp98pYfLgkE4nHIPnMBqbcMpBWA49brHjIj2ecjwjHjKc=="
    
    print("1. 分析x-s-common值:")
    print(f"原始值: {xs_common_value}")
    print(f"长度: {len(xs_common_value)}")
    
    # 检查是否是Base64编码
    print("\n2. Base64分析:")
    try:
        # 移除可能的XYS_前缀
        if xs_common_value.startswith('XYS_'):
            base64_part = xs_common_value[4:]
            print(f"Base64部分: {base64_part}")
            
            # 尝试解码
            decoded = base64.b64decode(base64_part)
            print(f"解码后长度: {len(decoded)}")
            print(f"解码后内容: {decoded}")
            
            # 尝试不同的编码
            encodings = ['utf-8', 'gbk', 'gb2312', 'latin-1']
            for encoding in encodings:
                try:
                    text = decoded.decode(encoding)
                    print(f"{encoding}解码: {text}")
                except:
                    pass
    except Exception as e:
        print(f"Base64解码失败: {e}")
    
    print("\n3. 分析x-s-common结构:")
    
    # 查找可能的模式
    patterns = [
        r'[A-Za-z0-9+/=]{20,}',  # Base64模式
        r'[A-Fa-f0-9]{32,}',      # 十六进制模式
        r'[A-Za-z0-9_\-]{20,}',   # 一般字符串模式
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, xs_common_value)
        if matches:
            print(f"模式 {pattern}: {len(matches)} 个匹配")
            for match in matches[:3]:  # 只显示前3个
                print(f"  {match}")
    
    print("\n4. 分析时间戳相关性:")
    
    # 分析你提供的时间戳
    timestamp = "1756907129379"
    print(f"时间戳: {timestamp}")
    print(f"时间戳长度: {len(timestamp)}")
    
    # 转换为可读时间
    try:
        timestamp_int = int(timestamp) // 1000  # 毫秒转秒
        readable_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp_int))
        print(f"对应时间: {readable_time}")
    except:
        print("时间戳转换失败")
    
    print("\n5. 分析参数相关性:")
    
    # 分析URL参数
    url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page?note_id=68a048c1000000001d01838e&root_comment_id=68a048ef000000003002a604&num=10&cursor=68a706280000000030009afb&image_formats=jpg,webp,avif&top_comment_id=&xsec_token=ABIyAXG1J9ckAl0VbljygE3I8b6TZ0k5P4jORY-kCIzzw%3D"
    
    parsed_url = urlparse(url)
    params = parse_qs(parsed_url.query)
    
    print("URL参数:")
    for key, values in params.items():
        print(f"  {key}: {values[0]}")
    
    # 尝试不同的哈希算法
    print("\n6. 尝试哈希算法:")
    
    test_strings = [
        url,
        parsed_url.path,
        parsed_url.query,
        f"{timestamp}68a048c1000000001d01838e68a048ef000000003002a604",
        f"68a048c1000000001d01838e68a048ef000000003002a604{timestamp}",
    ]
    
    hash_algorithms = ['md5', 'sha1', 'sha256', 'sha512']
    
    for test_string in test_strings:
        print(f"\n测试字符串: {test_string[:50]}...")
        for algo in hash_algorithms:
            try:
                hash_obj = hashlib.new(algo)
                hash_obj.update(test_string.encode('utf-8'))
                hash_result = hash_obj.hexdigest()
                print(f"  {algo}: {hash_result}")
            except:
                pass
    
    print("\n7. 分析可能的生成算法:")
    
    # 分析x-s-common的组成部分
    if xs_common_value.startswith('XYS_'):
        prefix = xs_common_value[:4]
        content = xs_common_value[4:]
        
        print(f"前缀: {prefix}")
        print(f"内容: {content}")
        
        # 尝试分割内容
        if len(content) > 20:
            # 尝试找到固定长度的前缀
            possible_prefix = content[:20]
            print(f"可能的内容前缀: {possible_prefix}")
            
            # 尝试找到固定长度的后缀
            possible_suffix = content[-20:]
            print(f"可能的内容后缀: {possible_suffix}")
    
    print("\n8. 对比X-s和x-s-common:")
    
    # 你提供的X-s值
    x_s_value = "XYS_2UQhPsHCH0c1Pjh9HjIj2erjwjQhyoPTqBPT49pjHjIj2eHjwjQgynEDJ74AHjIj2ePjwjQTJdPIP/ZlgMrU4SmH4emPLfkj4DpCn/QEndG3JnMsJLprPepLpez9tAS+aDQbzDzwqer9+BpBLrYg20+64BRG8SQdJaTOGDEwy9IM4DzP+B+GLSr9/bYD8oprwgzN+nGItFcUz9Y7G7p82LLI4URP8AqUJrpCJdk7874Bpbcl+LRhqrSbzDSc+Mk6N7kCG9EkJ7GU+FzG/9k38rp98pYfLgkE4nHIPnMBqbcMpBWA49brHjIj2ecjwjHjKc=="
    
    print(f"X-s: {x_s_value}")
    print(f"x-s-common: {xs_common_value}")
    
    # 比较两个值
    if x_s_value == xs_common_value:
        print("X-s和x-s-common完全相同")
    else:
        print("X-s和x-s-common不同")
        
        # 计算差异
        diff_count = sum(1 for a, b in zip(x_s_value, xs_common_value) if a != b)
        print(f"差异字符数: {diff_count}")
        
        # 找出不同的位置
        differences = []
        for i, (a, b) in enumerate(zip(x_s_value, xs_common_value)):
            if a != b:
                differences.append((i, a, b))
        
        print(f"前5个差异:")
        for i, (pos, a, b) in enumerate(differences[:5]):
            print(f"  位置 {pos}: '{a}' vs '{b}'")
    
    print("\n9. 结论和建议:")
    print("基于以上分析:")
    print("1. x-s-common似乎使用了与X-s相同的前缀'XYS_'")
    print("2. 可能是Base64编码的内容")
    print("3. 长度较长，可能包含多个参数的哈希值")
    print("4. 可能与时间戳、URL参数相关")
    
    print("\n建议的下一步:")
    print("1. 需要分析前端JS代码中的生成算法")
    print("2. 可能需要模拟完整的浏览器环境")
    print("3. 可能需要特定的访问序列")
    print("4. 可能需要分析其他请求头参数")

if __name__ == "__main__":
    analyze_xs_common()