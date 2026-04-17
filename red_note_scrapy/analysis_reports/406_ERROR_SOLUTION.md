# 小红书子评论爬取 - 解决406错误完整方案

## 📋 问题分析

经过深入分析，小红书子评论API返回406错误的主要原因是缺少必要的认证参数：

1. **X-s参数** - 已有实现（working_xs_generator.py）
2. **X-s-common参数** - 已有实现（xiaohongshu_xs_common_generator.py）
3. **xsec_token参数** - 需要从页面数据获取

## 🛠️ 解决方案步骤

### 步骤1：使用现有的X-s生成算法

项目中已有两个X-s生成算法：

#### 方案A：使用working_xs_generator.py（推荐）
```python
from working_xs_generator import WorkingXSGenerator

xs_generator = WorkingXSGenerator()
xs_value = xs_generator.generate_xs(
    url="https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page",
    method="GET",
    user_id=""
)
```

#### 方案B：使用xs_generator.py
```python
from xs_generator import XSGenerator

xs_generator = XSGenerator()
xs_value = xs_generator.generate_xs(
    url="https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page",
    note_id="68a35fc0000000001c009cd9",
    root_comment_id="68a83b5900000000260052c3",
    user_id="198908c6b1437n0y6e2wp9fkblicmigpdjfca1ow850000644479"
)
```

### 步骤2：生成X-s-common参数

```python
from xiaohongshu_xs_common_generator import XiaohongshuXSCommonGenerator

xs_common_generator = XiaohongshuXSCommonGenerator()
xs_common_value = xs_common_generator.generate_xs_common(
    "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page"
)
```

### 步骤3：获取xsec_token

从page.json文件中获取xsec_token：
```python
import json

# 读取page.json获取xsec_token
with open('page.json', 'r', encoding='utf-8') as f:
    page_data = json.load(f)
    xsec_token = page_data['data']['xsec_token']
```

### 步骤4：构建完整请求

```python
import requests
from urllib.parse import urlencode

def get_sub_comments(note_id, root_comment_id, cookie, xsec_token):
    # 构建请求参数
    params = {
        'note_id': note_id,
        'root_comment_id': root_comment_id,
        'num': '10',
        'cursor': '',
        'image_formats': 'jpg,webp,avif',
        'xsec_token': xsec_token
    }
    
    # 构建URL
    base_url = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/sub/page"
    url = base_url + '?' + urlencode(params)
    
    # 生成认证头
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,en-GB;q=0.6',
        'origin': 'https://www.xiaohongshu.com',
        'referer': 'https://www.xiaohongshu.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0',
        'cookie': cookie,
        'X-s': xs_value,                    # 步骤1生成
        'X-t': str(int(time.time() * 1000)),
        'x-s-common': xs_common_value       # 步骤2生成
    }
    
    # 发送请求
    response = requests.get(url, headers=headers)
    return response.json()
```

## 📝 完整使用示例

### 使用sub_comment_solution.py

```python
from sub_comment_solution import XiaohongshuSubCommentCrawler

# 初始化爬虫
crawler = XiaohongshuSubCommentCrawler()

# 设置参数
note_id = "68a35fc0000000001c009cd9"
root_comment_id = "68a83b5900000000260052c3"
cookie = "你的cookie"
xsec_token = "ABDqLWtD4XHpHf33wJV1R-hkqHfMDT91r8agSgB334lsI="

# 获取子评论
result = crawler.get_sub_comments(
    note_id=note_id,
    root_comment_id=root_comment_id,
    cookie=cookie,
    xsec_token=xsec_token,
    num=10
)

if result['success']:
    print(f"成功获取 {len(result['comments'])} 条子评论")
    for comment in result['comments']:
        print(f"- {comment['content']}")
else:
    print(f"获取失败: {result['error']}")
```

## 🔍 关键参数说明

### 必需参数
1. **X-s**: 使用working_xs_generator.py生成
2. **X-s-common**: 使用xiaohongshu_xs_common_generator.py生成  
3. **xsec_token**: 从页面数据获取
4. **Cookie**: 有效的用户认证cookie

### 可选参数
1. **cursor**: 分页游标，用于获取更多子评论
2. **num**: 每页数量，建议10-20

## 🎯 获取xsec_token的方法

### 方法1：从page.json获取
```python
import json
with open('page.json', 'r') as f:
    data = json.load(f)
    xsec_token = data['data']['xsec_token']
```

### 方法2：从评论数据获取
```python
# 从任何评论的user_info中获取
xsec_token = comment['user_info']['xsec_token']
```

### 方法3：通过浏览器调试获取
1. 打开小红书页面
2. F12打开开发者工具
3. 在网络请求中查找评论API
4. 从请求参数中复制xsec_token

## ⚠️ 注意事项

1. **Cookie有效性**: 确保cookie是最新的，过期会导致406错误
2. **xsec_token时效性**: xsec_token可能会变化，建议定期更新
3. **请求频率**: 避免过于频繁的请求，可能触发反爬机制
4. **参数匹配**: 确保note_id、root_comment_id和xsec_token来自同一页面

## 🚀 完整的解决方案文件

项目已包含完整的解决方案：
- `sub_comment_solution.py` - 完整的子评论获取解决方案
- `working_xs_generator.py` - 验证过的X-s生成算法
- `xiaohongshu_xs_common_generator.py` - X-s-common生成算法
- `page.json` - 包含真实的xsec_token和测试数据

运行 `python3 sub_comment_solution.py` 即可测试完整解决方案。