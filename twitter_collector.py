#!/usr/bin/env python3
"""
Twitter 数据采集工具
使用 twscrape 库从 Twitter/X 采集用户推文

使用方法：
1. 安装依赖: pip install twscrape
2. 添加账号: twscrape add_accounts
3. 运行脚本: python twitter_collector.py @username
"""

import asyncio
import json
import argparse
from datetime import datetime
from pathlib import Path
from twscrape import API, gather
from twscrape.logger import set_log_level


class TwitterCollector:
    """Twitter 数据采集器"""

    def __init__(self, log_level="INFO"):
        """初始化采集器"""
        self.api = API()
        set_log_level(log_level)

    async def login(self):
        """登录账号池"""
        print("🔐 正在登录账号池...")
        await self.api.pool.login()
        print("✓ 账号池已登录")

    async def get_user_info(self, username):
        """获取用户信息"""
        print(f"🔍 正在查找用户 @{username}...")
        try:
            user = await self.api.user_by_login(username)
            print(f"✓ 找到用户: {user.display_name} (@{username})")
            print(f"  - ID: {user.id}")
            print(f"  - 粉丝: {user.followersCount:,}")
            print(f"  - 关注: {user.friendsCount:,}")
            print(f"  - 推文: {user.statusesCount:,}")
            return user
        except Exception as e:
            print(f"✗ 错误: {e}")
            return None

    async def get_user_tweets(self, username, limit=100):
        """
        获取指定用户的推文

        Args:
            username: Twitter 用户名（不含 @）
            limit: 获取推文数量

        Returns:
            推文列表
        """
        user = await self.get_user_info(username)
        if not user:
            return []

        print(f"\n📥 正在获取推文（最多 {limit} 条）...")
        tweets = []

        try:
            async for tweet in self.api.user_tweets(user.id, limit=limit):
                tweets.append({
                    'id': str(tweet.id),
                    'date': tweet.date.isoformat(),
                    'content': tweet.rawContent,
                    'likes': tweet.likeCount,
                    'retweets': tweet.retweetCount,
                    'replies': tweet.replyCount,
                    'views': tweet.viewCount,
                    'url': f"https://twitter.com/{username}/status/{tweet.id}",
                    'author': username,
                    'author_id': str(user.id),
                })

                # 实时显示进度
                if len(tweets) % 10 == 0:
                    print(f"  已获取 {len(tweets)} 条...")

            print(f"✓ 成功获取 {len(tweets)} 条推文")
            return tweets

        except Exception as e:
            print(f"✗ 采集失败: {e}")
            return []

    async def get_following_list(self, username, limit=200):
        """
        获取用户的关注列表

        Args:
            username: Twitter 用户名
            limit: 最大关注数量

        Returns:
            关注的用户列表
        """
        user = await self.get_user_info(username)
        if not user:
            return []

        print(f"\n👥 正在获取关注列表...")
        following = []

        try:
            async for f in self.api.following(user.id, limit=limit):
                following.append({
                    'username': f.username,
                    'id': str(f.id),
                    'display_name': f.display_name,
                    'followers': f.followersCount,
                    'following': f.friendsCount,
                })

            print(f"✓ 找到 {len(following)} 个关注的用户")
            return following

        except Exception as e:
            print(f"✗ 获取失败: {e}")
            return []

    async def get_following_tweets(self, username, tweets_per_user=20, max_users=10):
        """
        获取关注用户的所有推文

        Args:
            username: Twitter 用户名
            tweets_per_user: 每个用户获取的推文数
            max_users: 最多获取多少个用户的推文

        Returns:
            所有推文列表
        """
        following = await self.get_following_list(username, limit=max_users)
        if not following:
            return []

        print(f"\n📥 正在下载关注用户的推文（每人最多 {tweets_per_user} 条）...")

        all_tweets = []
        for i, user in enumerate(following, 1):
            print(f"\n[{i}/{len(following)}] @{user['username']} ({user.get('display_name', 'N/A')})")
            tweets = await self.get_user_tweets(user['username'], limit=tweets_per_user)
            all_tweets.extend(tweets)

            # 添加延迟避免被限制
            await asyncio.sleep(1)

        return all_tweets

    def save_json(self, data, filename):
        """保存为 JSON 格式"""
        output_dir = Path("twitter_data")
        output_dir.mkdir(exist_ok=True)

        filepath = output_dir / f"{filename}.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"✓ 已保存到 {filepath}")
        return filepath

    def save_markdown(self, tweets, filename):
        """保存为 Markdown 格式（更好的可读性）"""
        output_dir = Path("twitter_data")
        output_dir.mkdir(exist_ok=True)

        filepath = output_dir / f"{filename}.md"
        with open(filepath, 'w', encoding='utf-8') as f:
            # 写入标题
            f.write(f"# Twitter 数据采集\n\n")
            f.write(f"**采集时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**推文数量**: {len(tweets)}\n\n")
            f.write("---\n\n")

            # 写入每条推文
            for tweet in tweets:
                f.write(f"## {tweet['date']}\n\n")
                f.write(f"**作者**: @{tweet.get('author', 'N/A')}\n\n")
                f.write(f"{tweet['content']}\n\n")

                # 互动数据
                f.write(f"**互动数据**:\n")
                f.write(f"- 👍 赞: {tweet['likes']:,}\n")
                f.write(f"- 🔄 转: {tweet['retweets']:,}\n")
                f.write(f"- 💬 回: {tweet['replies']:,}\n")
                if tweet.get('views'):
                    f.write(f"- 👁️ 看: {tweet['views']:,}\n")

                f.write(f"\n**链接**: {tweet['url']}\n\n")
                f.write("---\n\n")

        print(f"✓ 已保存到 {filepath}")
        return filepath

    def save_csv(self, tweets, filename):
        """保存为 CSV 格式（便于 Excel 打开）"""
        import csv

        output_dir = Path("twitter_data")
        output_dir.mkdir(exist_ok=True)

        filepath = output_dir / f"{filename}.csv"
        with open(filepath, 'w', encoding='utf-8-sig', newline='') as f:
            if not tweets:
                return

            writer = csv.DictWriter(f, fieldnames=[
                'date', 'author', 'content', 'likes', 'retweets',
                'replies', 'views', 'url'
            ])
            writer.writeheader()

            for tweet in tweets:
                writer.writerow({
                    'date': tweet['date'],
                    'author': tweet.get('author', ''),
                    'content': tweet['content'],
                    'likes': tweet['likes'],
                    'retweets': tweet['retweets'],
                    'replies': tweet['replies'],
                    'views': tweet.get('views', ''),
                    'url': tweet['url']
                })

        print(f"✓ 已保存到 {filepath}")
        return filepath


async def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='Twitter 数据采集工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 采集单个用户的推文
  python twitter_collector.py @elonmusk -n 100

  # 采集关注用户的推文
  python twitter_collector.py @myusername --following --max-users 20

  # 仅保存为 CSV
  python twitter_collector.py @username -n 50 --format csv
        """
    )

    parser.add_argument('username', help='Twitter 用户名（可以带 @）')
    parser.add_argument('-n', '--number', type=int, default=100,
                       help='获取推文数量（默认: 100）')
    parser.add_argument('--following', action='store_true',
                       help='获取该用户关注的所有人的推文')
    parser.add_argument('--max-users', type=int, default=10,
                       help='最多获取多少个关注用户的推文（默认: 10）')
    parser.add_argument('--tweets-per-user', type=int, default=20,
                       help='每个用户获取的推文数（默认: 20）')
    parser.add_argument('--format', choices=['json', 'markdown', 'csv', 'all'],
                       default='all', help='输出格式（默认: all）')
    parser.add_argument('--output', help='输出文件名（不含扩展名）')
    parser.add_argument('--debug', action='store_true',
                       help='显示调试日志')

    args = parser.parse_args()

    # 去掉 @ 符号
    username = args.username.lstrip('@')

    # 设置输出文件名
    output_name = args.output or f"{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    # 创建采集器
    collector = TwitterCollector(log_level="DEBUG" if args.debug else "INFO")

    # 登录
    await collector.login()

    # 采集数据
    if args.following:
        print(f"\n{'='*60}")
        print(f"采集模式: 关注列表")
        print(f"目标用户: @{username}")
        print(f"最多用户: {args.max_users}")
        print(f"每用户推文: {args.tweets_per_user}")
        print(f"{'='*60}\n")

        tweets = await collector.get_following_tweets(
            username,
            tweets_per_user=args.tweets_per_user,
            max_users=args.max_users
        )
    else:
        print(f"\n{'='*60}")
        print(f"采集模式: 单个用户")
        print(f"目标用户: @{username}")
        print(f"推文数量: {args.number}")
        print(f"{'='*60}\n")

        tweets = await collector.get_user_tweets(username, limit=args.number)

    if not tweets:
        print("\n❌ 没有获取到推文")
        return

    # 保存数据
    print(f"\n{'='*60}")
    print("💾 正在保存数据...")
    print(f"{'='*60}\n")

    if args.format in ['json', 'all']:
        collector.save_json(tweets, output_name)

    if args.format in ['markdown', 'all']:
        collector.save_markdown(tweets, output_name)

    if args.format in ['csv', 'all']:
        collector.save_csv(tweets, output_name)

    print(f"\n{'='*60}")
    print("✅ 采集完成！")
    print(f"{'='*60}")
    print(f"\n数据统计:")
    print(f"  总推文数: {len(tweets)}")
    print(f"  总点赞数: {sum(t['likes'] for t in tweets):,}")
    print(f"  总转发数: {sum(t['retweets'] for t in tweets):,}")
    print(f"  总回复数: {sum(t['replies'] for t in tweets):,}")

    if tweets:
        print(f"\n时间范围:")
        dates = [t['date'] for t in tweets]
        print(f"  最早: {min(dates)}")
        print(f"  最新: {max(dates)}")

    print(f"\n文件保存在: twitter_data/")

    # 显示使用提示
    print(f"\n💡 提示:")
    print(f"  - JSON 格式适合程序处理")
    print(f"  - Markdown 格式适合人类阅读")
    print(f"  - CSV 格式可用 Excel 打开")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断")
    except Exception as e:
        print(f"\n\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
