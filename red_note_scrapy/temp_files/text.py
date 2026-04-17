import requests
import json
import time
import hashlib
from urllib.parse import urlencode


def test_sub_comment_api():
    """测试子评论API"""

    # 配置信息 - 替换为你的实际数据
    COOKIE = "gid=yj8D24fWSDv0yj8D24fK069V0yIY6AFDTDxSxyU1kTyk2428MD7AC4888W2q2Yy8fJ0KjyDJ; xsecappid=xhs-pc-web; abRequestId=f425aaf4-2614-55c8-b8d1-262c611be2ab; a1=198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479; webId=fc4fb0dccb1a480d5f17359394c861d7; webBuild=4.79.0; unread={%22ub%22:%2268b56bf2000000001c004134%22%2C%22ue%22:%2268a3fe26000000001c0126d1%22%2C%22uc%22:20}; web_session=040069b3ed6ebed4fbe38d058d3a4bf7c6f823; websectiga=a9bdcaed0af874f3a1431e94fbea410e8f738542fbb02df1e8e30c29ef3d91ac; loadts=1756917485564"
    NOTE_ID = "68a35fc0000000001c009cd9"
    ROOT_COMMENT_ID = "68a83b5900000000260052c3"
    CURSOR = "68a83ccd000000002700255f"
    REAL_XS_COMMON = "2UQAPsHC+aIjqArjwjHjNsQhPsHCH0rjNsQhPaHCH0c1Pjh9HjIj2eHjwjQgynEDJ74AHjIj2ePjwjQhyoPTqBPT49pjHjIj2ecjwjHFN0qEN0ZjNsQh+aHCH0rEweDIwBP9G0rFPA41PoD98/Q7qeSfy9QVyn+Tyn4I8BkfG9rlJ7qh+/ZIPeZ9+ecF+ADjNsQh+jHCHjHVHdW7H0ijHjIj2eWjwjQQPAYUaBzdq9k6qB4Q4fpA8b878FSet9RQzLlTcSiM8/+n4MYP8F8LagY/P9Ql4FpUzfpS2BcI8nT1GFbC/L88JdbFyrSiafp/8DMra7pFLDDAa7+8J7QgabmFz7Qjp0mcwp4fanD68p40+fp8qgzELLbILrDA+9p3JpH9LLI3+LSk+d+DJfRSL98lnLYl49IUqgcMc0mrJFShtMmozBD6qM8FyFSh8o+h4g4U+obFyLSi4nbQz/+SPFlnPrDApSzQcA4SPopFJeQmzBMA/o8Szb+NqM+c4ApQzg8Ayp8FaDRl4AYs4g4fLomD8pzBpFRQ2ezLanSM+Skc47Qc4gcMag8VGLlj87PAqgzhagYSqAbn4FYQy7pTanTQ2npx87+8NM4L89L78p+l4BL6ze4AzB+IygmS8Bp8qDzFaLP98Lzn4AQQzLEAL7bFJBEVL7pwyS8Fag868nTl4e+0n04ApfuF8FSbL7SQyrLharQl4LShyBEl20YdanTQ8fRl49TQcMkgwBuAq9zV/9pnLoqAag8m8/mf89pDzBY7aLpOqAbgtF8EqgzGanWA8/bDcnLAzDRApSm7/9pf/7+8qgcAagYLq94p+d+/4gqM/e4Nq98n494QPMQCa/PFP7Qn4FEY4gqUJ7+kG7SI87+D8/4Apdb7tFS3a9prPrbApDlacDS9+nphPBzS8rD3cDSe87+fLo4Hag8QzSbc4FYcpdzmagWM8/8M4o8Qy9RS+dp7+LSiP7+x4gqM/db7z9Rn47pQc7kLag8a4bbSpDboJsRAygbFzDSiLozQynpSngp7J9pgG9+IpLRAzo+34LSiLdSFLo472db7cLS38g+gqgzMqLSmqM8B+dPlanQPaLLIqA8S8o+kLoz0GMm7qDSeafpfpd4fanTdqAGIp9RQcFTS8Bu68p4n4e+QPA4Spdb7PAYsngQQyrW3aLP9q7YQJ9L9wg8S8oQOqMSc4FzQc9T7aLpkwobM4F+Qy7p7a/+O8n8S+ozdzrkSP7p7+LDA/eZUqg4Scfc68nSx8o+xqgzkz7bFJrSkqDlQcM+DJM8F+F4n4FTQcFbS8Si9q9Sc4URt4g4PanYBt9bM498Qc9M6cDDROaHVHdWEH0iT+APhP0LF+AGMNsQhP/Zjw0ZVHdWlPaHCHfE6qfMYJsQR"

    # 构建请求URL
    params = {
        "note_id": NOTE_ID,
        "root_comment_id": ROOT_COMMENT_ID,
        "num": 10,
        "cursor": CURSOR,
        "image_formats": "jpg,webp,avif",
        "top_comment_id": "",
        "xsec_token": "ABMARfqKuxx76hZj-CQH0D9AIHxh8oCmV_RTOxyE_DIpI="
    }

    url = f"https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page?{urlencode(params)}"

    # 生成X-s
    xs = generate_xs(url, params)

    # 设置请求头
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome / 91.0.4472.124 Safari / 537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": "https://www.xiaohongshu.com/",
        "Origin": "https://www.xiaongshu.com",
        "Cookie": COOKIE,
        "X-s": xs,
        "X-s-common": REAL_XS_COMMON,
        "X-t": str(int(time.time() * 1000))
    }

    print(f"请求URL: {url}")
    print(f"X-s: {xs}")
    print(f"X-s-common: {REAL_XS_COMMON[:50]}...")

    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"响应状态: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print("✅ 请求成功!")

            if "data" in data:
                comments = data["data"].get("comments", [])
                print(f"获取到 {len(comments)} 条子评论")

                for i, comment in enumerate(comments[:3]):
                    print(f"{i + 1}. {comment.get('user', {}).get('nickname', 'Unknown')}: {comment.get('content','No content')}")

                return True
        else:
            print(f"❌ 请求失败: {response.status_code}")
            print(f"响应内容: {response.text}")
            return False

    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return False


if __name__ == "__main__":
    test_sub_comment_api()