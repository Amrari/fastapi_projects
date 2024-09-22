from ..reddit import RedditClient

LP_SUBREDDITS = ["learning", "easylevels", "TopLevels"]

# 1. Constructor Injection
class Ideas:
    def __init__(self, reddit_client: RedditClient):
        self.reddit_client = reddit_client

    def fetch_ideas(self) -> dict:
        return {
            key: self.reddit_client.get_reddit_top(subreddit=key)
            for key in LP_SUBREDDITS
        }


# 2. Setter Injection
class Ideas:
    _client = None

    def fetch_ideas(self) -> dict:
        return {
            key: self.client.get_reddit_top(subreddit=key) for key in LP_SUBREDDITS
        }

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, value: RedditClient):
        self._client = value


# Interface Injection
