# tracks the sentiment toward a given hashtag over time
# 20 mins got twitter stream printed out
# 40 mins got basic sentiment done
# 60 mins got stock price done and checked into git with externalised env vars <3

from birdy.twitter import StreamClient
from textblob import TextBlob
from datetime import datetime
import os
import sys


CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')


#TwitterClient File Stuff
client = StreamClient(CONSUMER_KEY,
                    CONSUMER_SECRET,
                    ACCESS_TOKEN,
                    ACCESS_TOKEN_SECRET)



#NLP File stuff


stock_price = [
    {
        "time": datetime.now(), 
        "price": 0, 
        "tweet": "Initialising...", 
        "polarity": 0
    }
]

def update_stock_price(tweet, polarity):
    stock_price.append({"time": datetime.now(), "price": stock_price[-1]["price"] + polarity, "tweet": tweet, "polarity": polarity})

def launch(term, limit):
    print("Parsing tweets for %s" %term)
    i = 1
    response = client.stream.statuses.filter.post(track="#%s" % term)
    for data in response.stream():
        if data.lang == 'en':
            tweet = TextBlob(data.text)
            update_stock_price(data.text, tweet.sentiment.polarity)
            s = "%s ---   %s" % (tweet.sentiment.polarity, data.text)
            print(s,end="\r", flush=True)
            i += 1
        if i >= limit:
            print(" Have done %s tweets, now exiting" % i)
            break

    print(len(stock_price))
    for price in stock_price:
        print("%s - %s" % (price["price"], price["tweet"]))



if __name__ == "__main__":
    term = sys.argv[1]
    limit = sys.argv[2]
    launch(term, int(limit))