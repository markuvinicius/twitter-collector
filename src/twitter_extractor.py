import argparse
import urlparse
import urllib
import tweepy
from cassandra.cluster import Cluster
import re
from configparser import ConfigParser

# URL handling
def url_fix(s, charset='utf-8'):
    if isinstance(s, unicode):
        s = s.encode(charset, 'ignore')
    scheme, netloc, path, qs, anchor = urlparse.urlsplit(s)
    path = urllib.quote(path, '/%')
    qs = urllib.quote_plus(qs, ':&=')
    return urlparse.urlunsplit((scheme, netloc, path, qs, anchor))


# Read and Parse the command line arguments
# Return values from 3 major parameters (language, auth_file, count)
def argument_parser():
    # USE EXAMPLES:
    # =-=-=-=-=-=-=
    # % twsearch <search term>            --- searches term
    # % twsearch <search term> -a auth.k  --- file containing the token and secret keys
    # % twsearch <search term> -l pt      --- searches term with lang=pt (Portuguese) <DEFAULT = pt>
    # % twsearch <search term> -c 100     --- searches term and returns 100 tweets (count=100) <DEFAULT = 100>

    # Parse the command line arguments
    parser = argparse.ArgumentParser(description='Twitter Search')
    parser.add_argument(action='store', dest='query', help='Search term string')
    parser.add_argument('-a', action='store', dest='a', help='Location of Auth File /usr/etc/auth.k')
    parser.add_argument('-l', action='store', dest='l', help='Language (en = English, fr = French, etc...)')
    parser.add_argument('-c', action='store', dest='c', help='Tweet count (must be <100)')
    args = parser.parse_args()

    query = args.query  # Actual query word(s)
    if not query:
        print("ERROR - A valid string query must be informed")
        exit()

    # auth file
    auth_file = args.a
    if (not auth_file):
        print("ERROR - Location for auth file must be informed")
        exit()

    # Language
    language = args.l
    if (not language):
        language = ""

    # Tweet count
    count = 0
    if args.c:
        count = int(args.c)
        if (count > cmax) or ( count < 1 ):
            print ("Resetting count to ", cmax, " (maximum allowed)")
            count = cmax
    else:
        count = 100

    print ("Query: Language: %s, Count: %s" % (language, count))

    dict_params = {'query'    : query,
                   'auth_file': auth_file,
                   'language' : language,
                   'count'    : count}

    return dict_params

# Read the Configuration File
def config_section_map(config,section):
    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                print "skip: %s" % option
        except:
            print "exception on %s!" % option
            dict1[option] = None
    return dict1

# AUTHENTICATION (OAuth)
def tw_oauth(authfile):
    with open(authfile, "r") as f:
        ak = f.readlines()
    f.close()

    auth1 = tweepy.auth.OAuthHandler(ak[0].replace("\n", ""), ak[1].replace("\n", ""))
    auth1.set_access_token(ak[2].replace("\n", ""), ak[3].replace("\n", ""))
    return tweepy.API(auth1)


# AUTHENTICATION (OAuth)
def twitter_autentication(twitter_config):
    auth1 = tweepy.auth.OAuthHandler(twitter_config['consumer_key'],
                                     twitter_config['consumer_secret'])

    auth1.set_access_token(twitter_config['key'],
                           twitter_config['secret'])

    return tweepy.API(auth1)

# INSERT DATA INTO CASSANDRA
def persist_data(tweet_list, params=None):
    host = [str(params['host'])]
    keyspace = str(params['keyspace'])
    cluster = Cluster(host)
    session = cluster.connect(keyspace)

    for tweet in tweet_list:
        session.execute(
            """
            INSERT INTO tweets (created, author_id, followers_count, 
                                friends_count, location, retweet_count, 
                                source, text, tweet_id, username, tag, 
                                process_date, lang)
            VALUES (%(created)s, %(author_id)s, %(followers_count)s, %(friends_count)s, %(location)s, 
                    %(retweet_count)s, %(source)s, %(text)s, %(tweet_id)s, %(username)s, %(tag)s, 
                    toDate(now()), %(lang)s )
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
             'tag': tweet['tag'],
             'lang': tweet['lang']
             }
        )


# Call the twitter api to fetch a bunch of data
def fetch_twitter_data(api, params=None):
    counter = 0
    twitter_list=[]

    for tweet in tweepy.Cursor(api.search,
                               q=params['query'],
                               lang=params['language'],
                               count=params['count']).items():
        twt={}

        # TWEET INFO
        twt['created'] = tweet.created_at
        twt['text'] = tweet.text
        twt['tweet_id'] = tweet.id
        twt['retwc'] = tweet.retweet_count

        # AUTHOR INFO
        twt['username'] = tweet.author.name
        twt['followers'] = tweet.author.followers_count
        twt['friends'] = tweet.author.friends_count
        twt['author_id'] = tweet.author.id
        twt['author_loc'] = tweet.author.location
        twt['lang'] = tweet.lang

        # QUERY
        twt['tag'] = params['query']

        # TECHNOLOGY INFO
        twt['source'] = tweet.source

        twitter_list.append(twt)
        counter = counter + 1

        if (counter == params['count']):
            break

    return twitter_list


if __name__ == "__main__":
    global cmax

    # Maximum allowed tweet count (note: Twitter sets this to ~180 per 15 minutes)
    cmax = 100


    # Parse the command line arguments
    params = argument_parser()

    # Read the configuration file
    config = ConfigParser()
    config.read(params['auth_file'])

    # Parse Twitter autentication parameters
    twitter_config = config_section_map(config,'TwitterSection')
    # Parse Cassandr autentication parameters
    cassandra_config = config_section_map(config, 'CassandraSection')

    # build a twitter connection using tweepy package
    api = twitter_autentication(twitter_config)

    # fetch a list of tweets according the paramaters
    tweet_list = fetch_twitter_data(api, params=params)
    if len(tweet_list)>0:
        persist_data(tweet_list, params=cassandra_config)
        print("SUCESS - Twitter Data Persisted on LZ by tag {} - {}".format(params['query'],len(tweet_list)))
    else:
        print("WARN - There is no tweets to persist")