#!/usr/bin/env python3
"""
XHS X-S-Common 参数生成器
基于逆向分析的xsCommon函数实现
"""

import json
import time
from urllib.parse import quote


# 自定义 Base64 字母表（从 vendor-dynamic.77f9fe85.js 第 12906 行提取）
_CUSTOM_B64_CHARS = "ZmserbBoHQtNP+wOcza/LpngG8yJq42KWYj0DSfdikx3VT16IlUAFM97hECvuRX5"


def _encode_utf8(text):
    """encodeUtf8 — 将字符串转为 UTF-8 字节列表（对应 JS p.lz）"""
    encoded = quote(text, safe='')  # 等价于 JS encodeURIComponent
    result = []
    i = 0
    while i < len(encoded):
        ch = encoded[i]
        if ch == '%':
            result.append(int(encoded[i+1:i+3], 16))
            i += 3
        else:
            result.append(ord(ch))
            i += 1
    return result


def _b64_encode(byte_list):
    """b64Encode — 使用自定义字母表编码（对应 JS p.xE）"""
    c = _CUSTOM_B64_CHARS
    n = len(byte_list)
    remainder = n % 3
    parts = []

    # 处理完整的 3 字节组
    i = 0
    end = n - remainder
    while i < end:
        # 每次最多处理 16383 字节（与 JS 一致）
        chunk_end = min(i + 16383, end)
        chunk_parts = []
        while i < chunk_end:
            triplet = (byte_list[i] << 16) + (byte_list[i+1] << 8) + byte_list[i+2]
            chunk_parts.append(
                c[(triplet >> 18) & 63] +
                c[(triplet >> 12) & 63] +
                c[(triplet >> 6) & 63] +
                c[triplet & 63]
            )
            i += 3
        parts.append(''.join(chunk_parts))

    # 处理剩余字节
    if remainder == 1:
        a = byte_list[n - 1]
        parts.append(c[a >> 2] + c[(a << 4) & 63] + '==')
    elif remainder == 2:
        a = (byte_list[n - 2] << 8) + byte_list[n - 1]
        parts.append(c[(a >> 10)] + c[(a >> 4) & 63] + c[(a << 2) & 63] + '=')

    return ''.join(parts)


def encode_xs_common(json_str):
    """完整的 x-s-common 编码流程：JSON → encodeUtf8 → b64Encode（自定义字母表）"""
    byte_list = _encode_utf8(json_str)
    return _b64_encode(byte_list)


class XHSCommonGenerator:
    """XHS X-S-Common参数生成器 — 基于 vendor-dynamic.77f9fe85.js 逆向"""

    # CRC32 查找表（多项式 0xedb88320）
    _crc_table = None

    def __init__(self):
        self.app_id = "xhs-pc-web"
        self.app_version = "5.11.0"  # 与浏览器一致
        self._sig_count = 0  # sessionStorage "sc"（浏览器中从 0 开始）
        if XHSCommonGenerator._crc_table is None:
            XHSCommonGenerator._crc_table = self._build_crc_table()

    @staticmethod
    def _build_crc_table():
        poly = 0xEDB88320
        table = []
        for i in range(256):
            r = i
            for _ in range(8):
                r = (r >> 1) ^ poly if (r & 1) else r >> 1
            table.append(r & 0xFFFFFFFF)
        return table

    @staticmethod
    def _crc32(text):
        """CRC32 — 对应 JS p.tb，与浏览器实现一致"""
        t = XHSCommonGenerator._crc_table
        if t is None:
            XHSCommonGenerator._crc_table = XHSCommonGenerator._build_crc_table()
            t = XHSCommonGenerator._crc_table
        c = 0xFFFFFFFF  # -1 as unsigned
        for ch in text:
            c = t[(c ^ ord(ch)) & 0xFF] ^ (c >> 8)
        return str(((~c) ^ 0xEDB88320) & 0xFFFFFFFF)

    def _get_a1_from_cookie(self):
        """从真实 cookie 中读取 a1 值"""
        try:
            import sys, os
            sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
            from real_cookie_manager import RealCookieManager
            cm = RealCookieManager()
            cookie_dict = cm.get_cookie_dict()
            if cookie_dict:
                return cookie_dict.get("a1", "")
        except Exception:
            pass
        return ""

    def generate_xs_common(self, url, x_s_signature, platform="Windows"):
        """生成 X-S-Common 参数"""
        if "/api/" not in url:
            return ""

        a1_value = self._get_a1_from_cookie()

        # x8: 浏览器指纹数据（从真实浏览器会话中提取）
        # 这是 localStorage "b1" 的值，包含设备/浏览器指纹信息
        x8_value = (
            "I38rHdgsjopgIvesdVwgIC+oIELmBZ5e3VwXLgFTIxS3bqwErFeexd0e"
            "kncAzMFYnqthIhJed9MDKutRI3KsYorWHPtGrbi0P9WfIi/eWc6eYqty"
            "QApPI37ekmR6QL+5Ii6sdnoeSfqYHqwl2qt5B0DoIx+PGDi/sVtkIx0s"
            "xuwr4qtiIhuaIE3e3LV0I3VTIC7e0utl2ADmsLveDSKsSPw5IEvsiVtJ"
            "Oqw8BuwfPpdeTFWOIx4TIiu6ZPwrPut5IvlaLbgs3qtxIxes1VwHIkum"
            "IkIyejgsY/WTge7eSqte/D7sDcpipedeYrDtIC6eDVw2IENsSqtlnlSu"
            "NjVtIvoekqt3cZ7sVo4gIESyIhE8HfquIxhnqz8gIkIfoqwkICZWG73s"
            "dlOeVPw3IvAe0fged0kJIi5s3IrF2utAIiKsidvekZNeTPt4nAOeWPwE"
            "IvYacAdeSuwEpBosfPwrI3RrIxE5Luwwaqw+rekhZANe1MNe0Pw9ICNs"
            "VLoeSbIFIkosSr7sVnFiIkgsVVtMIiudqqw+tqtWI30e3PwjIENeTVth"
            "Ih/sYqtSGqwymPwDIvIkI3It4aGS4Y/eiutjIimrIEOsSVtzBoFM/9ve"
            "j9ZvIiENGutzrutlIvve3PtUOpKeVWAs3phwIhos39Os3utscPwaICJsW"
            "Pw5IigekeqLICKejd/sfPt5Ix7sxuwD4mDnIib4IxNe3/0sTavsdIeek"
            "PwBIhSxICF5/PwsI3PFIiOe3Y8MzsJeWuteIE++puwImZeedMAeWVwmm"
            "ut2IiM9IhhQLPwJ8qtpI35sDAgeDPwdnVtjIEYyQut2Ikrzo0quIkes"
            "Vo6s07Ke6VwFHVtNIiPQIkos6VtRIEveYf8sIhYsQIlXIEF8Ixve0uw"
            "xoutoOqtxI3DkIh6sSANeVVwhprFMICD4KutheVtoIxqkI34LIkSiIE6e"
            "ir5sVpz1bVwJICLEcuwLrVwMIEveVMH/IxGJqpKexVtZ+ut9PacWPFiE"
            "Ii81zVw+Ik7s6z4eIiYQmVt7Iiq="
        )

        # x9: CRC32 哈希（浏览器中是数字类型）
        x9_value = int(self._crc32("" + "" + x8_value))

        # x12: 时间戳对（localStorage 中的访问记录）
        # 格式: "毫秒时间戳;毫秒时间戳"
        now_ms = int(time.time() * 1000)
        x12_value = f"{now_ms};{now_ms - 2933710000}"  # 模拟两个时间戳

        y = {
            "s0": 5,                          # 数字 5（不是字符串 "win32"）
            "s1": "",                          # 固定空
            "x0": "1",                         # localStorage "b1b1" 默认值 "1"
            "x1": "4.3.1",                    # SDK 版本号
            "x2": platform or "Windows",       # "Windows"（不是 "PC"）
            "x3": self.app_id,
            "x4": self.app_version,            # "5.11.0"
            "x5": a1_value,                   # cookie "a1" 值
            "x6": "",                          # 通常为空
            "x7": "",                          # 通常为空
            "x8": x8_value,                   # 浏览器指纹数据
            "x9": x9_value,                   # CRC32 哈希（数字类型）
            "x10": self._sig_count,           # 签名计数（从 0 开始）
            "x11": "normal",
            "x12": x12_value                  # 时间戳对
        }

        json_str = json.dumps(y, separators=(',', ':'), ensure_ascii=False)
        self._sig_count += 1  # 递增签名计数（下次调用时 x10 会 +1）
        return encode_xs_common(json_str)
    


if __name__ == "__main__":
    gen = XHSCommonGenerator()
    url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/page"
    xs = gen.generate_xs_common(url, "XYS_test")
    print(f"x-s-common: {xs[:60]}...")
    print(f"长度: {len(xs)}")
    print(f"sig_count: {gen._sig_count}")