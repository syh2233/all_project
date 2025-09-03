#!/usr/bin/env python3
"""
调试脚本 - 找出字符串和整数比较错误的具体位置
"""

import sys
import traceback
import warnings

# 禁用警告
warnings.filterwarnings('ignore')

def debug_crawler():
    try:
        # 导入爬虫类
        from xiaohongshu_crawler import XiaoHongShuCrawler
        
        print("创建爬虫实例...")
        crawler = XiaoHongShuCrawler(use_proxy=False)
        
        print("开始获取评论...")
        comments = crawler.get_comments(
            note_id="68a048c1000000001d01838e",
            max_pages=1  # 只获取1页来测试
        )
        
        print(f"获取到 {len(comments)} 条评论")
        
    except Exception as e:
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {e}")
        print("\n详细错误信息:")
        print("=" * 50)
        traceback.print_exc()
        print("=" * 50)
        
        # 尝试找出具体错误位置
        print("\n尝试找出具体错误位置...")
        try:
            # 禁用SSL警告
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            
            crawler = XiaoHongShuCrawler(use_proxy=False)
            
            # 手动执行每一步
            print("手动执行第一步：准备请求头...")
            base_url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/page"
            params = {
                'note_id': "68a048c1000000001d01838e",
                'cursor': '',
                'top_comment_id': '',
                'image_formats': 'jpg,webp,avif',
                'xsec_token': 'ABIyAXG1J9ckAl0VbljygE3I8b6TZ0k5P4jORY-kCIzzw%3D'
            }
            params = {k: v for k, v in params.items() if v}
            from urllib.parse import urlencode
            url = base_url + '?' + urlencode(params)
            
            print("手动执行第二步：生成X-s参数...")
            xs_value = crawler.xs_gen.generate_xs(
                url=url,
                method="GET",
                user_id=crawler.cookie_info['a1']
            )
            print("X-s参数生成成功")
            
        except Exception as e2:
            print(f"第二步出错: {e2}")
            traceback.print_exc()

if __name__ == "__main__":
    debug_crawler()