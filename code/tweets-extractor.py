#!/usr/bin/python3
""" Tweets extractor """

import re
import sys

def read_tweets_file(filename):
    """ Read the raw user id.-tweet tupples in 
        (assume a tweet ends in a time-stamp) """
    f = open(filename, 'rU')
    text = f.read()
    f.close()

    # look for a time-stamp which signifies the end of a tweet
    tweets = re.findall(r'(\d+)\t\d+\t(.+)\d+-\d+-\d+ \d+:\d+:\d+', text)

    return tweets

def modify_tweets(tweets, flag):
    """ Modify the raw user id.-tweet tupples to be lower case and contain only 
        alphabetic characters (including space)"""
    
    # sort the tweets by user id
    tweets = sorted(tweets)
    
    mtweets = []
    for tweet in tweets:
        # make all letters in the tweet text lower case
        mtweet_text = tweet[1].lower()

        # remove all non-alphabetic characters (excluding space)
        mtweet_text = re.sub(r'[^a-z ]', '', mtweet_text)

        # remove words that are 2 characters or less
        if (flag == '-B'):
            mtweet_words = mtweet_text.split(' ')
            mtweet_words = [word for word in mtweet_words if len(word) > 2]
            mtweet_text = ' '.join(mtweet_words)

        # if the tweet id already has an entry append the tweet text
        if mtweets and mtweets[-1][0] == tweet[0]:
            mtweets[-1] = (mtweets[-1][0], mtweets[-1][1] + ' ' + mtweet_text)
        else:
            mtweets.append((tweet[0], mtweet_text))

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

