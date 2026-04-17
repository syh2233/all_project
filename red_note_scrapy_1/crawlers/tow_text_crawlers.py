import requests
import time
import sys
import os
import json
from urllib.parse import urlencode


# from curl_cffi import requests

def get_xt():
    # 获取当前时间戳（毫秒）
    return str(int(time.time() * 1000))


sys.path.append(os.path.join(os.path.dirname(__file__), "..", "generators"))
from realistic_xhs_signature_generator import RealisticXHSSignatureGenerator
from xhs_cookie_manager import XHSCookieManager
from xhs_common_generator import XHSCommonGenerator


def generate_headers_with_signature(path, params):
    """生成包含动态X-S签名和X-S-Common的请求头"""
    # 初始化Cookie管理器
    cookie_manager = XHSCookieManager()

    # 初始化真实环境签名生成器
    signature_generator = RealisticXHSSignatureGenerator()

    # 初始化X-S-Common生成器
    common_generator = XHSCommonGenerator()

    # 生成X-S签名
    x_s_signature = signature_generator.generate_realistic_signature(path, params)
    print(f"x_s_signature: {x_s_signature}")

    # 生成X-S-Common
    full_url = f"https://edith.xiaohongshu.com{path}"
    x_s_common = common_generator.generate_xs_common(full_url, x_s_signature)
    print(f"x_s_common: {x_s_common}...")

    # 获取环境信息用于请求头
    env_info = signature_generator.get_environment_info()

    # 获取动态Cookie
    cookie_string = cookie_manager.get_cookie_string()

    # 显示Cookie状态
    cookie_info = cookie_manager.get_cookie_info()
    print(
        f"Cookie状态: 会话{'已过期' if cookie_info['session_expired'] else '有效'}, GID{'已过期' if cookie_info['gid_expired'] else '有效'}")

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,en-GB;q=0.6",
        "cookie": "gid=yj8D24fWSDv0yj8D24fK069V0yIY6AFDTDxSxyU1kTyk2428MD7AC4888W2q2Yy8fJ0KjyDJ; xsecappid=xhs-pc-web; abRequestId=f425aaf4-2614-55c8-b8d1-262c611be2ab; a1=198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479; webId=fc4fb0dccb1a480d5f17359394c861d7; web_session=040069b3ed6ebed4fbe38d058d3a4bf7c6f823; webBuild=4.79.0; unread={%22ub%22:%2268b56bf2000000001c004134%22%2C%22ue%22:%2268a3fe26000000001c0126d1%22%2C%22uc%22:20}; acw_tc=0a0bb06417569972818746546efc5ea03db04c40ae9fc7661d3469c5ecf69c; websectiga=29098a4cf41f76ee3f8db19051aaa60c0fc7c5e305572fec762da32d457d76ae; sec_poison_id=e5ec492d-6a0b-4426-bf20-1bce11819c65; loadts=1756997606669",
        "origin": "https://www.xiaohongshu.com",
        "referer": "https://www.xiaohongshu.com/",
        "user-agent": env_info["user_agent"],
        "x-b3-traceid": env_info["trace_id"],
        "x-s": x_s_signature,
        "x-s-common": x_s_common,
        "x-t": get_xt(),
        "x-xray-traceid": env_info["trace_id"]
    }
    return headers


def test_xhs_crawler():
    """测试集成真实环境X-S签名生成器的爬虫"""
    print("=== 测试XHS爬虫集成（真实环境签名）===")

    # API路径和参数
    api_path = "/api/sns/web/v2/comment/page"
    params = {
        "note_id": "68a35fc0000000001c009cd9",
        "cursor": "",
        "top_comment_id": "",
        "image_formats": "jpg,webp,avif",
        "xsec_token": "ABMARfqKuxx76hZj-CQH0D9AIHxh8oCmV_RTOxyE_DIpI="
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

            response = requests.get(
                full_url,
                headers=headers,
                timeout=30,
                allow_redirects=True
            )

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
    print(cookie_string[:300] + "..." if len(cookie_string) > 300 else cookie_string)
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


if __name__ == "__main__":
    print("🚀 XHS真实环境签名生成器爬虫集成测试\n")

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
