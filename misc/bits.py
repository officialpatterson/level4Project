def tokenizedTweets(tweets):
    stemmer = nltk.stem.snowball.SnowballStemmer("english", ignore_stopwords=True)
    #for each tweet tokenize, remove stop words and stem
    for i in range(0, len(tweets)):
        tokensArray = []
        tokenizer = RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(tweets[i][0].lower())
        for token in tokens:
            token = stemmer.stem(token)
            if token not in stopwords.words('english'):
                
                if len(token) >2:
                    tokensArray.append(token)
        
        label = tweets[i][1]
        tweets[i]= (tokensArray, label)
    return tweets