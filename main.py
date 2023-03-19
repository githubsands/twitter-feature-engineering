# DOCS: https://docs.tweepy.org/en/stable/client.html#
import os
import logging
import colorlog
import tweepy
import sys

# TODO: You should add multiplie proxies and each submission through tweepy needs to alternate
# our servers
os.environ['HTTP_PROXY'] = ""
os.environ['HTTPS_PROXY'] = ""

class twitter_client():
    def __init__(self, USER, BEARER_TOKEN, APIKEY, APIKEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET):
        try:
            client = tweepy.Client(bearer_token=BEARER_TOKEN,consumer_key=APIKEY,consumer_secret=APIKEY_SECRET,access_token=ACCESS_TOKEN,access_token_secret=ACCESS_TOKEN_SECRET)
            print(BEARER_TOKEN)
            auth = tweepy.OAuth2BearerHandler(BEARER_TOKEN)
            print(auth)
            api = tweepy.API(auth,wait_on_rate_limit=True)
        except ValueError as e:
            print("received error", e)
        else:
            self.client=client
            self.api=api
            self.user=USER
            print("authentication succeeded")

class people_manager(twitter_client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def unfollow_nonfriends(self):
        friends = self.api.get_follower_ids(user_id=self.user)
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
    def list_friends(self):
        friends = self.api.get_follower_ids(user_id=self.user)
        for friend in friends:
            print(friends)

class list_manager(twitter_client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def get_tweets_in_list(self,list_id):
        tweets = self.client.get_list_tweets(list_id)
    def add_steady_feed(self):
        resp = self.client.get_list_members(id=12)
    def get_my_lists(self):
        lists = self.api.get_lists()
        print(lists)

class spaces_manager(twitter_client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass

def main():
    USER=os.environ.get("USER")
    APIKEY=os.environ.get("APIKEY")
    APIKEY_SECRET=os.environ.get("APIKEY_SECRET")
    BEARER_TOKEN=os.environ.get("BEARER_TOKEN")
    ACCESS_TOKEN=os.environ.get("ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET=os.environ.get("ACCESS_TOKEN_SECRET")
    USER=os.environ.get("USER")
    if APIKEY == None:
        print("must set apikey")
        sys.exit()
    elif APIKEY_SECRET == None:
        print("must set apikey_secret")
        sys.exit()
    elif BEARER_TOKEN == None:
        print("must set bearer token")
        sys.exit()
    elif ACCESS_TOKEN == None:
        print("must set access token")
        sys.exit()
    elif ACCESS_TOKEN_SECRET == None:
        print("must set access token secret")
        sys.exit()
    elif USER == None:
        print("must set access token secret")
        sys.exit()

    pm=people_manager(USER, BEARER_TOKEN, APIKEY, APIKEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    pm.list_friends()

if __name__ == "__main__":
    main()
