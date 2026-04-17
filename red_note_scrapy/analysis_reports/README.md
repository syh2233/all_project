# 小红书评论爬虫使用说明

## 功能说明

这个爬虫可以获取小红书笔记下的所有评论数据，包括主评论和子评论，并支持自动分页获取。

## 文件说明

- `xiaohongshu_crawler.py` - 主爬虫文件
- `xs_generator.py` - X-s参数生成器
- `comments_*.csv` - 导出的CSV格式评论数据
- `comments_*.json` - 导出的JSON格式评论数据

## 使用方法

### 1. 基本使用

```python
from xiaohongshu_crawler import XiaoHongShuCrawler

# 创建爬虫实例
crawler = XiaoHongShuCrawler()

# 获取指定笔记的评论
comments = crawler.get_comments(
    note_id="68a048c1000000001d01838e",  # 笔记ID
    max_pages=10  # 最大页数
)

# 保存数据
crawler.save_to_csv(comments)
crawler.save_to_json(comments)
```

### 2. 自定义参数

```python
# 获取评论时可以指定更多参数
comments = crawler.get_comments(
    note_id="68a048c1000000001d01838e",
    cursor="",  # 分页游标，首次获取留空
    top_comment_id="",  # 顶级评论ID，一般留空
    max_pages=5,  # 限制获取5页
    image_formats="jpg,webp,avif"  # 图片格式
)
```

## 数据格式

### CSV格式
CSV文件包含以下字段：
- 评论ID
- 笔记ID
- 用户ID
- 昵称
- 评论内容
- 点赞数
- 发布时间
- IP归属地
- 评论等级
- 状态
- 子评论数
- 是否为子评论
- 目标用户（子评论的回复对象）
- 目标昵称

### JSON格式
JSON数据结构更复杂，包含完整的嵌套关系：
```json
[
  {
    "id": "评论ID",
    "note_id": "笔记ID",
    "user_id": "用户ID",
    "nickname": "昵称",
    "content": "评论内容",
    "like_count": 点赞数,
    "create_time": "发布时间",
    "ip_location": "IP归属地",
    "level": 评论等级,
    "status": 状态,
    "sub_comment_count": 子评论数,
    "sub_comments": [
      {
        "id": "子评论ID",
        "user_id": "用户ID",
        "nickname": "昵称",
        "content": "评论内容",
        "target_user_id": "回复对象用户ID",
        "target_nickname": "回复对象昵称",
        ...
      }
    ]
  }
]
```

## 注意事项

1. **Cookie更新**：爬虫使用的是示例cookie，实际使用时需要从浏览器中获取最新的cookie
2. **请求频率**：爬虫已内置1秒的延迟，避免请求过快被限制
3. **X-s参数**：已自动生成X-s和X-t参数，无需手动处理
4. **数据量**：热门笔记可能有数千条评论，建议合理设置max_pages

## 获取Cookie的方法

1. 用Chrome浏览器打开小红书网站
2. 登录你的账号
3. 打开开发者工具（F12）
4. 切换到Network标签
5. 刷新页面或进行一些操作
6. 找到API请求，查看Request Headers中的cookie
7. 复制完整的cookie字符串，更新到代码中

## 常见问题

1. **403错误**：通常是cookie失效，需要更新cookie
2. **空数据**：可能是笔记ID错误或笔记已被删除
3. **时间戳错误**：已自动处理毫秒和秒的时间戳格式

## 扩展功能

爬虫支持以下扩展：
- 添加代理支持
- 实现多线程爬取
- 添加评论内容过滤
- 支持按时间范围筛选
- 导出到数据库（MySQL、MongoDB等）

## 免责声明

请遵守小红书的使用条款，不要过度频繁请求，仅用于学习和研究目的。