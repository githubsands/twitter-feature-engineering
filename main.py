# https://docs.tweepy.org/en/stable/client.html#

import tweepy
import os

APIKEY=os.environ.get("APIKEY")
API_KEY_SECRET=os.environ.get("API_KEY_SECRET")
BEARER_TOKEN=os.environ.get("BEARER_TOKEN")
ACCESS_TOKEN=os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET=os.environ.get("ACCESS_TOKEN_SECRET")
USER=os.environ.get("USER")

class twitter_client():
    def __init__(self):
        try:
            client = tweepy.Client(bearer_token=BEARER_TOKEN,consumer_key=APIKEY,consumer_secret=API_KEY_SECRET,access_token=ACCESS_TOKEN,access_token_secret=ACCESS_TOKEN_SECRET)
            auth = tweepy.OAuth2BearerHandler(BEARER_TOKEN)
            api = tweepy.API(auth,wait_on_rate_limit=True)
        except ValueError as e:
            print("received error", e)
        else:
            self.client=client
            self.api=api

class follower_manager(twitter_client):
    def __init__(self):
        pass
    def unfollow_nonfriends(self):
        friends = self.api.get_follower_ids(user_id=USER)
        following = self.api.get_friend_ids()
        for followed_user in following:
            for friend in friends:
                if friend != followed_user:
                    print(followed_user)
                    try:
                        self.api.destroy_friendship(user_id=followed_user)
                    except ValueError as e:
                        print("received error", e)
                        pass
                    else:
                        print("unfollowed succeeded")
                        break


class list_manager(twitter_client):
    def __init__(self):
        twitter_client.__init__(self)
        pass
    def get_tweets_in_list(self,list_id):
        tweets = self.client.get_list_tweets(list_id)
    def add_steady_feed(self):
        resp = self.client.get_list_members(id=12)

def main():
    lm=list_manager()
    lm.get_tweets_in_list("steadyfeed")

if __name__ == "__main__":
    main()
