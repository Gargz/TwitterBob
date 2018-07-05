import tweepy
import twitter_credentials
import time 
from datetime import datetime

auth = tweepy.OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

user = api.me()

print(user.name)

search_terms=("giveaway", "chance to win", "retweet to win")
n = 0
retweets_count = 0

def main():
   
    
    search = search_terms[n]

    NumberOfTweets = 30
    text_file = open('tweet_report.txt', 'w')
    

    for tweet in tweepy.Cursor(api.search, search).items(NumberOfTweets):

        if ("bot" in tweet.text or "b0t" in tweet.text or "Bot" in tweet.text or "BOT" in tweet.text or "B0T" in tweet.text):
            print("***********************   SKIPPING HONEYPOT   ******************************* ")
        else:

            try:
                print(tweet.text)
                tweet.retweet()
                retweets_count += 1



                print(" **********************************************************************")
                print("                                TWEET RETWEETED                       ")
                print ("Tweet number " + retweets_count)
                user_id = tweet.user.id
                print(user_id)
                try:
                    api.create_friendship(user_id)
                    print ("Friendship requested")
                except Exception:
                    pass
                if ("Like" in tweet.text or "like" in tweet.text or "Fav" in tweet.text or "fav" in tweet.text):
                    try:
                        api.create_favorite(tweet.id)
                        print("Tweet to favourite")
                    except Exception:
                        pass
                print ("Found by " + search)
                print(" ************************************************************************")
            



            except tweepy.TweepError as e:
                
                print(e.reason)
                if ("185" in e.reason):
                    print ("NEED TO WAIT")
                    print ("RESUME in 17 MINUTES")
                    print(str(time.ctime()))
                    time.sleep(1000)

            except StopIteration:
                break
        text_file.close()



if __name__ == '__main__':
    while True:
        main()
        print (n)
        print ("######################## CHANGING SEARCH TERM #############################")
        print (n+1)
        if (len(search_terms) > (n + 1)):
            n+=1
        else:
            n = 0
        time.sleep(10)
        

