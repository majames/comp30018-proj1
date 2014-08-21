#!/usr/bin/python3
""" Tweets extractor """

import re
import sys
import random

def read_tweets_file(filename, num_lines=None):
    """ Read the raw user id.-tweet tupples in 
        (assume a tweet ends in a time-stamp) """
    f = open(filename, 'rU')
    text = f.read()
    f.close()

    # look for a time-stamp which signifies the end of a tweet
    tweets = re.findall(r'(\d+)\t\d+\t(.+)\d+-\d+-\d+ \d+:\d+:\d+', text)
    if num_lines:
        tweets = random.sample(tweets, num_lines)

    return tweets

def modify_tweets(tweets):
    """ Modify the raw user id.-tweet tupples to be lower case and contain only 
        alphabetic characters (including space)"""
    mtweets = []
    for tweet in tweets:
        # make all letters in the tweet text lower case
        mtweet_text = tweet[1].lower()

        # remove all non-alphabetic characters (excluding space)
        mtweet_text = re.sub(r'[^a-z ]', '', mtweet_text)

        mtweets.append((tweet[0], mtweet_text))

    # sort the tweets by user id
    return sorted(mtweets)


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
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print('usage: tweets-extractor.py src-file ' 
              'destination-file [num_tweets]')
        sys.exit()

    src_filename = sys.argv[1]
    dest_filename = sys.argv[2]

    tweets = []
    if len(sys.argv) == 4:
        num_tweets = int(sys.argv[3])
        tweets = read_tweets_file(src_filename, num_lines=num_tweets)
    else:
        tweets = read_tweets_file(src_filename)

    tweets = modify_tweets(tweets)
    write_tweets_to_file(tweets, dest_filename)

if __name__ == '__main__':
    main()

