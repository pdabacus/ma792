"""
scrape tweets from twitter
"""
import requests

_version = "1.0.0"

apikey = "AAAAAAAAAAAAAAAAAAAAANRILgAA    REDACTED    H5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"

url = "https://api.twitter.com/2/tweets/search/recent?query=tsla"

h = {"authorization": "Bearer " + apikey}
resp = requests.request("GET", url, headers=h)
print(resp)
print(resp.json())
