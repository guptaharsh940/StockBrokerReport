import feedparser
import requests
NewsFeed = feedparser.parse('https://economictimes.indiatimes.com/markets/stocks/rssfeeds/2146842.cms')
feed_list1 = []
feed_list2 = []
# print(NewsFeed.entries[0)
for i in range (50):
    entry = NewsFeed.entries[i]
    print(entry['title'])
    feed_list1.append(entry['title'])
# print(len(feed_list1))
for x in feed_list1:
    if 'target price' in x:
        print(x)

