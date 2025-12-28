# Twitter 数据获取完整指南

> 如何下载你关注的作者的推文（2025 年最新）

## 目录
1. [方法概览](#方法概览)
2. [官方 API 方法](#官方-api-方法)
3. [开源工具方法](#开源工具方法)
4. [无代码工具](#无代码工具)
5. [推荐方案](#推荐方案)
6. [实践示例](#实践示例)

---

## 方法概览

| 方法 | 难度 | 成本 | 稳定性 | 数据量限制 | 推荐度 |
|------|------|------|--------|------------|--------|
| **官方 API** | 中 | 高（$100+/月）| ⭐⭐⭐⭐⭐ | 有限制 | ⭐⭐⭐ |
| **Tweepy** | 中 | 免费/低 | ⭐⭐⭐⭐ | API 限制 | ⭐⭐⭐⭐ |
| **twscrape** | 低 | 免费 | ⭐⭐⭐ | 无硬限制 | ⭐⭐⭐⭐⭐ |
| **snscrape** | 低 | 免费 | ⭐⭐ | 无硬限制 | ⭐⭐⭐ |
| **无代码工具** | 低 | 中-高 | ⭐⭐⭐⭐ | 各异 | ⭐⭐⭐⭐ |

---

## 官方 API 方法

### X (Twitter) API v2

**优点**：
- 官方支持，稳定可靠
- 数据结构完整
- 持续更新维护

**缺点**：
- **价格昂贵**（Basic 层 $100/月，Pro 层 $5,000/月）
- 严格的速率限制
- 需要 OAuth 2.0 认证

**适用场景**：
- 企业级应用
- 需要稳定性和官方支持
- 大规模数据采集

### 获取 API 密钥

1. 访问 [X Developer Portal](https://developer.x.com/)
2. 创建开发者账号
3. 创建新 App
4. 获取 API Key、API Secret、Access Token、Access Token Secret

### 使用 Tweepy（官方 API 封装）

```bash
pip install tweepy
```

```python
import tweepy

# 认证
client = tweepy.Client(
    bearer_token='YOUR_BEARER_TOKEN',
    consumer_key='YOUR_API_KEY',
    consumer_secret='YOUR_API_SECRET',
    access_token='YOUR_ACCESS_TOKEN',
    access_token_secret='YOUR_ACCESS_TOKEN_SECRET'
)

# 获取用户的推文
def get_user_tweets(username, count=100):
    try:
        # 获取用户 ID
        user = client.get_user(username=username)
        user_id = user.data.id

        # 获取推文
        tweets = client.get_users_tweets(
            id=user_id,
            max_results=min(count, 100),
            tweet_fields=['created_at', 'public_metrics', 'context_annotations']
        )

        for tweet in tweets.data:
            print(f"{tweet.created_at}: {tweet.text}")

        return tweets
    except Exception as e:
        print(f"Error: {e}")

# 使用示例
get_user_tweets('elonmusk', 50)
```

**API 限制**（Basic Tier $100/月）：
- 每月 10,000 条推文
- 每 15 分钟 50 次请求

---

## 开源工具方法

### 1. twscrape（强烈推荐 ⭐⭐⭐⭐⭐）

**最新、最强大的开源 Twitter 工具**

**优点**：
- 完全免费
- 无硬性限制
- 使用多账号轮换
- 数据模型完整
- 活跃维护

**缺点**：
- 需要多个 Twitter 账号
- 需要管理账号池

#### 安装

```bash
pip install twscrape
```

#### 账号设置

```bash
# 添加账号（可以添加多个）
twscrape add_accounts

# 或从文件导入
twscrape add_accounts accounts.txt
```

`accounts.txt` 格式：
```
username:password
username2:password2
username3:password3
```

#### 使用示例

```python
import asyncio
from twscrape import API, gather
from twscrape.logger import set_log_level

# 设置日志级别
set_log_level("DEBUG")

async def main():
    api = API()

    # 账号池登录
    await api.pool.login()

    # 获取用户推文
    username = "jessetrived"
    user = await api.user_by_login(username)

    # 获取最近的推文
    tweets = []
    async for tweet in api.user_tweets(user.id, limit=100):
        tweets.append(tweet)
        print(f"{tweet.date}: {tweet.rawContent}")

    print(f"\n获取了 {len(tweets)} 条推文")

    # 保存到 JSON
    import json
    with open(f'{username}_tweets.json', 'w', encoding='utf-8') as f:
        json.dump([t.dict() for t in tweets], f, ensure_ascii=False, indent=2)

# 运行
asyncio.run(main())
```

#### 获取关注列表的所有推文

```python
import asyncio
from twscrape import API

async def download_following_tweets():
    api = API()
    await api.pool.login()

    # 你的账号
    my_username = "your_username"

    # 获取关注列表
    me = await api.user_by_login(my_username)

    following = []
    async for user in api.following(me.id, limit=1000):
        following.append(user)
        print(f"关注: @{user.username}")

    print(f"\n总共关注 {len(following)} 个用户")

    # 下载每个人的推文
    all_tweets = []
    for user in following:
        print(f"\n下载 @{user.username} 的推文...")
        try:
            async for tweet in api.user_tweets(user.id, limit=50):
                all_tweets.append({
                    'author': user.username,
                    'author_id': user.id,
                    'tweet_id': tweet.id,
                    'date': tweet.date.isoformat(),
                    'content': tweet.rawContent,
                    'likes': tweet.likeCount,
                    'retweets': tweet.retweetCount,
                    'replies': tweet.replyCount,
                    'views': tweet.viewCount
                })
        except Exception as e:
            print(f"  错误: {e}")

    # 保存
    import json
    with open('following_tweets.json', 'w', encoding='utf-8') as f:
        json.dump(all_tweets, f, ensure_ascii=False, indent=2)

    print(f"\n总共获取 {len(all_tweets)} 条推文")

asyncio.run(download_following_tweets())
```

#### CLI 使用

```bash
# 获取用户推文
twscrape user_tweets username --limit 100 --db tweets.db

# 搜索推文
twscrape search "python programming" --limit 500

# 获取关注列表
twscrape following username --limit 1000

# 导出为 JSON
twscrape user_tweets username --limit 100 --format json > tweets.json
```

---

### 2. snscrape

**优点**：
- 无需 API 密钥
- 简单易用
- 支持多种平台

**缺点**：
- **维护状态不活跃**（2022年后更新较少）
- 可能因为 Twitter API 变化而失效
- 较慢

#### 安装

```bash
pip install snscrape
```

#### 使用示例

```python
import snscrape.modules.twitter as sntwitter
import pandas as pd

# 获取用户推文
def get_tweets_snscrape(username, max_tweets=100):
    tweets = []

    for i, tweet in enumerate(sntwitter.TwitterUserScraper(username).get_items()):
        if i >= max_tweets:
            break
        tweets.append({
            'date': tweet.date,
            'content': tweet.rawContent,
            'likes': tweet.likeCount,
            'retweets': tweet.retweetCount
        })

    # 保存为 CSV
    df = pd.DataFrame(tweets)
    df.to_csv(f'{username}_tweets.csv', index=False)

    return df

# 使用
df = get_tweets_snscrape('elonmusk', 200)
```

---

### 3. 其他开源工具

#### Gallery-DL（适合下载媒体）

```bash
pip install gallery-dl
gallery-dl https://twitter.com/username
```

#### TWD（Twitter Watch Dog）

```bash
pip install twd
twd user username --limit 1000
```

---

## 无代码工具

### 1. Apify Twitter Scraper

- **网址**: https://apify.com/apify/twitter-scraper
- **价格**: 免费层 $5/月，付费 $49+/月
- **特点**: 无代码、可视化、支持大规模

### 2. PhantomBuster

- **网址**: https://phantombuster.com/
- **价格**: $30-569/月
- **特点**: 自动化、云端运行

### 3. Tweet Scraper V2

- **网址**: https://mapsscraper.ai/
- **价格**: 按需付费
- **特点**: 支持大量数据、API 访问

### 4. N8N（自建自动化）

开源工作流工具，可以结合 Twitter API：

```bash
npm install -g n8n
n8n start
```

---

## 推荐方案

### 对于个人使用（推荐）

**方案 1: twscrape（最佳免费方案）**

```bash
# 1. 安装
pip install twscrape

# 2. 准备 2-3 个备用 Twitter 账号
# 3. 添加账号
twscrape add_accounts

# 4. 下载推文
twscrape user_tweets username --limit 1000 --format json > tweets.json
```

**优点**: 免费、无限制、稳定
**缺点**: 需要管理多个账号

---

**方案 2: 官方 API（适合少量数据）**

如果你只需要获取少量推文（< 1000条/月），且预算充足：

- 使用官方 API + Tweepy
- 成本：$100/月（Basic 层）

---

### 对于大规模采集

**方案: Apify 或 PhantomBuster**

- 成本：$49-500/月
- 优点：云端运行、无代码、稳定
- 缺点：成本高

---

## 实践示例

### 完整的 Twitter 数据采集脚本

创建一个完整的采集脚本：

```python
# twitter_collector.py
import asyncio
import json
from datetime import datetime
from pathlib import Path
from twscrape import API

class TwitterCollector:
    def __init__(self):
        self.api = API()

    async def login(self):
        """登录账号池"""
        await self.api.pool.login()
        print("✓ 账号池已登录")

    async def get_user_tweets(self, username, limit=100):
        """获取指定用户的推文"""
        try:
            user = await self.api.user_by_login(username)
            print(f"✓ 找到用户: @{username} (ID: {user.id})")

            tweets = []
            async for tweet in self.api.user_tweets(user.id, limit=limit):
                tweets.append({
                    'id': str(tweet.id),
                    'date': tweet.date.isoformat(),
                    'content': tweet.rawContent,
                    'likes': tweet.likeCount,
                    'retweets': tweet.retweetCount,
                    'replies': tweet.replyCount,
                    'views': tweet.viewCount,
                    'url': f"https://twitter.com/{username}/status/{tweet.id}"
                })

            print(f"✓ 获取了 {len(tweets)} 条推文")
            return tweets

        except Exception as e:
            print(f"✗ 错误: {e}")
            return []

    async def get_following_tweets(self, username, tweets_per_user=50):
        """获取关注用户的所有推文"""
        try:
            user = await self.api.user_by_login(username)

            # 获取关注列表
            following = []
            async for f in self.api.following(user.id, limit=1000):
                following.append(f)

            print(f"✓ 正在下载 {len(following)} 个用户的推文...")

            all_tweets = []
            for i, f in enumerate(following, 1):
                print(f"[{i}/{len(following)}] @{f.username}...")
                tweets = await self.get_user_tweets(f.username, tweets_per_user)
                all_tweets.extend(tweets)

            return all_tweets

        except Exception as e:
            print(f"✗ 错误: {e}")
            return []

    def save_tweets(self, tweets, filename):
        """保存推文到文件"""
        # 创建输出目录
        Path("twitter_data").mkdir(exist_ok=True)

        # 保存 JSON
        json_path = f"twitter_data/{filename}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(tweets, f, ensure_ascii=False, indent=2)

        # 保存 Markdown（可读性更好）
        md_path = f"twitter_data/{filename}.md"
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(f"# Twitter 数据采集\n\n")
            f.write(f"采集时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"推文数量: {len(tweets)}\n\n")
            f.write("---\n\n")

            for tweet in tweets:
                f.write(f"## {tweet['date']}\n")
                f.write(f"**作者**: @{tweet.get('author', 'N/A')}\n\n")
                f.write(f"{tweet['content']}\n\n")
                f.write(f"**互动数据**:\n")
                f.write(f"- 👍 赞: {tweet['likes']}\n")
                f.write(f"- 🔄 转: {tweet['retweets']}\n")
                f.write(f"- 💬 回: {tweet['replies']}\n")
                f.write(f"- 👁️ 看: {tweet.get('views', 'N/A')}\n")
                f.write(f"**链接**: {tweet['url']}\n\n")
                f.write("---\n\n")

        print(f"✓ 已保存到 {json_path} 和 {md_path}")

# 使用示例
async def main():
    collector = TwitterCollector()
    await collector.login()

    # 方式 1: 获取单个用户的推文
    tweets = await collector.get_user_tweets('jessetrived', limit=100)
    collector.save_tweets(tweets, 'jessetrived')

    # 方式 2: 获取关注列表的所有推文
    # all_tweets = await collector.get_following_tweets('your_username', tweets_per_user=50)
    # collector.save_tweets(all_tweets, 'following_all')

if __name__ == "__main__":
    asyncio.run(main())
```

### 使用方法

```bash
# 1. 安装依赖
pip install twscrape

# 2. 添加账号
twscrape add_accounts

# 3. 运行脚本
python twitter_collector.py
```

---

## 数据存储建议

### 1. 文件存储（小规模）
```
twitter_data/
├── user1_tweets.json
├── user1_tweets.md
├── user2_tweets.json
└── user2_tweets.md
```

### 2. 数据库存储（中大规模）

**SQLite 方案**:
```python
import sqlite3

conn = sqlite3.connect('tweets.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS tweets (
        id TEXT PRIMARY KEY,
        author TEXT,
        date TEXT,
        content TEXT,
        likes INTEGER,
        retweets INTEGER
    )
''')

# 插入数据
c.execute('INSERT INTO tweets VALUES (?,?,?,?,?,?)', (...))
conn.commit()
```

**MongoDB 方案**:
```python
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.twitter_db
tweets_collection = db.tweets

tweets_collection.insert_many(tweets)
```

---

## 法律和伦理注意事项

⚠️ **重要提醒**:

1. **遵守 Twitter 服务条款**
   - 不要过于频繁地请求
   - 遵守 robots.txt
   - 不要用于商业目的（除非获得许可）

2. **数据使用**
   - 尊重原作者版权
   - 注明数据来源
   - 不用于恶意目的

3. **账号安全**
   - 使用专门的采集账号
   - 不要使用主账号
   - 定期轮换账号

4. **速率限制**
   - 添加延迟避免被封
   - 使用代理 IP（如果大规模采集）

---

## 常见问题

### Q1: twscrape 提示账号被锁定？
**A**: 使用多个账号轮换，添加延迟：
```python
import asyncio
await asyncio.sleep(2)  # 每次请求间隔 2 秒
```

### Q2: 如何获取历史推文（超过 3200 条）？
**A**: Twitter 官方限制只能访问最近 3200 条。如需更多，考虑：
- 使用第三方数据服务商（如 Nuzzel、TweetArchivist）
- 定期备份新增推文

### Q3: 如何下载推文中的图片/视频？
**A**: 使用 gallery-dl:
```bash
gallery-dl --filter "type:tweets" https://twitter.com/username
```

### Q4: API 价格太贵有替代方案吗？
**A**:
- 使用 twscrape（免费但需要多个账号）
- 使用 Apify 的免费层（$5/月额度）
- 使用学术机构的 Twitter API 访问权限

---

## 总结

**快速上手推荐**：

1. **免费方案**: twscrape
   ```bash
   pip install twscrape
   twscrape add_accounts
   twscrape user_tweets username --limit 1000
   ```

2. **付费稳定方案**: X API + Tweepy
   - 月费 $100
   - 适合需要稳定性的项目

3. **无代码方案**: Apify
   - 月费 $49 起
   - 适合非技术人员

**开始使用**: 推荐先用 twscrape 测试，满足需求后再考虑付费方案。

---

## 资源链接

- [twscrape GitHub](https://github.com/vladkens/twscrape)
- [Tweepy 文档](https://docs.tweepy.org/)
- [X API 官方文档](https://developer.x.com/en/docs/twitter-api)
- [Apify Twitter Scraper](https://apify.com/apify/twitter-scraper)
- [Twitter 数据采集最佳实践](https://github.com/shreya96/twitter-data-collection-guide)
