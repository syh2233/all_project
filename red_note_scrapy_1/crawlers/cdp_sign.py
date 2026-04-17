#!/usr/bin/env python3
"""
CDP 签名生成器 - 通过 Chrome DevTools Protocol 调用浏览器中的真实 mnsv2 签名

使用前提：
1. Chrome 以调试模式启动（--remote-debugging-port=9222）
2. 已打开小红书页面并登录
3. 签名服务会自动注入

生成的签名是浏览器真实的 XYS_ 签名，可通过子评论接口的严格校验。
"""

import json
import os
import shutil
import subprocess
import time
from urllib import request as urllib_request
from urllib.parse import urlencode

# CDP 端口范围
CDP_PORTS = [9222, 9223, 9224, 9225, 9226, 9227, 9228, 9229, 9230]

# 缓存
_cdp_port = None
_service_injected = False

# Node.js CDP 桥接脚本（使用 Node.js 22+ 内置 WebSocket，回退到 require('ws')）
_NODE_CDP_BRIDGE = r"""
// cdp_bridge.js — 通过 CDP WebSocket 在浏览器中执行 JS 并返回结果
const wsUrl = process.argv[2];
const expr = process.argv[3];

let WS;
try { WS = WebSocket; } catch(e) { try { WS = require('ws'); } catch(e2) {
  // 最后尝试 Node.js 22+ 的全局 WebSocket
  if (typeof globalThis.WebSocket !== 'undefined') WS = globalThis.WebSocket;
  else { process.stderr.write('no_websocket'); process.exit(1); }
}}

const ws = new WS(wsUrl);
ws.onopen = () => {
  ws.send(JSON.stringify({
    id: 1,
    method: 'Runtime.evaluate',
    params: { expression: expr, returnByValue: true, awaitPromise: true }
  }));
};
ws.onmessage = (event) => {
  const msg = JSON.parse(typeof event.data === 'string' ? event.data : event.data.toString());
  if (msg.id === 1) {
    const val = msg.result && msg.result.result && msg.result.result.value;
    process.stdout.write(typeof val === 'string' ? val : JSON.stringify(val));
    ws.close();
    process.exit(0);
  }
};
ws.onerror = (e) => { process.stderr.write(e.message || 'ws_error'); process.exit(1); };
setTimeout(() => { process.stderr.write('timeout'); process.exit(1); }, 15000);
"""

# 签名服务注入脚本
_INJECT_SCRIPT = """
(async function() {
  if (window._signService && typeof window._signService.sign === 'function') {
    return JSON.stringify({ok: true, cached: true});
  }
  try {
    let wr;
    window.webpackChunkxhs_pc_web.push([['_cdp_svc_'], {}, (r) => { wr = r; }]);
    const h = wr(69431), m = wr(31547), u = wr(55340), sw = wr(4301);
    window._signService = {
      sign: function(apiPath) {
        let f = apiPath;
        const c = h.Pu([f].join("")), d = h.Pu(apiPath), s = window.mnsv2(f, c, d);
        const xs = "XYS_" + h.xE(h.lz(JSON.stringify({ x0: u.i8, x1: "xhs-pc-web", x2: window[u.mj] || "PC", x3: s, x4: "" })));
        const xt = String(Date.now());
        const platform = window[u.mj] || "PC", a1 = (document.cookie.match(/a1=([^;]+)/) || [])[1] || "";
        const b1 = localStorage.getItem('b1') || '', b1b1 = localStorage.getItem('b1b1') || '1';
        const sc = Number(sessionStorage.getItem('sc')) || 0; sessionStorage.setItem('sc', String(sc + 1));
        const dsl = window._dsl || '', x7 = dsl ? ";" + dsl : "";
        const xsc = h.xE(h.lz(JSON.stringify({ s0: sw.SW(platform), s1: "", x0: b1b1, x1: u.i8, x2: platform || "PC", x3: "xhs-pc-web", x4: "5.11.0", x5: a1, x6: xs, x7, x8: b1, x9: Number(h.tb("" + xs + x7 + b1)), x10: sc, x11: "normal", x12: localStorage.getItem('b1c1') || "" })));
        return JSON.stringify({ xs, xt, xsc });
      },
      // 签名+请求一体化（浏览器自带cookie，不需要Python传cookie）
      fetchApi: async function(apiPath) {
        const { xs, xt, xsc } = JSON.parse(this.sign(apiPath));
        const resp = await fetch('https://edith.xiaohongshu.com' + apiPath, {
          method: 'GET',
          headers: { 'accept': 'application/json, text/plain, */*', 'x-s': xs, 'x-t': xt, 'x-s-common': xsc },
          credentials: 'include'
        });
        const text = await resp.text();
        return JSON.stringify({ status: resp.status, body: text });
      }
    };
    return JSON.stringify({ok: true, cached: false});
  } catch(e) {
    return JSON.stringify({ok: false, error: e.message});
  }
})()
"""


def _find_node():
    """查找 Node.js"""
    node = shutil.which("node")
    if node:
        return node
    for path in [
        r"C:\Program Files\nodejs\node.exe",
        r"C:\Program Files (x86)\nodejs\node.exe",
        os.path.expanduser(r"~\AppData\Roaming\nvm\current\node.exe"),
    ]:
        if os.path.exists(path):
            return path
    return None


def _find_cdp_port():
    """扫描可用的 CDP 端口"""
    global _cdp_port
    if _cdp_port:
        try:
            with urllib_request.urlopen(
                f"http://127.0.0.1:{_cdp_port}/json/version", timeout=2
            ) as resp:
                if resp.status == 200:
                    return _cdp_port
        except Exception:
            _cdp_port = None

    for port in CDP_PORTS:
        try:
            with urllib_request.urlopen(
                f"http://127.0.0.1:{port}/json/version", timeout=1
            ) as resp:
                if resp.status == 200:
                    _cdp_port = port
                    return port
        except Exception:
            pass
    return None


def _find_xhs_page(port):
    """找到小红书页面的 WebSocket URL"""
    try:
        with urllib_request.urlopen(
            f"http://127.0.0.1:{port}/json/list", timeout=2
        ) as resp:
            targets = json.load(resp)
            for t in targets:
                url = t.get("url", "")
                if "xiaohongshu.com" in url and t.get("type") == "page":
                    return t.get("webSocketDebuggerUrl", ""), t.get("id", "")
    except Exception:
        pass
    return None, None


def _cdp_eval(expression, timeout=15):
    """通过 Node.js 桥接执行 CDP Runtime.evaluate"""
    port = _find_cdp_port()
    if not port:
        return None, "未找到 CDP 端口"

    ws_url, _ = _find_xhs_page(port)
    if not ws_url:
        return None, "未找到小红书页面"

    node = _find_node()
    if not node:
        return None, "未找到 Node.js"

    # 写入临时桥接脚本
    bridge_path = os.path.join(os.path.dirname(__file__), "_cdp_bridge.js")
    if not os.path.exists(bridge_path):
        with open(bridge_path, "w", encoding="utf-8") as f:
            f.write(_NODE_CDP_BRIDGE)

    try:
        result = subprocess.run(
            [node, bridge_path, ws_url, expression],
            capture_output=True,
            text=True,
            timeout=timeout + 5,
        )
        if result.returncode == 0 and result.stdout.strip():
            try:
                return json.loads(result.stdout.strip()), None
            except json.JSONDecodeError:
                return result.stdout.strip(), None
        else:
            err = result.stderr.strip() if result.stderr else "empty response"
            return None, err
    except subprocess.TimeoutExpired:
        return None, "CDP 桥接超时"
    except Exception as e:
        return None, str(e)


def _ensure_sign_service():
    """确保浏览器中已注入签名服务"""
    global _service_injected
    if _service_injected:
        # 快速检查是否还在
        result, err = _cdp_eval(
            "JSON.stringify({ok: typeof window._signService === 'object' && typeof window._signService.sign === 'function'})"
        )
        if result and isinstance(result, dict) and result.get("ok"):
            return True
        _service_injected = False

    result, err = _cdp_eval(_INJECT_SCRIPT)
    if err:
        print(f"  ❌ 注入签名服务失败: {err}")
        return False
    if isinstance(result, dict) and result.get("ok"):
        _service_injected = True
        return True
    print(f"  ❌ 签名服务注入异常: {result}")
    return False


def generate_cdp_sign(api_path, params):
    """
    通过 CDP 调用浏览器生成真实 XYS_ 签名

    Returns:
        dict: {"xs": "XYS_...", "xt": "...", "xsc": "..."} 或 None
    """
    if not _ensure_sign_service():
        return None

    query_string = urlencode(params)
    full_path = f"{api_path}?{query_string}"
    sign_expr = f"window._signService.sign({json.dumps(full_path)})"

    result, err = _cdp_eval(sign_expr)
    if err:
        print(f"  ❌ CDP 签名失败: {err}")
        return None
    return result


def cdp_fetch_api(api_path, params):
    """
    通过浏览器直接请求 API（签名+cookie 全由浏览器处理）

    Returns:
        dict: {"status": 200, "body": "..."} 或 None
    """
    if not _ensure_sign_service():
        return None

    query_string = urlencode(params)
    full_path = f"{api_path}?{query_string}"
    fetch_expr = f"window._signService.fetchApi({json.dumps(full_path)})"

    result, err = _cdp_eval(fetch_expr)
    if err:
        print(f"  ❌ CDP fetch 失败: {err}")
        return None

    if isinstance(result, dict) and "body" in result:
        try:
            result["data"] = json.loads(result["body"])
            del result["body"]
        except json.JSONDecodeError:
            pass
    return result


# === 测试 ===
if __name__ == "__main__":
    print("=== CDP 签名生成器测试 ===\n")

    port = _find_cdp_port()
    if port:
        print(f"✅ CDP 端口: {port}")
    else:
        print("❌ 未找到 CDP 端口")
        print("请以调试模式启动 Chrome:")
        print(
            '  "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"'
            " --remote-debugging-port=9222"
        )
        exit(1)

    ws_url, page_id = _find_xhs_page(port)
    if ws_url:
        print(f"✅ 小红书页面: {page_id}")
    else:
        print("❌ 未找到小红书页面")
        exit(1)

    print("\n注入签名服务...")
    if _ensure_sign_service():
        print("✅ 签名服务就绪")
    else:
        print("❌ 签名服务注入失败")
        exit(1)

    print("\n测试签名生成...")
    params = {
        "note_id": "699dd0b1000000001d024fe6",
        "root_comment_id": "699dd405000000000b036096",
        "num": "10",
        "cursor": "",
        "image_formats": "jpg,webp,avif",
        "top_comment_id": "",
        "xsec_token": "ABsRvLIMkL008_96o22gryTaZWQ1hS6ndztRDFWXI1M5s=",
    }
    result = generate_cdp_sign("/api/sns/web/v2/comment/sub/page", params)
    if result:
        print(f"✅ 签名: {result['xs'][:60]}...")
        print(f"  x-t: {result['xt']}")
        print(f"  x-s-common 长度: {len(result.get('xsc', ''))}")
    else:
        print("❌ 签名失败")

    print("\n测试浏览器代理请求...")
    proxy_result = cdp_fetch_api("/api/sns/web/v2/comment/sub/page", params)
    if proxy_result:
        print(f"✅ 状态: {proxy_result.get('status')}")
        if "data" in proxy_result:
            d = proxy_result["data"]
            print(f"  code: {d.get('code')}, msg: {d.get('msg')}")
            print(
                f"  子评论数: {len(d.get('data', {}).get('comments', []))}"
            )
    else:
        print("❌ 代理请求失败")
