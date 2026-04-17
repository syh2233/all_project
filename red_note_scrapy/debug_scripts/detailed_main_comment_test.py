#!/usr/bin/env python3
"""
详细检查主评论API的响应内容
"""

import json
import time
import requests
import urllib3
from xiaohongshu_xs_reverse_engineer import XiaohongshuXSReverseEngineer

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def detailed_main_comment_test():
    """详细测试主评论API"""
    print("🔍 详细检查主评论API响应")
    print("=" * 50)
    
    xs_engineer = XiaohongshuXSReverseEngineer()
    
    # 有效的Cookie (请定期更新)
    cookie_str = "a1=18810038977; webId=1234567890; web_session=04006789012345678901234567890123; webBuild=2.12.4; xsecappid=xhs-pc-web;"
    
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
    
    # 使用一个真实的笔记ID进行测试
    note_id = "6666666660000000000000000"
    url = f"https://edith.xiaohongshu.com/api/sns/web/v2/comment/page"
    
    params = {
        "note_id": note_id,
        "cursor": "",
        "num": 10
    }
    
    try:
        # 生成X-s参数
        print("📝 生成X-s参数...")
        xs_value = xs_engineer.generate_xs(url)
        print(f"✅ X-s生成成功")
        
        # 构建请求头
        headers = base_headers.copy()
        headers["X-s"] = xs_value
        headers["X-t"] = str(int(time.time() * 1000))
        
        # 发送请求
        print("🚀 发送请求...")
        response = requests.get(
            url,
            params=params,
            headers=headers,
            verify=False,
            timeout=10
        )
        
        print(f"📊 状态码: {response.status_code}")
        
        if response.status_code == 200:
            try:
                response_data = response.json()
                print(f"✅ JSON解析成功")
                print(f"📋 完整响应结构:")
                print(json.dumps(response_data, ensure_ascii=False, indent=2))
                
                # 分析响应
                if response_data.get("success"):
                    print("\n✅ 请求成功")
                    if "data" in response_data:
                        data = response_data["data"]
                        print(f"📋 Data字段内容:")
                        print(json.dumps(data, ensure_ascii=False, indent=2))
                        
                        if "comments" in data:
                            comments = data["comments"]
                            print(f"✅ 找到评论字段，数量: {len(comments)}")
                        else:
                            print(f"⚠️ Data字段中没有comments，包含: {list(data.keys())}")
                    else:
                        print(f"⚠️ 响应中没有data字段")
                else:
                    print(f"\n❌ 请求失败")
                    print(f"   错误码: {response_data.get('code')}")
                    print(f"   错误信息: {response_data.get('msg')}")
                    
            except json.JSONDecodeError as e:
                print(f"❌ JSON解析失败: {e}")
                print(f"📋 原始响应: {response.text}")
        else:
            print(f"❌ HTTP错误: {response.status_code}")
            print(f"📋 响应内容: {response.text}")
            
    except Exception as e:
        print(f"❌ 异常: {e}")


if __name__ == "__main__":
    detailed_main_comment_test()