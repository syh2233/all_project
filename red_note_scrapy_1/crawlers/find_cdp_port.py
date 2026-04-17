#!/usr/bin/env python3
"""扫描本机所有可能的 CDP 端口"""
import json
from urllib import request

print("扫描 CDP 端口 (9222-9300, 以及其他常见端口)...\n")

ports_to_check = list(range(9222, 9300)) + [
    # 常见 CDP 端口
    9515, 9516, 9517, 9518, 9519, 9520,
    # Playwright / Puppeteer 常用
    0,  # placeholder
    # 更大范围
] + list(range(9300, 9400)) + list(range(12222, 12240))

found = []
for port in ports_to_check:
    if port == 0:
        continue
    try:
        with request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=1) as resp:
            data = json.load(resp)
            browser = data.get("Browser", "unknown")
            ws_url = data.get("webSocketDebuggerUrl", "")
            print(f"  ✅ Port {port}: {browser}")
            print(f"     WebSocket: {ws_url}")
            found.append(port)

            # 也列出该端口的所有页面
            try:
                with request.urlopen(f"http://127.0.0.1:{port}/json/list", timeout=1) as resp2:
                    targets = json.load(resp2)
                    for t in targets:
                        print(f"     页面: {t.get('title', '?')[:50]} - {t.get('url', '?')[:80]}")
            except:
                pass
            print()
    except:
        pass

if not found:
    print("❌ 未找到任何 CDP 端口\n")
    print("请确保 Chrome 以调试模式启动：")
    print('  方法1: 先关闭所有 Chrome 窗口和进程，然后运行：')
    print('  "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\\chrome_debug_profile"')
    print()
    print('  方法2: 如果不想关闭现有 Chrome，用单独的用户目录：')
    print('  "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\\chrome_debug_profile"')
    print()
    print("  注意：--user-data-dir 必须指定，否则如果已有 Chrome 实例在运行，调试端口不会生效")
else:
    print(f"\n找到 {len(found)} 个 CDP 端口: {found}")
