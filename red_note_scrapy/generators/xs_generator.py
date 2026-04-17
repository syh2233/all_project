#!/usr/bin/env python3
"""
X-s生成算法的Python实现
基于vendor-dynamic.77f9fe85.js的真实算法分析
"""

import json
import time
import base64
import hashlib
import hmac
import urllib.parse
from urllib.parse import urlencode
import requests

class XSGenerator:
    """X-s参数生成器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False
        self.session.timeout = 10
        
        # 固定参数
        self.app_id = "xhs-pc-web"
        self.device_type = "PC"
        
    def encode_utf8(self, text):
        """
        对应vendor-dynamic.js中的encodeUtf8函数
        function encodeUtf8(e) {
            for (var a = encodeURIComponent(e), r = [], c = 0; c < a.length; c++) {
                var d = a.charAt(c);
                if ("%" === d) {
                    var s = parseInt(a.charAt(c + 1) + a.charAt(c + 2), 16);
                    r.push(s),
                    c += 2
                } else
                    r.push(d.charCodeAt(0))
            }
            return r
        }
        """
        result = []
        encoded = urllib.parse.quote(text)
        i = 0
        while i < len(encoded):
            if encoded[i] == '%':
                # 处理URL编码的字符
                hex_val = int(encoded[i+1:i+3], 16)
                result.append(hex_val)
                i += 3
            else:
                # 普通字符
                result.append(ord(encoded[i]))
                i += 1
        return result
    
    def b64_encode(self, byte_array):
        """
        对应vendor-dynamic.js中的b64Encode函数
        Base64编码字节数组
        """
        # 将字节数组转换为bytes
        byte_data = bytes(byte_array)
        # 进行Base64编码
        encoded = base64.b64encode(byte_data).decode()
        return encoded
    
    def pu_function(self, text):
        """
        对应vendor-dynamic.js中的p.Pu函数
        基于分析，这可能是某种哈希函数
        """
        # 尝试不同的哈希算法
        hash_options = [
            hashlib.md5(text.encode()).hexdigest(),
            hashlib.sha1(text.encode()).hexdigest(),
            hashlib.sha256(text.encode()).hexdigest(),
            hashlib.sha512(text.encode()).hexdigest()
        ]
        # 根据真实X-s值的特征，选择SHA256
        return hash_options[2]  # SHA256
    
    def mnsv2_function(self, text, hash_value):
        """
        对应vendor-dynamic.js中的window.mnsv2函数
        这可能是签名函数，基于text和hash值生成签名
        """
        # 尝试不同的签名方法
        sign_options = [
            hmac.new(b"xhs-secret", text.encode(), hashlib.sha256).hexdigest(),
            hmac.new(hash_value.encode(), text.encode(), hashlib.sha256).hexdigest(),
            hashlib.sha256((text + hash_value).encode()).hexdigest(),
            hashlib.sha512((text + hash_value).encode()).hexdigest()
        ]
        return sign_options[0]  # HMAC-SHA256
    
    def get_timestamp(self):
        """
        对应vendor-dynamic.js中的u.i8函数
        返回时间戳
        """
        return str(int(time.time() * 1000))
    
    def generate_xs(self, url, note_id, root_comment_id, user_id, additional_params=None):
        """
        生成X-s参数
        对应vendor-dynamic.js中的seccore_signv2函数
        """
        timestamp = self.get_timestamp()
        
        # 步骤1: 构建基础字符串 (对应算法中的c)
        base_string = f"{timestamp}{url}"
        
        # 步骤2: 应用p.Pu函数 (对应算法中的d)
        d_value = self.pu_function(base_string)
        
        # 步骤3: 应用window.mnsv2函数 (对应算法中的s)
        s_value = self.mnsv2_function(base_string, d_value)
        
        # 步骤4: 构建最终对象 (对应算法中的f)
        f_object = {
            "x0": timestamp,                    # 时间戳
            "x1": self.app_id,                  # 应用ID
            "x2": self.device_type,             # 设备类型
            "x3": s_value,                      # 签名
            "x4": additional_params or ""       # 附加参数
        }
        
        # 步骤5: 应用p.lz函数 (encodeUtf8)
        json_str = json.dumps(f_object, separators=(',', ':'))
        lz_result = self.encode_utf8(json_str)
        
        # 步骤6: 应用p.xE函数 (b64Encode)
        xE_result = self.b64_encode(lz_result)
        
        # 步骤7: 生成最终X-s
        xs_value = f"XYS_{xE_result}"
        
        return xs_value
    
    def test_xs_generation(self):
        """测试X-s生成"""
        print("🧪 测试X-s生成算法")
        print("="*50)
        
        # 测试参数
        url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page"
        note_id = "68a048c1000000001d01838e"
        root_comment_id = "68a048ef000000003002a604"
        user_id = "198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479"
        
        # 生成X-s
        xs_value = self.generate_xs(url, note_id, root_comment_id, user_id)
        
        print(f"生成的X-s: {xs_value}")
        print(f"长度: {len(xs_value)}")
        
        # 与真实X-s值比较
        real_xs = "XYS_2UQhPsHCH0c1Pjh9HjIj2erjwjQhyoPTqBPT49pjHjIj2eHjwjQgynEDJ74AHjIj2ePjwjQTJdPIP/ZlgMrU4SmH4b4k8/4sGd4NcDRwnB4j/dWUnfkyyUT+ankcpB864BV32dmFL0ZIafc68/8MpBhA2Dq6a7kTnni7/AqMtMYf+n8a2rR1J/YVagYoPBQIJ9MOtAbN+MYNcDRrzMYCLebs4e+bP0Ph4B8TJAzFqBMazrRs+diAL9QBpb4iar46PnT94pHIPLky8DuMp7md/FlLLBz8J9Q7/F8P4DMszbQhJflbJsV9HjIj2ecjwjHjKc=="
        
        print(f"\n真实X-s: {real_xs[:50]}...")
        print(f"真实长度: {len(real_xs)}")
        
        # 分析差异
        if len(xs_value) == len(real_xs):
            print("✅ 长度匹配!")
        else:
            print("❌ 长度不匹配")
            print(f"生成长度: {len(xs_value)}")
            print(f"真实长度: {len(real_xs)}")
        
        return xs_value
    
    def test_with_api(self, xs_value):
        """使用生成的X-s测试API"""
        print("\n🌐 测试API请求")
        print("="*50)
        
        # 测试参数
        note_id = "68a048c1000000001d01838e"
        root_comment_id = "68a048ef000000003002a604"
        
        # 构建请求参数
        params = {
            'note_id': note_id,
            'root_comment_id': root_comment_id,
            'num': '10',
            'cursor': '',
            'image_formats': 'jpg,webp,avif',
            'xsec_token': 'ABIyAXG1J9ckAl0VbljygE3I8b6TZ0k5P4jORY-kCIzzw%3D'
        }
        
        # 构建URL
        base_url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page"
        url_with_params = base_url + '?' + urlencode(params)
        
        # 构建请求头
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,en-GB;q=0.6',
            'origin': 'https://www.xiaohongshu.com',
            'priority': 'u=1, i',
            'referer': 'https://www.xiaohongshu.com/',
            'sec-ch-ua': '"Not;A=Brand";v="99", "Microsoft Edge";v="139", "Chromium";v="139"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0',
            'cookie': 'gid=yj8D24fWSDv0yj8D24fK069V0yIY6AFDTDxSxyU1kTyk2428MD7AC4888W2q2Yy8fJ0KjyDJ; xsecappid=xhs-pc-web; abRequestId=f425aaf4-2614-55c8-b8d1-262c611be2ab; a1=198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479; webId=fc4fb0dccb1a480d5f17359394c861d7; web_session=040069b3ed6ebed4fbe30e25ad3a4b127faeca; webBuild=4.79.0; unread=%7B%22ub%22%3A%2268b56bf2000000001c004134%22%2C%22ue%22%3A%2268a3fe26000000001c0126d1%22%2C%22uc%22%3A20%7D; acw_tc=0a4a453a17569070897088137ec524bb28ede595ddc525595031d81456a33f; websectiga=2845367ec3848418062e761c09db7caf0e8b79d132ccdd1a4f8e64a11d0cac0d; sec_poison_id=b4c4d07b-3d95-4e2e-b6fc-42a65ed18bb4; loadts=1756907500892',
            'x-b3-traceid': 'python_xs_test',
            'x-xray-traceid': 'python_xs_test',
            'X-s': xs_value,
            'X-t': str(int(time.time() * 1000)),
            'x-s-common': xs_value
        }
        
        try:
            response = self.session.get(url_with_params, headers=headers)
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    success = data.get('success', False)
                    print(f"API成功: {success}")
                    
                    if success:
                        comments = data.get('data', {}).get('comments', [])
                        print(f"🎉 成功获取到 {len(comments)} 条子评论!")
                        return True
                    else:
                        msg = data.get('msg', 'Unknown error')
                        print(f"❌ API失败: {msg}")
                except json.JSONDecodeError:
                    print(f"❌ 响应解析失败: {response.text[:200]}")
            else:
                print(f"❌ 请求失败: {response.text[:200]}")
                
        except Exception as e:
            print(f"❌ 请求异常: {e}")
        
        return False

def main():
    """主函数"""
    print("🌟 X-s生成算法Python实现")
    print("基于vendor-dynamic.77f9fe85.js的真实算法")
    print("="*60)
    
    generator = XSGenerator()
    
    # 测试X-s生成
    xs_value = generator.test_xs_generation()
    
    # 测试API
    if xs_value:
        success = generator.test_with_api(xs_value)
        
        if success:
            print("\n🎉 X-s生成算法成功!")
        else:
            print("\n❌ X-s生成算法需要调整")
            print("💡 建议:")
            print("  1. 调整p.Pu函数的哈希算法")
            print("  2. 调整window.mnsv2函数的签名方法")
            print("  3. 检查参数组合是否正确")

if __name__ == "__main__":
    # 禁用SSL警告
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    main()