from flask import Flask, redirect, url_for, render_template, request
from facebook_scraper import get_posts
import tweepy
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np
import warnings
import re
from flask_mail import Mail, Message
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import RegexpTokenizer #used to tokenize into words and remove punctuation
import newspaper
import collections
import re
from newspaper import Article
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.sentiment import SentimentIntensityAnalyzer
import spacy
from spacy import displacy
from collections import Counter
nlp = spacy.load('en_core_web_sm')
try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")
import sys

app = Flask(__name__)

app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'infoforkrestaurant@gmail.com',
    MAIL_PASSWORD = 'mieoxumiyevgwegm',
))

mail = Mail(app)

def remove_emojis(data):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', data)

def retrieveFacebook(pageName, count):
    warnings.filterwarnings('ignore')
    data = []
    i = -1

    for post in get_posts(pageName , pages=count):
        i+=1
        mypost = post['text']
        mypost = re.split("Likes[0-9]+", mypost)
        mypost = mypost[0].rsplit("Play Video")
        #data.append([post['post_url'], post['images'], post['post_id'], remove_emojis(mypost[0].replace('\n', " "))])
        data.append([remove_emojis(mypost[0].replace('\n', " ")), post['post_url']])
    return (data)

def search_for_hashtags(hashtag_phrase, value):
    tweetList = []
    # this creates input boxes where you will input your keys given to you by twitter
    consumer_key = "6VtGqzLes6zc5xJ1150c6tl58"
    consumer_secret = "Irn493VD9OHaNFi9r9h5vF0zR9wTZZSriNj4z3apFWjw7mTOSL"
    access_token = "1503333538913038340-IO8RIL358RkImPTRZ6SiAjeDodsRNA"
    access_token_secret = "WckCE4JE7uw3vprz4v7786QpF3WhAjhBFfyoBW6b1Vhw5"

    # create an authorization for accessing Twitter (aka tell the program we have permission to do what we're doing)
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # initialize Tweepy API
    api = tweepy.API(auth)

    for tweet in tweepy.Cursor(api.search_tweets, q=hashtag_phrase + '-filter:retweets', count=100,
                               tweet_mode='extended', lang="en").items(int(value)):
        text = tweet._json["full_text"]
        link = 'https://twitter.com/twitter/statuses/' + str(tweet._json['id'])
        tweetList.append([text.replace('\n', " "), link])
    return tweetList

def UrltoHTML(query, value):
    allUrls = []
    for url in search(query, tld="co.in", num=int(value), stop=int(value), pause=2):
        allUrls.append(url)
    return(allUrls)

def NewspapertoHTML(webLink):
    site = newspaper.build(webLink, memoize_articles=False)
    allUrls = []
    for article in site.articles:
        allUrls.append(article.url)
    return allUrls

def retrieveArticle(links, value):
    count = 0
    ArticleList = []
    #article = ""
   
    for r in links:
        if count == value:
            break
        article_name = Article(r)
        
        article_name.download()
        try:
            article_name.parse()
            article_name.nlp() 
            article = article_name.summary
  
        except Exception:
            pass
        count += 1

        ArticleList.append([article.replace('\n', ' '), r])

    return ArticleList

tokenizer = RegexpTokenizer(r'\w+')

def tokenise(PassedData):
    tokens_document = []
    for x in range(len(PassedData)):
        tokens_document.append([tokenizer.tokenize(PassedData[x][0]), PassedData[x][1]])
    return tokens_document

def caseFold(PassedData):  # function which handles casefolding
    casefoldedList = []
    for x in range(len(PassedData)):
        CaseFolded = [word.casefold() for word in PassedData[x][0]]
        casefoldedList.append([CaseFolded, PassedData[x][1]])

    return casefoldedList

def stopWordRemoval(PassedData): #stopwords is used from nltk and stopWordRemoval is called to remove stop words from the passed document
    stopWordList = []
    for x in range(len(PassedData)):
        stopWord = [word for word in PassedData[x][0] if not word in stopwords.words('english')]
        stopWordList.append([stopWord, PassedData[x][1]])
    return stopWordList


def cleanData(passedData):
    Mytoken = tokenise(passedData)
    MyCase = caseFold(Mytoken)
    MyStop = stopWordRemoval(MyCase)
    MyStem = stemm(MyStop)

    return (MyStem)

def stemm(PassedData): #function which handles a documents stemming
    Stem = PorterStemmer()
    stemmWordList = []
    for x in range(len(PassedData)):
        stemmList = [Stem.stem(word) for word in PassedData[x][0]]
        stemmWordList.append([stemmList, PassedData[x][1]])
    return stemmWordList

JoinedData = []
orderedTopicDict = {}

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        if request.form['submit_button'] == 'Add Data':
            data = request.form
            Twitter = data["Twitter Hashtag"]
            Facebook = data["Facebook group"]
            Article = data["Article Link"]
            Google = data["Google term"]

            #Twitter
            value = 100
            TW = []
            if(Twitter):
                TW = search_for_hashtags(Twitter, value)

            #Articles
            MaxArticles = 5
            ART = []
            if(Article):
                allLinks = NewspapertoHTML(Article)
                ART = retrieveArticle(allLinks, MaxArticles)

            #Facebook
            FB = []
            if(Facebook):
                pagecount = 10
                FB = retrieveFacebook(Facebook, pagecount)

            # Google
            WEB = []
            if(Google):
                value = 5
                Links = UrltoHTML(Google, value)
                print(Links, file=sys.stderr)
                WEB = retrieveArticle(Links, value)

            JoinedData.extend(TW + FB + ART + WEB)

            return render_template("index.html", data=JoinedData, len=len(JoinedData))

        if request.form['submit_button'] == 'Remove Data':
            JoinedData.clear()
            orderedTopicDict.clear()
            return render_template("index.html", data=JoinedData, len=len(JoinedData))

        if request.form['submit_button'] == 'Process Data':
            orderedTopicDict.clear()
            for x in range(len(JoinedData)):  # Filter out links
                JoinedData[x][0] = re.sub(r'http\S+', '', JoinedData[x][0])
                JoinedData[x][0] = re.sub('[!@#$]', '', JoinedData[x][0])

            CleanedData = cleanData(JoinedData)
            AllData = []
            for x in range(len(CleanedData)):
                Sentence = ""
                for word in CleanedData[x][0]:
                    Sentence += word + " "
                AllData.append([Sentence, CleanedData[x][1]])

            sia = SentimentIntensityAnalyzer()
            ScoredDataTwo = []
            for x in range(len(JoinedData)):
                Score = sia.polarity_scores(JoinedData[x][0])

                S = "Positive: " + str(round(Score['pos'] * 100, 2)) + "% " + "Negative: " + str(
                round(Score['neg'] * 100, 2)) + "% " + "Neutral: " + str(round(Score['neu'] * 100, 2)) + "%"

                ScoredDataTwo.append([JoinedData[x][0], S, JoinedData[x][1]])

            GetToken = []
            for x in range(len(CleanedData)):
                GetToken.append(CleanedData[x][0])

            tfIdfV = TfidfVectorizer(tokenizer=lambda doc: doc, lowercase=False)
            tfIdfarr = tfIdfV.fit_transform(GetToken)
            vocab_tfIdf = tfIdfV.get_feature_names()

            lda_model = LatentDirichletAllocation(n_components=8)

            # fit transform on model on our count_vectorizer : running this will return our topics
            X_topics = lda_model.fit_transform(tfIdfarr)

            # .components_ gives us our topic distribution
            topic_words = lda_model.components_

            n_top_words = 8
            Topiclist = []
            for i, topic_dist in enumerate(topic_words):
                sorted_topic_dist = np.argsort(topic_dist)

                topic_words = np.array(vocab_tfIdf)[sorted_topic_dist]

                topic_words = topic_words[:-n_top_words:-1]
                #print("Topic", chr(i + 65), topic_words)
                Topiclist.append(topic_words)

            # To view what topics are assigned to the douments:
            topicDict = {}
            doc_topic = lda_model.transform(tfIdfarr)

            # iterating over ever value till the end value
            for n in range(doc_topic.shape[0]):

                # argmax() gives maximum index value
                topic_doc = doc_topic[n].argmax()

                Topic = "Topic: " + chr(topic_doc + 65) + " " + str(Topiclist[topic_doc])
                topicDict.setdefault(Topic,[]).append(ScoredDataTwo[n])

            orderedTopicDict.update(collections.OrderedDict(sorted(topicDict.items())))

            SpacyList = []
            for key, value in orderedTopicDict.items():
                AllWords = ''
                for x in range(len(value)):
                    AllWords = AllWords + ''.join(value[x][0])
                article = nlp(AllWords)
                items = [x.text for x in article.ents]
                TopFive = Counter(items).most_common(5)

                SpacyList.append([key,TopFive])

            return render_template("index.html", data=JoinedData, len=len(JoinedData), data2=orderedTopicDict, data3=SpacyList, len3=len(SpacyList))

        if request.form['submit_button'] == 'Email Data':
            data = request.form
            Email = data["Email"]
            msg = Message('Processed Data', sender='infoforkrestaurant@gmail.com', recipients=[Email])
            MyBody = ""
            for key, value in orderedTopicDict.items():
                MyBody += str(key) + "\n\n"
                for v in value:
                    MyBody += v[0] + "\n"
                    MyBody += v[1] + "\n"
                    MyBody += v[2] + "\n\n"
            msg.body = MyBody
            mail.send(msg)

            orderedTopicDict.clear()
            JoinedData.clear()

            return render_template("index.html")

    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run()