import argparse
import urlparse
import urllib
import tweepy
from cassandra.cluster import Cluster
import re


# URL CLEANUP
def url_fix(s, charset='utf-8'):
    if isinstance(s, unicode):
        s = s.encode(charset, 'ignore')
    scheme, netloc, path, qs, anchor = urlparse.urlsplit(s)
    path = urllib.quote(path, '/%')
    qs = urllib.quote_plus(qs, ':&=')
    return urlparse.urlunsplit((scheme, netloc, path, qs, anchor))

# TEXT CLEANUP
def remove_non_ascii(text):
    return re.sub(r'[^\x00-\x7f]',r'', text)


# COMMAND PARSER
def tw_parser():
    global l, c, a, qw

    # USE EXAMPLES:
    # =-=-=-=-=-=-=
    # % twsearch <search term>            --- searches term
    # % twsearch <search term> -a auth.k  --- file containing the token and secret keys
    # % twsearch <search term> -l pt      --- searches term with lang=pt (Portuguese) <DEFAULT = pt>
    # % twsearch <search term> -c 100     --- searches term and returns 100 tweets (count=100) <DEFAULT = 100>

    # Parse the command
    parser = argparse.ArgumentParser(description='Twitter Search')
    parser.add_argument(action='store', dest='query', help='Search term string')
    parser.add_argument('-a', action='store', dest='a', help='Location of Auth File /usr/etc/auth.k')
    parser.add_argument('-l', action='store', dest='l', help='Language (en = English, fr = French, etc...)')
    parser.add_argument('-c', action='store', dest='c', help='Tweet count (must be <100)')
    args = parser.parse_args()

    qw = args.query  # Actual query word(s)

    # auth file
    a = args.a
    if (not a):
        print("ERROR - Location for auth file must be informed")
        exit()

    # Language
    l = args.l
    if (not l):
        l = "pt"

    # Tweet count
    if args.c:
        c = int(args.c)
        if (c > cmax):
            print ("Resetting count to ", cmax, " (maximum allowed)")
            c = cmax
        if (not (c) or (c < 1)):
            c = 1

    if not (args.c):
        c = 100

    print ("Query: Language: %s, Count: %s" % (l, c))


# AUTHENTICATION (OAuth)
def tw_oauth(authfile):
    with open(authfile, "r") as f:
        ak = f.readlines()
    f.close()
    auth1 = tweepy.auth.OAuthHandler(ak[0].replace("\n", ""), ak[1].replace("\n", ""))
    auth1.set_access_token(ak[2].replace("\n", ""), ak[3].replace("\n", ""))
    return tweepy.API(auth1)

# INSERT DATA INTO CASSANDRA
def persist_data(tweet_list):
    cluster = Cluster(['localhost'])
    session = cluster.connect('lz')

    for tweet in tweet_list:
        session.execute(
            """
            INSERT INTO tweets (created, author_id, followers_count, 
                                friends_count, location, retweet_count, 
                                source, text, tweet_id, username, tag)
            VALUES (%(created)s, %(author_id)s, %(followers_count)s, %(friends_count)s, %(location)s, 
                    %(retweet_count)s, %(source)s, %(text)s, %(tweet_id)s, %(username)s, %(tag)s)
            """,

            {'created': tweet['created'],
             'text': tweet['text'],
             'tweet_id': tweet['tweet_id'],
             'retweet_count': tweet['retwc'],
             'username': tweet['username'],
             'followers_count': tweet['followers'],
             'friends_count': tweet['friends'],
             'author_id': tweet['author_id'],
             'location': tweet['author_loc'],
             'source': tweet['source'],
             'tag': tweet['tag']}
        )

# TWEEPY SEARCH FUNCTION
def tw_search(api):
    counter = 0
    twitter_list=[]

    for tweet in tweepy.Cursor(api.search,
                               q=qw,
                               lang=l,
                               count=c).items():
        twt={}

        # TWEET INFO
        twt['created'] = tweet.created_at
        #twt['text'] = remove_non_ascii(tweet.text)
        twt['text'] = tweet.text
        twt['tweet_id'] = tweet.id
        twt['retwc'] = tweet.retweet_count

        # AUTHOR INFO
        twt['username'] = tweet.author.name
        twt['followers'] = tweet.author.followers_count
        twt['friends'] = tweet.author.friends_count
        twt['author_id'] = tweet.author.id
        twt['author_loc'] = tweet.author.location
        twt['tag'] = qw

        # TECHNOLOGY INFO
        twt['source'] = tweet.source

        twitter_list.append(twt)
        counter = counter + 1

        if (counter == c):
            break

    return twitter_list


if __name__ == "__main__":
    global api, cmax, locords

    # Maximum allowed tweet count (note: Twitter sets this to ~180 per 15 minutes)
    cmax = 100
    # OAuth key file

    tw_parser()
    api = tw_oauth(a)
    tw_list = tw_search(api)
    if len(tw_list)>0:
        persist_data(tw_list)
        print("SUCESS - Twitter Data Persisted on LZ by tag {}".format(qw))
    else:
        print("WARN - There is no tweets to persist")