from reddit import RedditClient


LP_SUBREDDITS = ["learning_path", "EasyLevels", "TopLevels"]


def fetch_ideas(reddit_client: RedditClient) -> dict:
    return {
        key: reddit_client.get_reddit_top(subreddit=key) for key in LP_SUBREDDITS
    }
