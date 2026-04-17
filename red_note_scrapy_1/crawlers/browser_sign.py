#!/usr/bin/env python3
"""
Node.js 签名生成器 - 通过 Node.js 执行小红书 DS 脚本生成真实 XYW_ 签名
不依赖浏览器，只需要 Node.js 运行时
"""

import json
import subprocess
import os
import time
import shutil
from urllib.parse import urlencode
from urllib import request as urllib_request

# Node.js 签名服务的端口
SIGN_SERVER_PORT = 5678
_sign_server_process = None


def _find_node():
    """查找 Node.js 可执行文件"""
    node = shutil.which("node")
    if node:
        return node
    # Windows 常见路径
    for path in [
        r"C:\Program Files\nodejs\node.exe",
        r"C:\Program Files (x86)\nodejs\node.exe",
        os.path.expanduser(r"~\AppData\Roaming\nvm\current\node.exe"),
    ]:
        if os.path.exists(path):
            return path
    return None


def _get_sign_script_path():
    """获取 node_sign.js 的路径"""
    return os.path.join(os.path.dirname(__file__), "node_sign.js")


def _start_sign_server():
    """启动 Node.js 签名 HTTP 服务（后台进程）"""
    global _sign_server_process

    if _sign_server_process and _sign_server_process.poll() is None:
        # 服务已在运行，检查健康状态
        try:
            with urllib_request.urlopen(
                f"http://127.0.0.1:{SIGN_SERVER_PORT}/health", timeout=2
            ) as resp:
                if resp.status == 200:
                    return True
        except Exception:
            # 服务不响应，杀掉重启
            _sign_server_process.kill()
            _sign_server_process = None

    node = _find_node()
    if not node:
        print("  ❌ 未找到 Node.js，请安装 Node.js")
        return False

    script = _get_sign_script_path()
    if not os.path.exists(script):
        print(f"  ❌ 签名脚本不存在: {script}")
        return False

    print(f"  启动 Node.js 签名服务 (port={SIGN_SERVER_PORT})...")
    _sign_server_process = subprocess.Popen(
        [node, script, "--server", str(SIGN_SERVER_PORT)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=os.path.dirname(script),
    )

    # 等待服务启动
    for i in range(30):
        time.sleep(1)
        try:
            with urllib_request.urlopen(
                f"http://127.0.0.1:{SIGN_SERVER_PORT}/health", timeout=2
            ) as resp:
                if resp.status == 200:
                    print(f"  ✅ Node.js 签名服务已启动")
                    return True
        except Exception:
            pass

        # 检查进程是否已退出
        if _sign_server_process.poll() is not None:
            stderr = _sign_server_process.stderr.read().decode("utf-8", errors="replace")
            print(f"  ❌ Node.js 签名服务启动失败: {stderr[:500]}")
            _sign_server_process = None
            return False

    print("  ❌ Node.js 签名服务启动超时")
    return False


def _call_sign_server(api_url):
    """通过 HTTP 调用签名服务"""
    url = f"http://127.0.0.1:{SIGN_SERVER_PORT}/sign?url={urllib_request.quote(api_url)}"
    try:
        with urllib_request.urlopen(url, timeout=15) as resp:
            return json.load(resp)
    except Exception as e:
        return {"error": str(e)}


def _call_sign_once(api_url):
    """单次调用 Node.js 生成签名（不启动服务）"""
    node = _find_node()
    if not node:
        return {"error": "Node.js not found"}

    script = _get_sign_script_path()
    try:
        result = subprocess.run(
            [node, script, api_url],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=os.path.dirname(script),
        )
        if result.returncode == 0:
            return json.loads(result.stdout.strip())
        else:
            return {"error": result.stderr[:500]}
    except subprocess.TimeoutExpired:
        return {"error": "Node.js sign timeout"}
    except Exception as e:
        return {"error": str(e)}


def generate_browser_sign(api_path, params):
    """
    生成真实 x-s 签名（兼容旧接口名）

    优先使用 HTTP 服务模式（快），失败则用单次调用模式

    Args:
        api_path: API 路径，如 /api/sns/web/v2/comment/sub/page
        params: 查询参数字典

    Returns:
        dict: {"xs": "XYW_...", "xt": "1234567890"} 或 None
    """
    query_string = urlencode(params)
    full_url = f"{api_path}?{query_string}"

    # 方式1: 尝试 HTTP 服务模式
    try:
        with urllib_request.urlopen(
            f"http://127.0.0.1:{SIGN_SERVER_PORT}/health", timeout=1
        ) as resp:
            if resp.status == 200:
                result = _call_sign_server(full_url)
                if result and "error" not in result:
                    return result
    except Exception:
        pass

    # 方式2: 启动服务再调用
    if _start_sign_server():
        result = _call_sign_server(full_url)
        if result and "error" not in result:
            return result
        if result:
            print(f"  ⚠️ 签名服务返回错误: {result.get('error')}")

    # 方式3: 单次调用模式
    print("  尝试单次调用模式...")
    result = _call_sign_once(full_url)
    if result and "error" not in result:
        return result

    if result:
        print(f"  ❌ Node.js 签名失败: {result.get('error')}")
    return None


# === 测试 ===
if __name__ == "__main__":
    print("=== Node.js 签名生成器测试 ===\n")

    node = _find_node()
    if node:
        print(f"✅ Node.js: {node}")
    else:
        print("❌ 未找到 Node.js")
        exit(1)

    params = {
        "note_id": "699dd0b1000000001d024fe6",
        "root_comment_id": "699dd405000000000b036096",
        "num": "10",
        "cursor": "",
        "image_formats": "jpg,webp,avif",
        "top_comment_id": "",
        "xsec_token": "ABsRvLIMkL008_96o22gryTaZWQ1hS6ndztRDFWXI1M5s=",
    }

    result = generate_browser_sign("/api/sns/web/v2/comment/sub/page", params)
    if result:
        print(f"✅ 签名生成成功:")
        print(f"  x-s: {result['xs'][:60]}...")
        print(f"  x-t: {result['xt']}")
    else:
        print("❌ 签名生成失败")
