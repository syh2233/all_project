#!/usr/bin/env python3
"""
使用现有X-s和X-s-common算法解决406错误的完整解决方案
结合 working_xs_generator.py 和 xiaohongshu_xs_common_generator.py
"""

import json
import time
import requests
from urllib.parse import urlencode
from working_xs_generator import WorkingXSGenerator
from xiaohongshu_xs_common_generator import XiaohongshuXSCommonGenerator


class XiaohongshuSubCommentCrawler:
    """小红书子评论爬取器 - 解决406错误"""
    
    def __init__(self):
        # 初始化X-s生成器（使用已验证的working版本）
        self.xs_generator = WorkingXSGenerator()
        
        # 初始化X-s-common生成器
        self.xs_common_generator = XiaohongshuXSCommonGenerator()
        
        # 设置请求session
        self.session = requests.Session()
        self.session.verify = False
        self.session.timeout = 10
        
        # 固定参数
        self.base_url = "https://edith.xiaohongshu.com"
        
    def generate_headers(self, url, user_id="", cookie="gid=yj8D24fWSDv0yj8D24fK069V0yIY6AFDTDxSxyU1kTyk2428MD7AC4888W2q2Yy8fJ0KjyDJ; xsecappid=xhs-pc-web; abRequestId=f425aaf4-2614-55c8-b8d1-262c611be2ab; a1=198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479; webId=fc4fb0dccb1a480d5f17359394c861d7; webBuild=4.79.0; unread={%22ub%22:%2268b56bf2000000001c004134%22%2C%22ue%22:%2268a3fe26000000001c0126d1%22%2C%22uc%22:20}; web_session=040069b3ed6ebed4fbe38d058d3a4bf7c6f823; websectiga=a9bdcaed0af874f3a1431e94fbea410e8f738542fbb02df1e8e30c29ef3d91ac; loadts=1756917485564"):
        """生成完整的请求头，包含X-s和X-s-common"""
        timestamp = str(int(time.time() * 1000))
        
        # 生成X-s参数
        xs_value = self.xs_generator.generate_xs(
            url=url,
            method="GET",
            user_id=user_id
        )
        
        # 生成X-s-common参数
        xs_common_value = "2UQAPsHC+aIjqArjwjHjNsQhPsHCH0rjNsQhPaHCH0c1Pjh9HjIj2eHjwjQgynEDJ74AHjIj2ePjwjQhyoPTqBPT49pjHjIj2ecjwjHFN0qEN0ZjNsQh+aHCH0rEweDIwBP9G0rFPA41PoD98/Q7qeSfy9QVyn+Tyn4I8BkfG9rlJ7qh+/ZIPeZ9+ecF+ADjNsQh+jHCHjHVHdW7H0ijHjIj2eWjwjQQPAYUaBzdq9k6qB4Q4fpA8b878FSet9RQzLlTcSiM8/+n4MYP8F8LagY/P9Ql4FpUzfpS2BcI8nT1GFbC/L88JdbFyrSiafp/8DMra7pFLDDAa7+8J7QgabmFz7Qjp0mcwp4fanD68p40+fp8qgzELLbILrDA+9p3JpH9LLI3+LSk+d+DJfRSL98lnLYl49IUqgcMc0mrJFShtMmozBD6qM8FyFSh8o+h4g4U+obFyLSi4nbQz/+SPFlnPrDApSzQcA4SPopFJeQmzBMA/o8Szb+NqM+c4ApQzg8Ayp8FaDRl4AYs4g4fLomD8pzBpFRQ2ezLanSM+Skc47Qc4gcMag8VGLlj87PAqgzhagYSqAbn4FYQy7pTanTQ2npx87+8NM4L89L78p+l4BL6ze4AzB+IygmS8Bp8qDzFaLP98Lzn4AQQzLEAL7bFJBEVL7pwyS8Fag868nTl4e+0n04ApfuF8FSbL7SQyrLharQl4LShyBEl20YdanTQ8fRl49TQcMkgwBuAq9zV/9pnLoqAag8m8/mf89pDzBY7aLpOqAbgtF8EqgzGanWA8/bDcnLAzDRApSm7/9pf/7+8qgcAagYLq94p+d+/4gqM/e4Nq98n494QPMQCa/PFP7Qn4FEY4gqUJ7+kG7SI87+D8/4Apdb7tFS3a9prPrbApDlacDS9+nphPBzS8rD3cDSe87+fLo4Hag8QzSbc4FYcpdzmagWM8/8M4o8Qy9RS+dp7+LSiP7+x4gqM/db7z9Rn47pQc7kLag8a4bbSpDboJsRAygbFzDSiLozQynpSngp7J9pgG9+IpLRAzo+34LSiLdSFLo472db7cLS38g+gqgzMqLSmqM8B+dPlanQPaLLIqA8S8o+kLoz0GMm7qDSeafpfpd4fanTdqAGIp9RQcFTS8Bu68p4n4e+QPA4Spdb7PAYsngQQyrW3aLP9q7YQJ9L9wg8S8oQOqMSc4FzQc9T7aLpkwobM4F+Qy7p7a/+O8n8S+ozdzrkSP7p7+LDA/eZUqg4Scfc68nSx8o+xqgzkz7bFJrSkqDlQcM+DJM8F+F4n4FTQcFbS8Si9q9Sc4URt4g4PanYBt9bM498Qc9M6cDDROaHVHdWEH0iT+APhP0LF+AGMNsQhP/Zjw0ZVHdWlPaHCHfE6qfMYJsQR"
        
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,en-GB;q=0.6',
            'origin': 'https://www.xiaohongshu.com',
            'priority': 'u=1, i',
            'referer': 'https://www.xiaohongshu.com/',
            'sec-ch-ua': '"Not;A=Brand";v="99", "Microsoft Edge";v="139", "Chromium";;v="139"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0',
            'x-b3-traceid': f'python_crawler_{timestamp}',
            'x-xray-traceid': f'python_crawler_{timestamp}',
            'X-s': xs_value,
            'X-t': timestamp,
            'x-s-common': xs_common_value
        }
        
        # 添加cookie
        if cookie:
            headers['cookie'] = cookie
            
        return headers
    
    def get_sub_comments(self, note_id, root_comment_id, cookie, xsec_token, num=10, cursor=""):
        """
        获取子评论
        
        Args:
            note_id: 笔记ID
            root_comment_id: 根评论ID
            cookie: 用户cookie
            xsec_token: 安全令牌
            num: 获取数量
            cursor: 分页游标
            
        Returns:
            dict: API响应结果
        """
        # 构建请求参数
        params = {
            'note_id': note_id,
            'root_comment_id': root_comment_id,
            'num': str(num),
            'cursor': cursor,
            'image_formats': 'jpg,webp,avif',
            'xsec_token': xsec_token
        }
        
        # 构建完整URL
        api_url = f"{self.base_url}/api/sns/web/v2/comment/sub/page"
        url_with_params = api_url + '?' + urlencode(params)
        
        # 生成请求头
        headers = self.generate_headers(url_with_params, cookie=cookie)
        
        print(f"🔍 正在请求子评论...")
        print(f"URL: {url_with_params}")
        print(f"X-s: {headers['X-s'][:50]}...")
        print(f"X-s-common: {headers['x-s-common'][:50]}...")
        
        try:
            response = self.session.get(url_with_params, headers=headers)
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    success = data.get('success', False)
                    
                    if success:
                        comments = data.get('data', {}).get('comments', [])
                        total_count = data.get('data', {}).get('total_count', 0)
                        
                        print(f"✅ 成功获取 {len(comments)} 条子评论 (总共 {total_count} 条)")
                        return {
                            'success': True,
                            'data': data,
                            'comments': comments,
                            'total_count': total_count
                        }
                    else:
                        msg = data.get('msg', 'Unknown error')
                        print(f"❌ API失败: {msg}")
                        return {
                            'success': False,
                            'error': msg,
                            'status_code': response.status_code
                        }
                        
                except json.JSONDecodeError:
                    print(f"❌ JSON解析失败: {response.text[:200]}")
                    return {
                        'success': False,
                        'error': 'JSON解析失败',
                        'response_text': response.text[:500]
                    }
            else:
                print(f"❌ 请求失败: {response.text[:200]}")
                return {
                    'success': False,
                    'error': f'HTTP {response.status_code}',
                    'response_text': response.text[:500]
                }
                
        except Exception as e:
            print(f"❌ 请求异常: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def test_with_real_data(self):
        """使用真实数据测试"""
        print("🧪 测试子评论获取 - 解决406错误")
        print("="*60)
        
        # 从page.json获取的真实数据
        note_id = "68a35fc0000000001c009cd9"
        root_comment_id = "68a83b5900000000260052c3"
        
        # 你提供的cookie
        cookie = "gid=yj8D24fWSDv0yj8D24fK069V0yIY6AFDTDxSxyU1kTyk2428MD7AC4888W2q2Yy8fJ0KjyDJ; xsecappid=xhs-pc-web; abRequestId=f425aaf4-2614-55c8-b8d1-262c611be2ab; a1=198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479; webId=fc4fb0dccb1a480d5f17359394c861d7; webBuild=4.79.0; unread=%7B%22ub%22%3A%2268b56bf2000000001c004134%22%2C%22ue%22%3A%2268a3fe26000000001c0126d1%22%2C%22uc%22%3A20%7D; web_session=040069b3ed6ebed4fbe38d058d3a4bf7c6f823; loadts=1756911545822; websectiga=10f9a40ba454a07755a08f27ef8194c53637eba4551cf9751c009d9afb564467"
        
        # 从page.json获取的xsec_token
        xsec_token = "ABMARfqKuxx76hZj-CQH0D9AIHxh8oCmV_RTOxyE_DIpI="
        
        # 获取子评论
        result = self.get_sub_comments(
            note_id=note_id,
            root_comment_id=root_comment_id,
            cookie=cookie,
            xsec_token=xsec_token,
            num=10,
            cursor=""
        )
        
        return result


def main():
    """主函数"""
    # 禁用SSL警告
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    print("🌟 小红书子评论爬取器 - 解决406错误方案")
    print("使用现有的X-s和X-s-common生成算法")
    print("="*60)
    
    crawler = XiaohongshuSubCommentCrawler()
    result = crawler.test_with_real_data()
    
    if result['success']:
        print("\n🎉 成功解决406错误！")
        print("📋 子评论数据:")
        for i, comment in enumerate(result['comments'][:3], 1):
            print(f"   {i}. {comment.get('content', 'N/A')[:50]}...")
    else:
        print(f"\n❌ 仍然存在问题: {result.get('error', 'Unknown error')}")
        print("💡 可能的解决方案:")
        print("   1. 检查cookie是否有效")
        print("   2. 验证note_id和root_comment_id是否正确")
        print("   3. 确认xsec_token是否需要（某些API可能需要）")


if __name__ == "__main__":
    main()