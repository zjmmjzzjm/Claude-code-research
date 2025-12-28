# Twitter 数据采集工具

一个简单易用的 Twitter/X 数据采集工具，使用 Python 和 twscrape 库。

## 快速开始

### 1. 安装依赖

```bash
# 安装 twscrape
pip install twscrape

# 或使用 pipx
pipx install twscrape
```

### 2. 添加 Twitter 账号

```bash
# 交互式添加账号
twscrape add_accounts

# 或从文件导入（每行一个账号，格式: username:password）
twscrape add_accounts accounts.txt
```

**推荐**: 准备 2-3 个备用的 Twitter 账号，这样可以轮换使用避免被限制。

### 3. 运行采集脚本

```bash
# 采集单个用户的推文
python twitter_collector.py @elonmusk -n 100

# 采集关注列表的推文
python twitter_collector.py @your_username --following --max-users 20

# 查看帮助
python twitter_collector.py --help
```

## 使用示例

### 示例 1: 采集单个用户

获取 @jessetrived 最近 200 条推文：

```bash
python twitter_collector.py @jessetrived -n 200
```

输出：
```
twitter_data/
├── jessetrived_20251228_123456.json      # JSON 格式
├── jessetrived_20251228_123456.md        # Markdown 格式
└── jessetrived_20251228_123456.csv       # CSV 格式
```

### 示例 2: 采集关注列表

获取你关注的最多 50 个用户，每人最近 30 条推文：

```bash
python twitter_collector.py @your_username \
  --following \
  --max-users 50 \
  --tweets-per-user 30 \
  --format all
```

### 示例 3: 只保存 CSV 格式

```bash
python twitter_collector.py @username -n 100 --format csv
```

### 示例 4: 自定义输出文件名

```bash
python twitter_collector.py @username -n 100 --output my_tweets
```

输出文件：
- `twitter_data/my_tweets.json`
- `twitter_data/my_tweets.md`
- `twitter_data/my_tweets.csv`

## 命令行参数

```
位置参数:
  username              Twitter 用户名（可以带 @）

可选参数:
  -h, --help            显示帮助信息
  -n, --number N        获取推文数量（默认: 100）
  --following           获取关注用户的所有推文
  --max-users N         最多获取多少个关注用户（默认: 10）
  --tweets-per-user N   每个用户获取的推文数（默认: 20）
  --format {json,markdown,csv,all}
                        输出格式（默认: all）
  --output OUTPUT       输出文件名（不含扩展名）
  --debug               显示调试日志
```

## 输出格式

### JSON 格式
适合程序处理和数据交换：

```json
[
  {
    "id": "1234567890",
    "date": "2025-12-28T12:34:56",
    "content": "推文内容...",
    "likes": 1234,
    "retweets": 56,
    "replies": 78,
    "views": 12345,
    "url": "https://twitter.com/username/status/1234567890",
    "author": "username",
    "author_id": "123456"
  }
]
```

### Markdown 格式
适合人类阅读和归档：

```markdown
# Twitter 数据采集

**采集时间**: 2025-12-28 12:34:56
**推文数量**: 100

---

## 2025-12-28T12:34:56

**作者**: @username

推文内容...

**互动数据**:
- 👍 赞: 1,234
- 🔄 转: 56
- 💬 回: 78
- 👁️ 看: 12,345

**链接**: https://twitter.com/username/status/1234567890

---
```

### CSV 格式
可用 Excel、Google Sheets 等打开：

| date | author | content | likes | retweets | replies | views | url |
|------|--------|---------|-------|----------|---------|-------|-----|
| 2025-12-28T12:34:56 | username | 推文内容... | 1234 | 56 | 78 | 12345 | https://... |

## 高级用法

### 1. 批量采集多个用户

创建一个脚本 `batch_collect.py`：

```python
import asyncio
from twitter_collector import TwitterCollector

users = ['user1', 'user2', 'user3']

async def batch_collect():
    collector = TwitterCollector()
    await collector.login()

    for user in users:
        tweets = await collector.get_user_tweets(user, limit=100)
        collector.save_json(tweets, f"{user}_tweets")
        collector.save_markdown(tweets, f"{user}_tweets")

asyncio.run(batch_collect())
```

### 2. 定时采集

使用 cron 或任务调度器定期运行：

```bash
# 每天凌晨 2 点采集
0 2 * * * cd /path/to/project && python twitter_collector.py @username -n 100
```

### 3. 结合 Claude Code 分析

采集后可以让 Claude Code 分析：

```bash
# 采集数据
python twitter_collector.py @expert -n 500

# 在 Claude Code 中分析
claude
> 分析 twitter_data/expert_20251228.json 中的推文主题
> 总结这个作者最近的关注点
```

## 常见问题

### Q: 提示账号被锁定或限制？
**A**:
- 使用多个账号轮换
- 在采集之间添加延迟
- 避免短时间内大量请求

修改脚本中的延迟时间：
```python
await asyncio.sleep(2)  # 改为 2 秒延迟
```

### Q: 只能获取最近 3200 条推文？
**A**: 这是 Twitter 的官方限制。如需更多历史数据：
- 定期备份新增推文
- 使用第三方数据服务（商业方案）

### Q: 如何获取推文中的图片/视频？
**A**: 使用 gallery-dl 工具：
```bash
pip install gallery-dl
gallery-dl --filter "type:tweets" https://twitter.com/username
```

### Q: 可以采集搜索结果吗？
**A**: 可以，使用 twscrape 的搜索功能：
```python
async for tweet in api.search("python programming", limit=100):
    # 处理推文
```

### Q: 如何避免违反 Twitter 服务条款？
**A**:
- ✅ 仅用于个人研究
- ✅ 注明数据来源
- ✅ 尊重原创作者
- ❌ 不要用于商业目的（未获许可）
- ❌ 不要过度频繁请求
- ❌ 不要转售数据

## 技术细节

### 依赖项
- **Python**: 3.7+
- **twscrape**: 核心采集库
- **asyncio**: 异步 I/O

### 工作原理
1. 使用账号池登录 Twitter
2. 通过 GraphQL API 获取数据
3. 自动轮换账号避免限制
4. 支持多种数据格式导出

### 性能优化
- 异步并发请求
- 账号池自动轮换
- 自动错误重试
- 流式数据处理

## 相关资源

- **完整指南**: [twitter-data-collection-guide.md](./twitter-data-collection-guide.md)
- **twscrape GitHub**: https://github.com/vladkens/twscrape
- **Twitter API 文档**: https://developer.x.com/en/docs/twitter-api

## 许可和免责声明

本工具仅供学习和研究使用。使用本工具时请：
- 遵守 Twitter/X 服务条款
- 尊重数据版权和隐私
- 承担使用本工具的风险和责任

## 贡献

欢迎提交问题和改进建议！

---

**开始使用**:
```bash
pip install twscrape
twscrape add_accounts
python twitter_collector.py @username -n 100
```
