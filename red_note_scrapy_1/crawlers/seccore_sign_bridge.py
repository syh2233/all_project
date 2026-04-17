"""
seccore 签名桥接 - 通过 Node.js seccore_sign.js 生成真实 mnsv2 签名

用法：
    from seccore_sign import generate_seccore_sign, start_seccore_server

    # 方式1：单次调用（每次启动 Node.js 进程，较慢）
    result = generate_seccore_sign("/api/sns/web/v2/comment/page?note_id=xxx")

    # 方式2：HTTP 服务模式（推荐，启动一次后复用）
    start_seccore_server()
    result = seccore_sign_via_server("/api/sns/web/v2/comment/page?note_id=xxx")
"""

import json
import os
import shutil
import subprocess
import time
from urllib import request as urllib_request
from urllib.parse import urlencode, quote

_server_port = 5679
_server_process = None
_node_path = None


def _find_node():
    """查找 Node.js"""
    global _node_path
    if _node_path:
        return _node_path
    node = shutil.which("node")
    if node:
        _node_path = node
        return node
    for path in [
        r"C:\Program Files\nodejs\node.exe",
        r"C:\Program Files (x86)\nodejs\node.exe",
        os.path.expanduser(r"~\AppData\Roaming\nvm\current\node.exe"),
    ]:
        if os.path.exists(path):
            _node_path = path
            return path
    return None


def _get_script_path():
    return os.path.join(os.path.dirname(__file__), "seccore_sign.js")


def generate_seccore_sign(api_url_with_params):
    """单次调用 Node.js 生成 mnsv2 签名（每次启动进程，约 3-5 秒）

    Args:
        api_url_with_params: 完整 API 路径含参数，如 "/api/sns/web/v2/comment/page?note_id=xxx"

    Returns:
        dict: {"mns": "mns0201_...", "md5": "..."} 或 None
    """
    node = _find_node()
    if not node:
        print("  ❌ 未找到 Node.js")
        return None

    script = _get_script_path()
    try:
        result = subprocess.run(
            [node, script, api_url_with_params],
            capture_output=True, timeout=60,
            encoding='utf-8', errors='replace',
        )
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout.strip())
            if "error" in data:
                print(f"  ❌ seccore 签名错误: {data['error']}")
                return None
            return data
        else:
            err = result.stderr.strip()[-200:] if result.stderr else "empty"
            print(f"  ❌ seccore 进程失败: {err}")
            return None
    except subprocess.TimeoutExpired:
        print("  ❌ seccore 签名超时")
        return None
    except Exception as e:
        print(f"  ❌ seccore 签名异常: {e}")
        return None


def start_seccore_server(port=5679):
    """启动 seccore HTTP 签名服务（后台进程）"""
    global _server_process, _server_port
    _server_port = port

    # 检查是否已在运行
    try:
        with urllib_request.urlopen(f"http://127.0.0.1:{port}/health", timeout=2) as resp:
            if resp.status == 200:
                print(f"  ✅ seccore 服务已在运行 (端口 {port})")
                return True
    except Exception:
        pass

    node = _find_node()
    if not node:
        print("  ❌ 未找到 Node.js")
        return False

    script = _get_script_path()
    _server_process = subprocess.Popen(
        [node, script, "--server", str(port)],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )

    # 等待服务启动
    for i in range(30):
        time.sleep(1)
        try:
            with urllib_request.urlopen(f"http://127.0.0.1:{port}/health", timeout=2) as resp:
                if resp.status == 200:
                    print(f"  ✅ seccore 服务已启动 (端口 {port})")
                    return True
        except Exception:
            pass
        if _server_process.poll() is not None:
            err = _server_process.stderr.read().decode()[-500:]
            print(f"  ❌ seccore 服务启动失败: {err}")
            return False

    print("  ❌ seccore 服务启动超时")
    return False


def seccore_sign_via_server(api_url_with_params, a1="", port=None):
    """通过 HTTP 服务获取 mnsv2 签名（毫秒级响应）

    Args:
        api_url_with_params: 完整 API 路径含参数
        a1: cookie 中的 a1 值（用于 x-s-common）

    Returns:
        dict: {"xs": "XYS_...", "xt": "...", "xsc": "..."} 或 None
    """
    p = port or _server_port
    try:
        url = f"http://127.0.0.1:{p}/sign?url={quote(api_url_with_params, safe='')}&a1={quote(a1, safe='')}"
        with urllib_request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            if "error" in data:
                print(f"  ❌ seccore 签名错误: {data['error']}")
                return None
            return data
    except Exception as e:
        print(f"  ❌ seccore 服务请求失败: {e}")
        return None


def stop_seccore_server():
    """停止 seccore 服务"""
    global _server_process
    if _server_process:
        _server_process.terminate()
        _server_process = None


# === 测试 ===
if __name__ == "__main__":
    print("=== seccore 签名桥接测试 ===\n")

    test_url = "/api/sns/web/v2/comment/page?note_id=699dd0b1000000001d024fe6&cursor=&top_comment_id=&image_formats=jpg,webp,avif"

    print("1. 单次调用模式:")
    result = generate_seccore_sign(test_url)
    if result:
        print(f"  mns: {result['mns'][:60]}... (长度: {len(result['mns'])})")
        print(f"  md5: {result['md5']}")
    else:
        print("  失败")

    print("\n2. HTTP 服务模式:")
    if start_seccore_server():
        result2 = seccore_sign_via_server(test_url)
        if result2:
            print(f"  mns: {result2['mns'][:60]}... (长度: {len(result2['mns'])})")
        else:
            print("  失败")
        stop_seccore_server()
