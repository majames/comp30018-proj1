#!/usr/bin/python
""" Tweets extractor """

import re
import sys
from nltk.corpus import stopwords

def read_tweets_file(filename):
    """ Read the raw user id.-tweet tupples in 
        (assume a tweet ends in a time-stamp) """
    f = open(filename, 'rU')
    text = f.read()
    f.close()

    # look for a time-stamp which signifies the end of a tweet
    tweets = re.findall(r'(\d+)\t(\d+)\t(.+)\d+-\d+-\d+ \d+:\d+:\d+', text)

    return tweets

def modify_tweets(tweets, flag):
    """ Modify the raw user id.-tweet tupples to be lower case and contain only 
        alphabetic characters (including space)"""
    
    # sort the tweets by user id then tweet id then tweet text 
    tweets = sorted(tweets)
    
    stop = stopwords.words('english')
    mtweets = []
    for tweet in tweets:
        # make all letters in the tweet text lower case
        mtweet_text = tweet[2].lower()

        # remove all non-alphabetic characters (excluding space)
        mtweet_text = re.sub(r'[^a-z ]', '', mtweet_text)

        if (flag == '-B'):
            mtweet_words = mtweet_text.split(' ')

            # remove words that are 2 characters or less
            mtweet_words = [word for word in mtweet_words if len(word) > 2]
            
            # remove common words
            mtweet_words = [word for word in mtweet_words if word not in stop]

            mtweet_text = ' '.join(mtweet_words)

        if mtweet_text:
            mtweets.append((tweet[0], tweet[1], mtweet_text))

    return mtweets


def write_tweets_to_file(tweets, filename):
    """ Write the modified user id.-tweet tupples to file 
        (seperated by a newline) """
    f = open(filename, 'w')
    # convert the tweets from a 2d tupple to a tab seperated string
    tweets = ['\t'.join(tweet) + '\n' for tweet in tweets]

    # write the tweets to file
    f.writelines(tweets)
    f.close()


def main():
    """ Entry point """
    if len(sys.argv) != 4:
        print('usage: tweets-extractor.py FLAG src-file ' 
              'destination-file')
        sys.exit()


    src_filename = sys.argv[2]
    dest_filename = sys.argv[3]

    tweets = []
    tweets = read_tweets_file(src_filename)

    tweets = modify_tweets(tweets, sys.argv[1])
    write_tweets_to_file(tweets, dest_filename)

if __name__ == '__main__':
    main()

