import requests
import time
import sys
import os
import json
import random
from urllib.parse import urlencode
from seccore_sign_bridge import generate_seccore_sign, start_seccore_server, seccore_sign_via_server, stop_seccore_server
# from curl_cffi import requests

# 代理池 (ip|port|user|pwd)
PROXY_LIST = [
    "123.187.240.97|19597|OQER9BXPB8|43503534",
    "1.194.200.221|16195|DX4DHRVQCZ|13824768",
    "106.225.165.32|19144|PHHUSYXHJG|51285581",
    "59.36.227.5|10981|MWRG5TCTEM|94482286",
    "180.102.17.136|16875|YQGAVT98QJ|91896292",
    "115.239.216.242|14657|ZSBREWJQZ1|61675299",
]

# 记录不可用的代理
_dead_proxies = set()

def _build_proxy(proxy_str):
    """把 ip|port|user|pwd 转成 requests proxies 字典"""
    ip, port, user, pwd = proxy_str.split("|")
    proxy_url = f"socks5h://{user}:{pwd}@{ip}:{port}"
    return {"http": proxy_url, "https": proxy_url}

def get_random_proxy():
    """随机选一个可用代理，全部不可用时重置重试"""
    alive = [p for p in PROXY_LIST if p not in _dead_proxies]
    if not alive:
        print("⚠️ 所有代理均不可用，重置代理池重试")
        _dead_proxies.clear()
        alive = PROXY_LIST
    chosen = random.choice(alive)
    return chosen, _build_proxy(chosen)

def request_with_proxy(method, url, headers, max_retries=3, **kwargs):
    """带自动换代理重试的请求，返回 response 或 None"""
    for attempt in range(max_retries):
        proxy_str, proxies = get_random_proxy()
        try:
            resp = requests.request(method, url, headers=headers, proxies=proxies, timeout=30, **kwargs)
            return resp
        except Exception as e:
            _dead_proxies.add(proxy_str)
            remaining = len(PROXY_LIST) - len(_dead_proxies)
            print(f"  ⚠️ 代理 {proxy_str.split('|')[0]} 不可用，剩余{remaining}个可用代理 ({e})")
            if attempt < max_retries - 1:
                time.sleep(1)
    print("  ❌ 所有重试均失败")
    return None

def get_xt():
    # 获取当前时间戳（毫秒）
    return str(int(time.time() * 1000))

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "generators"))
from realistic_xhs_signature_generator import RealisticXHSSignatureGenerator
from xhs_cookie_manager import XHSCookieManager
from xhs_common_generator import XHSCommonGenerator

# 模块级单例，保持 sig_count 递增
_common_generator = XHSCommonGenerator()

def generate_headers_with_signature(path, params, use_real_cookie=True):
    """生成包含动态X-S签名和X-S-Common的请求头"""
    # 选择Cookie管理器
    if use_real_cookie:
        try:
            sys.path.append(os.path.join(os.path.dirname(__file__), "..", "generators"))
            from real_cookie_manager import RealCookieManager
            cookie_manager = RealCookieManager()
            cookie_string = cookie_manager.get_cookie_string()
            
            if cookie_string:
                print("✅ 使用真实Cookie")
                cookie_info = {"real_cookie": True}
            else:
                print("⚠️ 没有真实Cookie，使用模拟Cookie")
                cookie_manager = XHSCookieManager()
                cookie_string = cookie_manager.get_cookie_string()
                cookie_info = cookie_manager.get_cookie_info()
        except Exception as e:
            print(f"⚠️ 真实Cookie管理器失败，使用模拟Cookie: {e}")
            cookie_manager = XHSCookieManager()
            cookie_string = cookie_manager.get_cookie_string()
            cookie_info = cookie_manager.get_cookie_info()
    else:
        # 使用模拟Cookie
        cookie_manager = XHSCookieManager()
        cookie_string = cookie_manager.get_cookie_string()
        cookie_info = cookie_manager.get_cookie_info()
    
    # 初始化真实环境签名生成器
    signature_generator = RealisticXHSSignatureGenerator()
    
    # 使用模块级 X-S-Common 生成器（保持 sig_count 递增）
    common_generator = _common_generator

    # 生成X-S签名
    x_s_signature = signature_generator.generate_realistic_signature(path, params)
    print(f"x_s_signature: {x_s_signature}")
    
    # 生成X-S-Common
    full_url = f"https://edith.xiaohongshu.com{path}"
    x_s_common = common_generator.generate_xs_common(full_url, x_s_signature)
    print(f"x_s_common: {x_s_common}...")
    
    # 获取环境信息用于请求头
    env_info = signature_generator.get_environment_info()
    
    # 显示Cookie状态
    if isinstance(cookie_info, dict) and cookie_info.get("real_cookie"):
        print("Cookie状态: 使用真实Cookie (长期有效)")
    else:
        print(f"Cookie状态: 会话{'已过期' if cookie_info['session_expired'] else '有效'}, GID{'已过期' if cookie_info['gid_expired'] else '有效'}")
    
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9",
        "cookie": cookie_string,
        "origin": "https://www.xiaohongshu.com",
        "priority": "u=1, i",
        "referer": "https://www.xiaohongshu.com/",
        "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": env_info["user_agent"],
        "x-b3-traceid": env_info["trace_id"],
        "x-s": x_s_signature,
        "x-s-common": x_s_common,
        "x-t": get_xt(),
        "x-xray-traceid": env_info["trace_id"]
    }
    return headers

def generate_headers_with_browser_sign(path, params):
    """使用真实浏览器签名生成请求头（用于子评论等严格校验接口）

    优先级：seccore mnsv2 签名 > CDP 真实签名 > Node.js XYW_ 签名
    """
    # 获取真实 Cookie
    from real_cookie_manager import RealCookieManager
    cookie_manager = RealCookieManager()
    cookie_string = cookie_manager.get_cookie_string()
    if not cookie_string:
        print("  ❌ 没有真实Cookie，无法使用浏览器签名")
        return None

    # 生成 trace id
    signature_generator = RealisticXHSSignatureGenerator()
    env_info = signature_generator.get_environment_info()

    # 构建完整 API 路径
    query_string = urlencode(params)
    full_api_path = f"{path}?{query_string}"

    # 从 cookie 中提取 a1（签名服务需要）
    a1 = ""
    for part in cookie_string.split(";"):
        part = part.strip()
        if part.startswith("a1="):
            a1 = part[3:]
            break

    # 方式1: seccore mnsv2 签名（通过 Node.js 运行真实字节码 VM）
    seccore_result = seccore_sign_via_server(full_api_path, a1=a1)
    if not seccore_result:
        seccore_result = generate_seccore_sign(full_api_path)

    if seccore_result and seccore_result.get("xs"):
        print(f"  ✅ 使用 seccore mnsv2 签名 (XYS_)")
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9",
            "cookie": cookie_string,
            "origin": "https://www.xiaohongshu.com",
            "priority": "u=1, i",
            "referer": "https://www.xiaohongshu.com/",
            "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
            "x-b3-traceid": env_info["trace_id"],
            "x-s": seccore_result["xs"],
            "x-s-common": seccore_result.get("xsc", ""),
            "x-t": seccore_result["xt"],
            "x-xray-traceid": env_info["trace_id"],
        }
        return headers

    # seccore 签名失败
    print("  ❌ seccore mnsv2 签名失败")
    return None


def test_xhs_crawler():
    """测试集成真实环境X-S签名生成器的爬虫"""
    print("=== 测试XHS爬虫集成（真实环境签名）===")
    
    # API路径和参数
    api_path = "/api/sns/web/v2/comment/page"
    params = {
        "note_id": "699dd0b1000000001d024fe6",
        "cursor": "",
        "top_comment_id": "",
        "image_formats": "jpg,webp,avif",
        "xsec_token": "ABsRvLIMkL008_96o22gryTaZWQ1hS6ndztRDFWXI1M5s="
    }
    
    # 构建完整URL
    base_url = "https://edith.xiaohongshu.com"
    query_string = urlencode(params)
    full_url = f"{base_url}{api_path}?{query_string}"
    
    print(f"测试URL: {full_url}")
    print(f"API路径: {api_path}")
    print(f"参数: {params}")
    
    # 生成动态请求头
    headers = generate_headers_with_signature(api_path, params)
    print(f"生成的X-S签名: {headers['x-s']}")
    
    # 测试请求
    for attempt in range(3):
        try:
            print(f"\n第 {attempt + 1} 次尝试...")
            
            response = request_with_proxy("GET", full_url, headers=headers, allow_redirects=True)
            if response is None:
                print(f"❌ 第 {attempt + 1} 次尝试失败: 代理全部不可用")
                if attempt < 2:
                    time.sleep(2)
                continue
            
            print(f"响应状态码: {response.status_code}")
            print(f"Content-Type: {response.headers.get('Content-Type')}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print("✅ 请求成功!")
                    print(f"响应数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
                    return True
                except json.JSONDecodeError:
                    print("⚠️ 响应不是有效的JSON格式")
                    print(f"响应内容: {response.text[:200]}...")
            else:
                print(f"❌ 请求失败，状态码: {response.status_code}")
                print(f"响应内容: {response.text[:200]}...")
            
            break
            
        except Exception as e:
            print(f"❌ 第 {attempt + 1} 次尝试失败: {e}")
            if attempt < 2:
                time.sleep(2)
    
    return False

def test_cookie_management():
    """测试Cookie管理功能"""
    print("\n=== 测试Cookie管理 ===")
    
    # 初始化Cookie管理器
    cookie_manager = XHSCookieManager()
    
    # 显示Cookie信息
    print("Cookie管理信息:")
    cookie_info = cookie_manager.get_cookie_info()
    for key, value in cookie_info.items():
        if isinstance(value, bool):
            print(f"{key}: {'是' if value else '否'}")
        else:
            print(f"{key}: {value}")
    print()
    
    # 生成Cookie字符串
    print("生成的Cookie字符串:")
    cookie_string = cookie_manager.get_cookie_string()
    print(cookie_string if len(cookie_string) > 300 else cookie_string)
    print()
    
    # 显示Cookie字典
    print("Cookie字典:")
    cookie_dict = cookie_manager.get_cookie_dict()
    for key, value in cookie_dict.items():
        print(f"{key}: {value}")
    print()

def test_signature_generation():
    """测试签名生成功能"""
    print("\n=== 测试真实环境签名生成 ===")
    
    generator = RealisticXHSSignatureGenerator()
    
    # 显示环境信息
    print("生成的环境信息:")
    env_info = generator.get_environment_info()
    for key, value in env_info.items():
        if key in ["device_id", "session_id", "web_id", "trace_id", "request_id"]:
            print(f"{key}: {value}")
        elif key == "user_agent":
            print(f"{key}: {value[:50]}...")
        elif key == "screen_info":
            print(f"{key}: {value['resolution']}")
        elif key == "timezone_info":
            print(f"{key}: {value['timezone']}")
    print()
    
    test_cases = [
        {
            "path": "/api/sns/web/v2/comment/page",
            "params": {
                "note_id": "68a35fc0000000001c009cd9",
                "cursor": "",
                "top_comment_id": ""
            }
        },
        {
            "path": "/api/sns/web/v1/feed", 
            "params": {
                "note_id": "68a35fc0000000001c009cd9"
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        try:
            signature = generator.generate_realistic_signature(test_case["path"], test_case["params"])
            print(f"测试用例 {i}:")
            print(f"  路径: {test_case['path']}")
            print(f"  参数: {test_case['params']}")
            print(f"  生成的签名: {signature[:80]}...")
            print(f"  签名长度: {len(signature)}")
            print()
        except Exception as e:
            print(f"测试用例 {i} 失败: {e}")

def fetch_all_sub_comments(note_id, root_comment_id, xsec_token, initial_cursor=""):
    """获取某条主评论下的所有子评论"""
    all_sub_comments = []
    cursor = initial_cursor
    api_path = "/api/sns/web/v2/comment/sub/page"
    base_url = "https://edith.xiaohongshu.com"
    page = 0

    while True:
        page += 1
        params = {
            "note_id": note_id,
            "root_comment_id": root_comment_id,
            "num": "10",
            "cursor": cursor,
            "image_formats": "jpg,webp,avif",
            "top_comment_id": "",
            "xsec_token": xsec_token,
        }

        query_string = urlencode(params)
        full_url = f"{base_url}{api_path}?{query_string}"

        headers = generate_headers_with_browser_sign(api_path, params)
        if headers is None:
            print(f"    ⚠️ 签名失败，回退到模拟签名")
            headers = generate_headers_with_signature(api_path, params)

        data = None
        # 遇到 461 时换代理重试
        for retry in range(3):
            try:
                response = request_with_proxy("GET", full_url, headers=headers)
                if response is None:
                    print(f"    ❌ 子评论请求失败: 代理全部不可用")
                    break
                if response.status_code == 200:
                    resp_data = response.json()
                    if resp_data.get("code") == 0:
                        data = resp_data
                    else:
                        print(f"    ❌ 子评论接口返回错误: {resp_data.get('msg')}")
                    break
                elif response.status_code in (461, 403):
                    print(f"    ⚠️ 状态码 {response.status_code}，换代理重试 ({retry+1}/3)...")
                    time.sleep(random.uniform(3, 5))
                    # 重新生成签名（时间戳会变）
                    headers = generate_headers_with_browser_sign(api_path, params)
                    if headers is None:
                        headers = generate_headers_with_signature(api_path, params)
                    continue
                else:
                    print(f"    ❌ 子评论请求失败，状态码: {response.status_code}")
                    break
            except Exception as e:
                print(f"    ❌ 子评论请求异常: {e}")
                break

        if data is None:
            break

        comments = data.get("data", {}).get("comments", [])
        all_sub_comments.extend(comments)
        print(f"    子评论第{page}页: 获取{len(comments)}条，累计{len(all_sub_comments)}条")

        if not data.get("data", {}).get("has_more", False):
            break
        cursor = data.get("data", {}).get("cursor", "")
        if not cursor:
            break
        time.sleep(random.uniform(2, 4))

    return all_sub_comments


def fetch_all_comments(note_id, xsec_token):
    """获取笔记的所有主评论及其全部子评论，保存到JSON文件"""
    all_comments = []
    cursor = ""
    api_path = "/api/sns/web/v2/comment/page"
    base_url = "https://edith.xiaohongshu.com"
    page = 0
    total_sub = 0
    incomplete_sub_comments = 0

    # 使用主评论接口返回的动态xsec_token（服务端每页会刷新）
    current_xsec_token = xsec_token

    print(f"\n{'='*50}")
    print(f"开始爬取笔记所有评论: {note_id}")
    print(f"{'='*50}")

    while True:
        page += 1
        params = {
            "note_id": note_id,
            "cursor": cursor,
            "top_comment_id": "",
            "image_formats": "jpg,webp,avif",
            "xsec_token": current_xsec_token,
        }
        query_string = urlencode(params)
        full_url = f"{base_url}{api_path}?{query_string}"

        try:
            data = None
            for retry in range(3):
                headers = generate_headers_with_signature(api_path, params)
                response = request_with_proxy("GET", full_url, headers=headers)
                if response is None:
                    print(f"❌ 主评论请求失败: 代理全部不可用")
                    break
                if response.status_code == 200:
                    resp_data = response.json()
                    if resp_data.get("code") == 0:
                        data = resp_data
                    else:
                        print(f"❌ 主评论接口返回错误: {resp_data.get('msg')}")
                    break
                elif response.status_code in (461, 403):
                    print(f"⚠️ 主评论状态码 {response.status_code}，换代理重试 ({retry+1}/3)...")
                    time.sleep(random.uniform(3, 5))
                    continue
                else:
                    print(f"❌ 主评论请求失败，状态码: {response.status_code}")
                    break

            if data is None:
                break

            # 更新动态xsec_token
            new_token = data.get("data", {}).get("xsec_token", "")
            if new_token:
                current_xsec_token = new_token

            comments = data.get("data", {}).get("comments", [])
            print(f"\n主评论第{page}页: 获取{len(comments)}条")

            for comment in comments:
                # 如果子评论没拉完，尝试补全
                if comment.get("sub_comment_has_more"):
                    cid = comment["id"]
                    sub_cursor = comment.get("sub_comment_cursor", "")
                    print(f"  补全子评论 (主评论 {cid})...")
                    time.sleep(random.uniform(2, 4))
                    extra_subs = fetch_all_sub_comments(note_id, cid, current_xsec_token, sub_cursor)
                    if extra_subs:
                        # 合并：保留API已返回的 + 追加新拉取的（去重）
                        existing_ids = {s["id"] for s in comment.get("sub_comments", [])}
                        for s in extra_subs:
                            if s["id"] not in existing_ids:
                                comment.setdefault("sub_comments", []).append(s)
                                existing_ids.add(s["id"])
                        comment["sub_comment_has_more"] = False
                    else:
                        # 子评论补全失败，标记但不中断
                        declared = int(comment.get("sub_comment_count", 0))
                        fetched = len(comment.get("sub_comments", []))
                        print(f"    ⚠️ 子评论补全失败 (已有{fetched}/{declared}条)，跳过")
                        incomplete_sub_comments += 1

                sub_count = len(comment.get("sub_comments", []))
                total_sub += sub_count
                all_comments.append(comment)

            if not data.get("data", {}).get("has_more", False):
                print("\n所有主评论已获取完毕")
                break
            cursor = data.get("data", {}).get("cursor", "")
            if not cursor:
                break
            time.sleep(random.uniform(3, 5))
        except Exception as e:
            print(f"❌ 主评论请求异常: {e}")
            break

    # 保存结果
    output_file = os.path.join(os.path.dirname(__file__), f"comments_{note_id}.json")
    result = {
        "note_id": note_id,
        "total_comments": len(all_comments),
        "total_sub_comments": total_sub,
        "incomplete_sub_comments": incomplete_sub_comments,
        "comments": all_comments,
    }
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*50}")
    print(f"爬取完成!")
    print(f"主评论: {len(all_comments)} 条")
    print(f"子评论: {total_sub} 条")
    if incomplete_sub_comments > 0:
        print(f"⚠️ 子评论不完整: {incomplete_sub_comments} 条主评论的子评论未能完全获取")
    print(f"保存到: {output_file}")
    print(f"{'='*50}")
    return all_comments


if __name__ == "__main__":
    print("🚀 XHS真实环境签名生成器爬虫集成测试\n")

    # 启动 seccore mnsv2 签名服务（后台）
    print("启动 seccore 签名服务...")
    start_seccore_server()

    # 先测试Cookie管理
    test_cookie_management()

    # 再测试签名生成
    test_signature_generation()

    # 最后测试爬虫集成
    success = test_xhs_crawler()

    if success:
        print("\n🎉 集成测试成功!")
        print("✅ 真实环境签名生成器已成功集成到爬虫中")
        print("✅ 包含完整的设备指纹和浏览器信息")
        print("✅ 包含会话标识和安全增强数据")
        print("✅ 包含调试和追踪信息")
        print("✅ 自动Cookie管理，避免过期问题")
        print("\n📋 功能特点:")
        print("- 动态生成真实设备ID和会话ID")
        print("- 模拟真实浏览器环境信息")
        print("- 包含硬件、WebGL、Canvas指纹")
        print("- 自动生成追踪ID和请求ID")
        print("- 智能Cookie管理，自动刷新过期Cookie")
        print("- 通过小红书服务器签名验证")
        print("- 避免登录过期问题")
    else:
        print("\n⚠️ 集成测试失败，需要进一步调试")

    # 爬取所有评论（主评论翻页 + 子评论补全）
    note_id = "699dd0b1000000001d024fe6"
    xsec_token = "ABsRvLIMkL008_96o22gryTaZWQ1hS6ndztRDFWXI1M5s="
    fetch_all_comments(note_id, xsec_token)
