class Tweet():
	def __init__(self, twitter_json):
		self.id = twitter_json['id']
		self.id_str = twitter_json['id_str']
		self.user = twitter_json['user']
		self.text = twitter_json['text'].lower()
		self.retweet_count = twitter_json['retweet_count']
		self.created_at = twitter_json['created_at']
		self.coordinates = twitter_json['coordinates']
		self.label = None
	def set_label(self, label):
		self.label = label
