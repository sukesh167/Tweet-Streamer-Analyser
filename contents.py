# -*- coding: utf-8 -*-
from cleaner import cleaning
from tweepy import OAuthHandler, API, Cursor
from pycorenlp import StanfordCoreNLP

class get_tweets():
	def __init__(self,tweet):
		self.tweets=tweet
		self.created_at=tweet.created_at
		self.user_name=tweet.user.name
		self.full_text=tweet.full_text
		self.words=None
		self.clean_text=None
		self.retweet_count=tweet.retweet_count.real
		self.verified_user=tweet.user.verified
		self.sentiment=None
		self.sentiment_value=None

class content():
	def __init__(self):
		self.clean_tweets=None
		self.tweets=[]
		
		ACCESS_TOKEN = '1192350351078371329-L4MshX1GA8FicYhe8PDMmDaTUS9ayK'
		ACCESS_TOKEN_SECRET = '9H5VgkrTGnle6CsPpyfptgGONj0UuJK9rGrg5RZtduWLR'
		CONSUMER_KEY = 'dDHYwqdav0HFo96VJlqb92CPH'
		CONSUMER_SECRET = 'UDt6MwCZiGCfQwkYeD4d7GzOIEXZuOkF9HYA8APmVa9rFhd8wP'
		
		auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
		self.api = API(auth, wait_on_rate_limit=True)
		self.trends=self.api.trends_place(1)[0]['trends'][:5]	

	def tweet_search(self,query):
		for tweet in Cursor(self.api.search, q=query, lang="en", 
							tweet_mode="extended").items():
			self.tweets.append(get_tweets(tweet))
		
	def tweet_clean(self):
		self.clean_tweets=cleaning(self.tweets).clean_tweets

	def sentiment_analysis(self):
		nlp = StanfordCoreNLP('http://localhost:9000')
		for text in self.clean_tweets:
			result = nlp.annotate(text.clean_text,
					properties={
					'annotators': 'sentiment',
					'outputFormat': 'json',
					'timeout' : 75000})
			
			for s in result["sentences"]:
				text.sentiment=s["sentiment"]
				text.sentiment_value=s["sentimentValue"]
	


