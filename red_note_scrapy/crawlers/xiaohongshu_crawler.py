#!/usr/bin/env python3
"""
小红书评论爬虫
获取指定笔记的评论数据
"""

import requests
import json
import time
import csv
import os
import random
from datetime import datetime
import sys
import logging
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "generators"))
try:
    from working_xs_generator import WorkingXSGenerator
except ImportError as e:
    logging.error(f'ImportError {e}')
from urllib.parse import urlencode, quote
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class XiaoHongShuCrawler:
    def __init__(self, use_proxy=False):
        self.xs_gen = WorkingXSGenerator()
        self.session = requests.Session()
        
        # 配置重试策略
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        
        # 配置适配器
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # 配置session
        self.session.verify = False  # 禁用SSL验证
        self.session.timeout = 30
        
        # 代理设置
        self.use_proxy = use_proxy
        if use_proxy:
            self.session.proxies = {
                'http': 'http://127.0.0.1:7890',
                'https': 'http://127.0.0.1:7890'
            }
        
        # 基础请求头
        self.base_headers = {
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
            'x-b3-traceid': '',  # 可以留空或随机生成
            'x-xray-traceid': '',  # 可以留空或随机生成
        }
        
        # 从用户提供的cookie中提取关键信息
        self.cookie_info = self._parse_cookie()
        
        # 生成随机跟踪ID
        self.x_b3_traceid = self._generate_trace_id()
        self.x_xray_traceid = self._generate_trace_id()
        
    def _parse_cookie(self):
        """解析cookie，提取关键信息"""
        cookie_str = (
            "gid=yj8D24fWSDv0yj8D24fK069V0yIY6AFDTDxSxyU1kTyk2428MD7AC4888W2q2Yy8fJ0KjyDJ; "
            "xsecappid=xhs-pc-web; "
            "abRequestId=f425aaf4-2614-55c8-b8d1-262c611be2ab; "
            "a1=198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479; "
            "webId=fc4fb0dccb1a480d5f17359394c861d7; "
            "web_session=040069b3ed6ebed4fbe38d058d3a4bf7c6f823; "
            "webBuild=4.79.0; "
            "unread={%22ub%22:%2268b56bf2000000001c004134%22%2C%22ue%22:%2268a3fe26000000001c0126d1%22%2C%22uc%22:20}; "
            "acw_tc=0a5088b217569088917503762e8bfe73414226f403ffca1e69fe74fa1b61df; "
            "websectiga=29098a4cf41f76ee3f8db19051aaa60c0fc7c5e305572fec762da32d457d76ae; "
            "sec_poison_id=5944d42a-39e9-444e-b237-d629133962ab; "
            "loadts=1756910531213"
        )
        
        cookies = {}
        for item in cookie_str.split('; '):
            if '=' in item:
                key, value = item.split('=', 1)
                cookies[key] = value
        
        return {
            'a1': cookies.get('a1', ''),
            'web_session': cookies.get('web_session', ''),
            'webId': cookies.get('webId', ''),
            'webBuild': cookies.get('webBuild', '4.79.0'),
            'gid': cookies.get('gid', ''),
            'websectiga': cookies.get('websectiga', ''),
            'sec_poison_id': cookies.get('sec_poison_id', ''),
            'acw_tc': cookies.get('acw_tc', ''),
        }
    
    def _generate_trace_id(self):
        """生成随机跟踪ID"""
        import uuid
        return str(uuid.uuid4()).replace('-', '')[:24]
    
    def _generate_xs_common(self):
        """生成X-s-common参数"""
        # 使用与X-s相同的生成算法
        return self.xs_gen.generate_xs_common()
    
    def get_sub_comments(self, note_id, comment_id, cursor='', max_pages=10):
        """
        获取子评论
        
        Args:
            note_id: 笔记ID
            comment_id: 主评论ID
            cursor: 分页游标
            max_pages: 最大获取页数
            
        Returns:
            list: 子评论数据列
        """
        base_url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page"
        
        # 构建查询参数
        params = {
            'note_id': note_id,
            'root_comment_id': comment_id,  # 修正参数名
            'cursor': cursor,
            'num': '10',
            'image_formats': 'jpg,webp,avif',
            'xsec_token': 'ABIyAXG1J9ckAl0VbljygE3I8b6TZ0k5P4jORY-kCIzzw%3D'
        }
        
        # 移除空值参数
        params = {k: v for k, v in params.items() if v}
        
        # 构建完整URL
        url = base_url + '?' + urlencode(params)
        
        # 生成时间戳
        timestamp = str(int(time.time() * 1000))
        
        # 准备请求头
        headers = self.base_headers.copy()
        headers['cookie'] = (
            f"gid={self.cookie_info['gid']}; "
            f"xsecappid=xhs-pc-web; "
            f"abRequestId=f425aaf4-2614-55c8-b8d1-262c611be2ab; "
            f"a1={self.cookie_info['a1']}; "
            f"webId={self.cookie_info['webId']}; "
            f"web_session={self.cookie_info['web_session']}; "
            f"webBuild={self.cookie_info['webBuild']}; "
            f"acw_tc=0a5088b217569088917503762e8bfe73414226f403ffca1e69fe74fa1b61df; "
            f"websectiga=29098a4cf41f76ee3f8db19051aaa60c0fc7c5e305572fec762da32d457d76ae; "
            f"sec_poison_id=5944d42a-39e9-444e-b237-d629133962ab; "
            "unread=%7B%22ub%22%3A%2268b56bf2000000001c004134%22%2C%22ue%22%3A%2268a3fe26000000001c0126d1%22%2C%22uc%22%3A20%7D; "
            f"loadts={int(time.time() * 1000)}"
        )
        
        # 生成X-s参数
        xs_value = self.xs_gen.generate_xs(
            url=url,
            user_id=self.cookie_info['a1']
        )
        
        # 添加认证相关头
        headers['X-s'] = xs_value
        headers['X-s-common'] = self._generate_xs_common()
        headers['X-t'] = timestamp
        
        all_sub_comments = []
        page = 1
        
        while page <= max_pages:
            try:
                print(f"正在获取主评论 {comment_id} 的第 {page} 页子评论...")
                
                # 发送请求
                response = self.session.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get('success', False):
                        comment_data = data.get('data', {})
                        sub_comments = comment_data.get('comments', [])
                        
                        if not sub_comments:
                            print("没有更多子评论了")
                            break
                        
                        # 处理子评论数据
                        for sub_comment in sub_comments:
                            sub_comment_info = {
                                'id': sub_comment.get('id', ''),
                                'note_id': note_id,
                                'user_id': sub_comment.get('user_info', {}).get('user_id', ''),
                                'nickname': sub_comment.get('user_info', {}).get('nickname', ''),
                                'content': sub_comment.get('content', ''),
                                'like_count': sub_comment.get('like_count', 0),
                                'create_time': datetime.fromtimestamp(sub_comment.get('create_time', 0) / 1000 if sub_comment.get('create_time', 0) > 1000000000000 else sub_comment.get('create_time', 0)).strftime('%Y-%m-%d %H:%M:%S'),
                                'ip_location': sub_comment.get('ip_location', ''),
                                'level': sub_comment.get('level', 0),
                                'status': sub_comment.get('status', 0),
                                'target_user_id': sub_comment.get('target_user_info', {}).get('user_id', ''),
                                'target_nickname': sub_comment.get('target_user_info', {}).get('nickname', ''),
                                'parent_comment_id': comment_id
                            }
                            all_sub_comments.append(sub_comment_info)
                        
                        print(f"主评论 {comment_id} 第 {page} 页获取到 {len(sub_comments)} 条子评论")
                        
                        # 检查是否还有下一页
                        cursor = comment_data.get('cursor', '')
                        if not cursor:
                            break
                        
                        # 更新URL中的cursor
                        params['cursor'] = cursor
                        url = base_url + '?' + urlencode(params)
                        
                        # 重新生成X-s参数（因为URL变了）
                        xs_value = self.xs_gen.generate_xs(
                            url=url,
                            user_id=self.cookie_info['a1']
                        )
                        headers['X-s'] = xs_value
                        headers['X-t'] = str(int(time.time() * 1000))
                        
                        page += 1
                        
                        # 添加延迟避免请求过快
                        time.sleep(random.uniform(1, 3))
                        
                    else:
                        print(f"子评论API返回错误: {data.get('msg', 'Unknown error')}")
                        break
                        
                elif response.status_code == 403:
                    print("子评论请求被拒绝，可能是cookie失效或参数错误")
                    break
                else:
                    print(f"子评论请求失败，状态码: {response.status_code}")
                    print(f"响应内容: {response.text}")
                    break
                    
            except requests.exceptions.SSLError as e:
                print(f"子评论SSL错误: {e}")
                print("等待5秒后重试...")
                time.sleep(5)
                continue
            except requests.exceptions.ConnectionError as e:
                print(f"子评论连接错误: {e}")
                print("等待5秒后重试...")
                time.sleep(5)
                continue
            except requests.exceptions.Timeout as e:
                print(f"子评论请求超时: {e}")
                print("等待3秒后重试...")
                time.sleep(3)
                continue
            except Exception as e:
                print(f"获取子评论时发生错误: {e}")
                break
        
        return all_sub_comments
    
    def get_comments(self, note_id, cursor='', top_comment_id='', max_pages=10):
        """
        获取笔记评论
        
        Args:
            note_id: 笔记ID
            cursor: 分页游标
            top_comment_id: 顶级评论ID
            max_pages: 最大获取页数
            
        Returns:
            list: 评论数据列表
        """
        base_url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/page"
        
        # 构建查询参数
        params = {
            'note_id': note_id,
            'cursor': cursor,
            'top_comment_id': top_comment_id,
            'image_formats': 'jpg,webp,avif',
            'xsec_token': 'ABIyAXG1J9ckAl0VbljygE3I8b6TZ0k5P4jORY-kCIzzw%3D'
        }
        
        # 移除空值参数
        params = {k: v for k, v in params.items() if v}
        
        # 构建完整URL
        url = base_url + '?' + urlencode(params)
        
        # 生成时间戳
        timestamp = str(int(time.time() * 1000))
        
        # 准备请求头
        headers = self.base_headers.copy()
        headers['cookie'] = (
            f"gid={self.cookie_info['gid']}; "
            f"xsecappid=xhs-pc-web; "
            f"abRequestId=f425aaf4-2614-55c8-b8d1-262c611be2ab; "
            f"a1={self.cookie_info['a1']}; "
            f"webId={self.cookie_info['webId']}; "
            f"web_session={self.cookie_info['web_session']}; "
            f"webBuild={self.cookie_info['webBuild']}; "
            f"acw_tc=0a5088b217569088917503762e8bfe73414226f403ffca1e69fe74fa1b61df; "
            f"websectiga=29098a4cf41f76ee3f8db19051aaa60c0fc7c5e305572fec762da32d457d76ae; "
            f"sec_poison_id=5944d42a-39e9-444e-b237-d629133962ab; "
            "unread=%7B%22ub%22%3A%2268b56bf2000000001c004134%22%2C%22ue%22%3A%2268a3fe26000000001c0126d1%22%2C%22uc%22%3A20%7D; "
            f"loadts={int(time.time() * 1000)}"
        )
        
        # 生成X-s参数
        xs_value = self.xs_gen.generate_xs(
            url=url,
            user_id=self.cookie_info['a1']
        )
        
        # 添加认证相关头
        headers['X-s'] = xs_value
        headers['X-s-common'] = self._generate_xs_common()
        headers['X-t'] = timestamp
        
        all_comments = []
        page = 1
        
        while page <= max_pages:
            try:
                print(f"正在获取第 {page} 页评论...")
                
                # 发送请求
                response = self.session.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get('success', False):
                        comment_data = data.get('data', {})
                        comments = comment_data.get('comments', [])
                        
                        if not comments:
                            print("没有更多评论了")
                            break
                        
                        # 处理评论数据
                        for comment in comments:
                            comment_info = {
                                'id': comment.get('id', ''),
                                'note_id': note_id,
                                'user_id': comment.get('user_info', {}).get('user_id', ''),
                                'nickname': comment.get('user_info', {}).get('nickname', ''),
                                'content': comment.get('content', ''),
                                'like_count': comment.get('like_count', 0),
                                'create_time': datetime.fromtimestamp(comment.get('create_time', 0) / 1000 if comment.get('create_time', 0) > 1000000000000 else comment.get('create_time', 0)).strftime('%Y-%m-%d %H:%M:%S'),
                                'ip_location': comment.get('ip_location', ''),
                                'level': comment.get('level', 0),
                                'status': comment.get('status', 0),
                                'sub_comment_count': comment.get('sub_comment_count', 0),
                                'sub_comments': []
                            }
                            
                            # 处理子评论 - 使用单独的API获取
                            sub_comment_count = comment.get('sub_comment_count', 0)
                            # 确保sub_comment_count是整数
                            try:
                                sub_comment_count = int(sub_comment_count)
                            except (ValueError, TypeError):
                                sub_comment_count = 0
                            
                            if sub_comment_count > 0:
                                print(f"主评论 {comment_info['id']} 有 {sub_comment_count} 条子评论，正在获取...")
                                sub_comments = self.get_sub_comments(
                                    note_id=note_id,
                                    comment_id=comment_info['id']
                                )
                                comment_info['sub_comments'] = sub_comments
                                print(f"主评论 {comment_info['id']} 获取到 {len(sub_comments)} 条子评论")
                            else:
                                comment_info['sub_comments'] = []
                            
                            all_comments.append(comment_info)
                        
                        print(f"第 {page} 页获取到 {len(comments)} 条评论")
                        
                        # 检查是否还有下一页
                        cursor = comment_data.get('cursor', '')
                        if not cursor:
                            break
                        
                        # 更新URL中的cursor
                        params['cursor'] = cursor
                        url = base_url + '?' + urlencode(params)
                        
                        # 重新生成X-s参数（因为URL变了）
                        xs_value = self.xs_gen.generate_xs(
                            url=url,
                            user_id=self.cookie_info['a1']
                        )
                        headers['X-s'] = xs_value
                        headers['X-t'] = str(int(time.time() * 1000))
                        
                        page += 1
                        
                        # 添加延迟避免请求过快
                        time.sleep(random.uniform(1, 3))
                        
                    else:
                        print(f"API返回错误: {data.get('msg', 'Unknown error')}")
                        break
                        
                elif response.status_code == 403:
                    print("请求被拒绝，可能是cookie失效或参数错误")
                    break
                else:
                    print(f"请求失败，状态码: {response.status_code}")
                    print(f"响应内容: {response.text}")
                    break
                    
            except requests.exceptions.SSLError as e:
                print(f"SSL错误: {e}")
                print("等待5秒后重试...")
                time.sleep(5)
                continue
            except requests.exceptions.ConnectionError as e:
                print(f"连接错误: {e}")
                print("等待5秒后重试...")
                time.sleep(5)
                continue
            except requests.exceptions.Timeout as e:
                print(f"请求超时: {e}")
                print("等待3秒后重试...")
                time.sleep(3)
                continue
            except TypeError as e:
                print(f"类型错误: {e}")
                print("这可能是字符串和整数比较错误")
                import traceback
                traceback.print_exc()
                break
            except Exception as e:
                print(f"发生错误: {e}")
                import traceback
                traceback.print_exc()
                break
        
        return all_comments
    
    def save_to_csv(self, comments, filename=None):
        """保存评论到CSV文件"""
        if not filename:
            filename = f"comments_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        # 准备CSV数据
        rows = []
        for comment in comments:
            # 主评论
            row = {
                '评论ID': comment['id'],
                '笔记ID': comment['note_id'],
                '用户ID': comment['user_id'],
                '昵称': comment['nickname'],
                '评论内容': comment['content'],
                '点赞数': comment['like_count'],
                '发布时间': comment['create_time'],
                'IP归属地': comment['ip_location'],
                '评论等级': comment['level'],
                '状态': comment['status'],
                '子评论数': comment['sub_comment_count'],
                '是否为子评论': '否',
                '目标用户': '',
                '目标昵称': ''
            }
            rows.append(row)
            
            # 子评论
            for sub_comment in comment['sub_comments']:
                sub_row = {
                    '评论ID': sub_comment['id'],
                    '笔记ID': comment['note_id'],
                    '用户ID': sub_comment['user_id'],
                    '昵称': sub_comment['nickname'],
                    '评论内容': sub_comment['content'],
                    '点赞数': sub_comment['like_count'],
                    '发布时间': sub_comment['create_time'],
                    'IP归属地': sub_comment['ip_location'],
                    '评论等级': sub_comment['level'],
                    '状态': sub_comment['status'],
                    '子评论数': 0,
                    '是否为子评论': '是',
                    '目标用户': sub_comment.get('target_user_id', ''),
                    '目标昵称': sub_comment.get('target_nickname', '')
                }
                rows.append(sub_row)
        
        # 写入CSV
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        
        print(f"评论数据已保存到: {filename}")
        return filename
    
    def save_to_json(self, comments, filename=None):
        """保存评论到JSON文件"""
        if not filename:
            filename = f"comments_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(comments, f, ensure_ascii=False, indent=2)
        
        print(f"评论数据已保存到: {filename}")
        return filename

def main():
    """主函数"""
    # 禁用SSL警告
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    # 创建爬虫实例
    # use_proxy=True 如果需要使用代理
    crawler = XiaoHongShuCrawler(use_proxy=False)
    
    # 笔记ID（从你提供的API中提取）
    note_id = "68a048c1000000001d01838e"
    
    print(f"开始获取笔记 {note_id} 的评论...")
    
    # 获取评论
    comments = crawler.get_comments(
        note_id=note_id,
        max_pages=10  # 限制获取10页，避免过多请求
    )
    
    if comments:
        print(f"\n共获取到 {len(comments)} 条主评论")
        
        # 保存数据
        csv_file = crawler.save_to_csv(comments)
        json_file = crawler.save_to_json(comments)
        
        # 显示前5条评论
        print("\n前5条评论预览:")
        for i, comment in enumerate(comments[:5], 1):
            print(f"\n{i}. {comment['nickname']} ({comment['create_time']})")
            print(f"   内容: {comment['content']}")
            print(f"   点赞: {comment['like_count']} | IP: {comment['ip_location']}")
            if comment['sub_comments']:
                print(f"   子评论数: {len(comment['sub_comments'])}")
    else:
        print("未获取到评论数据")

if __name__ == "__main__":
    main()