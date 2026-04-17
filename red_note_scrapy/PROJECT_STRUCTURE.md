# 小红书子评论爬取项目 - 文件结构说明

## 📁 项目结构

```
red_note_scrapy/
├── 📂 generators/                    # 核心生成算法
│   ├── xs_generator.py              # X-s参数生成算法
│   ├── working_xs_generator.py      # 验证过的X-s生成算法（推荐）
│   ├── xiaohongshu_xs_common_generator.py  # X-s-common参数生成算法
│   └── sub_comment_solution.py      # 完整的子评论解决方案
│
├── 📂 crawlers/                     # 爬虫实现
│   ├── xiaohongshu_crawler.py       # 主爬虫
│   ├── xiaohongshu_crawler_optimized.py  # 优化版爬虫
│   ├── mobile_sub_comment_crawler.py    # 移动端子评论爬虫
│   └── selenium_sub_comment_crawler.py   # Selenium版爬虫
│
├── 📂 browser_files/                # 浏览器相关文件
│   ├── *.js                        # JavaScript源文件
│   ├── 📂 html/                     # HTML调试文件
│   └── 📂 scripts/                  # 用户脚本
│
├── 📂 debug_scripts/                # 调试和分析脚本
│   ├── *debug*.py                  # 调试脚本
│   ├── *analysis*.py               # 分析脚本
│   ├── *test*.py                   # 测试脚本
│   └── *analyzer*.py               # 分析器
│
├── 📂 test_data/                    # 测试数据
│   ├── page.json                   # 页面数据（包含xsec_token）
│   ├── comments_*.json             # 评论数据
│   └── *.json                      # 其他测试数据
│
├── 📂 analysis_reports/             # 分析报告
│   ├── *.md                        # Markdown分析报告
│   └── 406_ERROR_SOLUTION.md       # 406错误解决方案
│
└── 📂 temp_files/                   # 临时文件
    ├── *.py                        # 临时脚本
    └── *.json                      # 临时数据
```

## 🚀 快速开始

### 1. 使用完整的解决方案
```bash
cd generators/
python3 sub_comment_solution.py
```

### 2. 使用单独的生成器
```bash
# X-s生成器
cd generators/
python3 working_xs_generator.py

# X-s-common生成器
cd generators/
python3 xiaohongshu_xs_common_generator.py
```

### 3. 使用爬虫
```bash
cd crawlers/
python3 xiaohongshu_crawler.py
```

## 📋 核心文件说明

### 生成器 (generators/)
- **working_xs_generator.py** - 推荐使用的X-s生成算法
- **xiaohongshu_xs_common_generator.py** - X-s-common生成算法
- **sub_comment_solution.py** - 集成所有算法的完整解决方案

### 爬虫 (crawlers/)
- **xiaohongshu_crawler.py** - 主要的爬虫实现
- **mobile_sub_comment_crawler.py** - 移动端适配版本

### 浏览器文件 (browser_files/)
- **vendor-dynamic.77f9fe85.js** - 包含X-s-common生成逻辑的关键文件
- **index.4a7dae10.js** - 前端主要逻辑文件
- **Note.457d2fea.js** - 评论相关组件

### 测试数据 (test_data/)
- **page.json** - 包含真实的xsec_token和评论数据

## 🔧 解决406错误

子评论API返回406错误需要以下参数：

1. **X-s** - 使用`working_xs_generator.py`生成
2. **X-s-common** - 使用`xiaohongshu_xs_common_generator.py`生成
3. **xsec_token** - 从`test_data/page.json`获取
4. **有效的Cookie**

详细解决方案请参考：`analysis_reports/406_ERROR_SOLUTION.md`

## 📝 使用示例

```python
from generators.sub_comment_solution import XiaohongshuSubCommentCrawler

crawler = XiaohongshuSubCommentCrawler()
result = crawler.test_with_real_data()

if result['success']:
    print(f"成功获取 {len(result['comments'])} 条子评论")
```

## ⚠️ 注意事项

1. **Cookie时效性** - 定期更新Cookie
2. **xsec_token变化** - 需要从页面重新获取
3. **请求频率** - 避免过于频繁的请求
4. **文件路径** - 在不同目录运行时注意导入路径

## 🎯 下一步优化

1. 实现自动获取xsec_token
2. 添加Cookie自动更新机制
3. 优化请求频率控制
4. 添加异常处理和重试机制