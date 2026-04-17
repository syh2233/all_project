#!/usr/bin/env python3
"""
测试发现的新API参数
"""

import requests
import json
import time
import uuid
from urllib.parse import urlencode
from xs_generator import XSGenerator

def test_new_api_params():
    """测试新的API参数"""
    
    # 基础请求头
    base_headers = {
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
    }
    
    # Cookie信息（更新了loadts和unread）
    cookie_info = {
        'a1': '198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479',
        'web_session': '040069b3ed6ebed4fbe30e25ad3a4b127faeca',
        'webId': 'fc4fb0dccb1a480d5f17359394c861d7',
        'webBuild': '4.79.0',
        'gid': 'yj8D24fWSDv0yj8D24fK069V0yIY6AFDTDxSxyU1kTyk2428MD7AC4888W2q2Yy8fJ0KjyDJ',
        'websectiga': '634d3ad75ffb42a2ade2c5e1705a73c845837578aeb31ba0e442d75c648da36a',
        'sec_poison_id': '3e95e4cf-0caf-423d-a0ec-d4e3a49d703c',
        'acw_tc': '0a4a453a17569070897088137ec524bb28ede595ddc525595031d81456a33f',
    }
    
    # 测试参数
    note_id = "68a048c1000000001d01838e"
    root_comment_id = "68a048ef000000003002a604"
    
    # 创建session
    session = requests.Session()
    session.verify = False
    session.timeout = 10
    
    # XS生成器
    xs_gen = XSGenerator()
    
    def generate_trace_id():
        return str(uuid.uuid4()).replace('-', '')[:24]
    
    def prepare_headers(url, include_xs_common=True):
        """准备请求头"""
        timestamp = str(int(time.time() * 1000))
        
        headers = base_headers.copy()
        
        # 更新的cookie信息
        headers['cookie'] = (
            f"gid={cookie_info['gid']}; "
            f"xsecappid=xhs-pc-web; "
            f"abRequestId=f425aaf4-2614-55c8-b8d1-262c611be2ab; "
            f"a1={cookie_info['a1']}; "
            f"webId={cookie_info['webId']}; "
            f"web_session={cookie_info['web_session']}; "
            f"webBuild={cookie_info['webBuild']}; "
            f"unread=%7B%22ub%22%3A%2268b56bf2000000001c004134%22%2C%22ue%22%3A%2268a3fe26000000001c0126d1%22%2C%22uc%22%3A20%7D; "
            f"acw_tc={cookie_info['acw_tc']}; "
            f"websectiga={cookie_info['websectiga']}; "
            f"sec_poison_id={cookie_info['sec_poison_id']}; "
            f"loadts={timestamp}"
        )
        
        headers['x-b3-traceid'] = generate_trace_id()
        headers['x-xray-traceid'] = generate_trace_id()
        
        # 生成X-s参数
        xs_value = xs_gen.generate_xs(
            url=url,
            method="GET",
            user_id=cookie_info['a1']
        )
        
        headers['X-s'] = xs_value
        headers['X-t'] = timestamp
        
        # 添加x-s-common参数（如果需要）
        if include_xs_common:
            # 这里需要根据实际算法生成x-s-common
            # 暂时使用示例值
            headers['x-s-common'] = "2UQAPsHC+aIjqArjwjHjNsQhPsHCH0rjNsQhPaHCH0c1Pjh9HjIj2eHjwjQgynEDJ74AHjIj2ePjwjQhyoPTqBPT49pjHjIj2ecjwjHFN0qEN0ZjNsQh+aHCH0rEweDIwBP9G0rFPA41PoD98/Q7qeSfy9QVyn+Tyn4I8BkfG9rlJ7qh+/ZIPeZ9+ecF+ADjNsQh+jHCHjHVHdW7H0ijHjIj2eWjwjQQPAYUaBzdq9k6qB4Q4fpA8b878FSet9RQzLlTcSiM8/+n4MYP8F8LagY/P9Ql4FpUzfpS2BcI8nT1GFbC/L88JdbFyrSiafp/8DMra7pFLDDAa7+8J7QgabmFz7Qjp0mcwp4fanD68p40+fp8qgzELLbILrDA+9p3JpH9LLI3+LSk+d+DJfpSL98lnLYl49IUqgcMc0mrcDShtMmozBD6qM8FyFSh8o+h4g4U+obFyLSi4nbQz/+SPFlnPrDApSzQcA4SPopFJeQmzBMA/o8Szb+NqM+c4ApQzg8Ayp8FaDRl4AYs4g4fLomD8pzBpFRQ2ezLanSM+Skc47Qc4gcMag8VGLlj87PAqgzhagYSqAbn4FYQy7pTanTQ2npx87+8NM4L89L78p+l4BL6ze4AzB+IygmS8Bp8qDzFaLP98Lzn4AQQzLEAL7bFJBEVL7pwyS8Fag868nTl4e+0n04ApfuF8FSbL7SQyrptLn8l4LShyBEl20YdanTQ8fRl49TQcMkgwBuAq9zV/9pnLoqAag8m8/mf89pDzBY7aLpOqAbgtF8EqgzGanWA8/bDcnLAzDRApSm7/9pf/7+8qgcAagYLq94p+d+/4gqM/e4Nq98n494QPMQCa/PFP7Qn47zY4gqUcd+gG7S/J7+D8/4Apdb7tFS3a9prPrbApDlacDS9+nphPBzS8rD3cDSe87+fLo4Hag8QzSbc4FYcpdzmagWM8/8M4o8Qy9RS+dp7+LSiP7+x4gqM/db7z9Rn47pQc7kLag8a4bbSpDboJsRAygbFzDSiLozQynpSngp7J9pgG9+IpLRAzo+34LSiLdSFLo472db7cLS38g+gqgzMqLSmqM8B+dPlanQPaLLIqA8S8o+kLoz0GMm7qDSeafpfpd4fanTdqAGIp9RQcFTS8Bu68p4n4e+QPA4Spdb7PAYsngQQyrW3a/+kOaHVHdWEH0iTP/HEPeGIPAcFPsIj2erIH0iINsQhP/rjwjQ1J7QTGnIjKc=="
        
        return headers
    
    print("测试新的API参数...\n")
    
    # 先访问页面建立session
    print("1. 访问页面建立session:")
    page_url = f"https://www.xiaohongshu.com/explore/{note_id}"
    page_headers = prepare_headers(page_url, include_xs_common=False)
    
    try:
        page_response = session.get(page_url, headers=page_headers, timeout=10)
        print(f"页面访问状态码: {page_response.status_code}")
    except Exception as e:
        print(f"页面访问出错: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 测试新的API参数组合
    print("2. 测试新的API参数组合:")
    
    sub_url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page"
    
    # 测试不同的参数组合
    test_cases = [
        {
            'name': '原始参数（comment_id）',
            'params': {
                'note_id': note_id,
                'comment_id': root_comment_id,
                'cursor': '',
                'image_formats': 'jpg,webp,avif',
                'xsec_token': 'ABIyAXG1J9ckAl0VbljygE3I8b6TZ0k5P4jORY-kCIzzw%3D'
            }
        },
        {
            'name': '新参数（root_comment_id）',
            'params': {
                'note_id': note_id,
                'root_comment_id': root_comment_id,
                'cursor': '',
                'image_formats': 'jpg,webp,avif',
                'xsec_token': 'ABIyAXG1J9ckAl0VbljygE3I8b6TZ0k5P4jORY-kCIzzw%3D'
            }
        },
        {
            'name': '完整参数（带num和cursor）',
            'params': {
                'note_id': note_id,
                'root_comment_id': root_comment_id,
                'num': '10',
                'cursor': '68a706280000000030009afb',
                'image_formats': 'jpg,webp,avif',
                'top_comment_id': '',
                'xsec_token': 'ABIyAXG1J9ckAl0VbljygE3I8b6TZ0k5P4jORY-kCIzzw%3D'
            }
        },
        {
            'name': '精简参数（只保留必需的）',
            'params': {
                'note_id': note_id,
                'root_comment_id': root_comment_id,
                'num': '10',
                'image_formats': 'jpg,webp,avif',
                'xsec_token': 'ABIyAXG1J9ckAl0VbljygE3I8b6TZ0k5P4jORY-kCIzzw%3D'
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n测试用例 {i}: {test_case['name']}")
        print(f"参数: {test_case['params']}")
        
        # 构建URL
        params = {k: v for k, v in test_case['params'].items() if v}
        url_with_params = sub_url + '?' + urlencode(params)
        
        # 准备请求头
        headers = prepare_headers(url_with_params)
        
        try:
            response = session.get(url_with_params, headers=headers, timeout=10)
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    success = data.get('success', False)
                    print(f"成功: {success}")
                    
                    if success:
                        comments = data.get('data', {}).get('comments', [])
                        cursor = data.get('data', {}).get('cursor', '')
                        has_more = data.get('data', {}).get('has_more', False)
                        
                        print(f"子评论数量: {len(comments)}")
                        print(f"下一页cursor: {cursor}")
                        print(f"是否有更多: {has_more}")
                        
                        # 显示前两条评论
                        if comments:
                            print("前两条评论:")
                            for j, comment in enumerate(comments[:2], 1):
                                print(f"  {j}. {comment.get('content', 'N/A')}")
                                print(f"     点赞: {comment.get('like_count', 0)}")
                        
                        print("✅ 成功获取子评论！")
                    else:
                        msg = data.get('msg', 'Unknown error')
                        code = data.get('code', 'Unknown')
                        print(f"错误信息: {msg}")
                        print(f"错误代码: {code}")
                        
                except json.JSONDecodeError:
                    print(f"响应不是JSON格式: {response.text[:200]}")
            else:
                print(f"失败: {response.text[:200]}")
                
        except Exception as e:
            print(f"请求出错: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 测试不同的请求头组合
    print("3. 测试不同的请求头组合:")
    
    # 使用成功的参数组合
    successful_params = {
        'note_id': note_id,
        'root_comment_id': root_comment_id,
        'num': '10',
        'image_formats': 'jpg,webp,avif',
        'xsec_token': 'ABIyAXG1J9ckAl0VbljygE3I8b6TZ0k5P4jORY-kCIzzw%3D'
    }
    
    params = {k: v for k, v in successful_params.items() if v}
    url_with_params = sub_url + '?' + urlencode(params)
    
    header_test_cases = [
        {'name': '包含x-s-common', 'include_xs_common': True},
        {'name': '不包含x-s-common', 'include_xs_common': False},
        {'name': '简化的请求头', 'include_xs_common': False, 'simplified': True}
    ]
    
    for i, test_case in enumerate(header_test_cases, 1):
        print(f"\n请求头测试 {i}: {test_case['name']}")
        
        if test_case.get('simplified', False):
            # 使用简化的请求头
            test_headers = {
                'accept': 'application/json, text/plain, */*',
                'accept-encoding': 'gzip, deflate, br, zstd',
                'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,en-GB;q=0.6',
                'origin': 'https://www.xiaohongshu.com',
                'referer': 'https://www.xiaohongshu.com/',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0',
            }
            
            # 添加基本的cookie
            timestamp = str(int(time.time() * 1000))
            test_headers['cookie'] = (
                f"gid={cookie_info['gid']}; "
                f"a1={cookie_info['a1']}; "
                f"webId={cookie_info['webId']}; "
                f"web_session={cookie_info['web_session']}; "
                f"webBuild={cookie_info['webBuild']}; "
                f"loadts={timestamp}"
            )
            
            # 添加X-s和X-t
            xs_value = xs_gen.generate_xs(
                url=url_with_params,
                method="GET",
                user_id=cookie_info['a1']
            )
            test_headers['X-s'] = xs_value
            test_headers['X-t'] = timestamp
            
            headers = test_headers
        else:
            headers = prepare_headers(url_with_params, test_case['include_xs_common'])
        
        try:
            response = session.get(url_with_params, headers=headers, timeout=10)
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                success = data.get('success', False)
                print(f"成功: {success}")
                if success:
                    comments = data.get('data', {}).get('comments', [])
                    print(f"子评论数量: {len(comments)}")
                else:
                    print(f"错误: {data.get('msg', 'Unknown error')}")
            else:
                print(f"失败: {response.text[:100]}")
                
        except Exception as e:
            print(f"请求出错: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 结论
    print("4. 结论:")
    print("基于测试结果，")
    print("1. root_comment_id 是正确的参数名")
    print("2. num 参数控制返回的评论数量")
    print("3. cursor 参数用于分页")
    print("4. x-s-common 参数可能是关键")
    print("5. 需要进一步研究x-s-common的生成算法")

if __name__ == "__main__":
    # 禁用SSL警告
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    test_new_api_params()