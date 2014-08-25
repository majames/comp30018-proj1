#!/usr/bin/python
""" Uses the fuzzywuzzy module to do global edit distance matching
    and local edit distance matching for strings """

import sys
import myparser
import timeit
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def token_set_alignment(tweets, locations):
    # initialise the list of matches and dictionary of
    # tweet i.d. - matches list pairs 
    d = {}
    matches = []

    for tweet in tweets:
        for location in locations:
            score = fuzz.token_set_ratio(tweet[1], location)
            if score >= 90:
                matches.append((location, score))
                print(matches[-1])
        d[tweet[0]] = matches

    print(d)

def global_edit_alignment(tweets, locations):
    """ Tokenize the location and the tweets into words,
        and compare """
    # initialise the list of matches and dictionary of
    # tweet i.d. - matches list pairs 
    d = {}
    matches = []

    for tweet in tweets:
        tweet_words = tweet[1].split(' ')
        print(tweet_words)
        for location in locations:
            num_location_words = len(location.split(' '))
            for i in range(0, len(tweet_words)):
                score = fuzz.ratio(location, 
                                   ' '.join(tweet_words[i:i+num_location_words]))
                if score >= 90:
                    matches.append((location, score))
                    # debugging
                    print(matches[-1])

        d[tweet[0]] = matches
        print(d)
        matches = []


def main():
    """ Entry point for the program """
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print('usage: editdistance.py tweets-file locations-file [num-tweets]')
        sys.exit()

    if len(sys.argv) == 4:
        tweets = myparser.parse_tweets(sys.argv[1], num_tweets=int(sys.argv[3]))
    else:
        tweets = myparser.parse_tweets(sys.argv[1])

    locations = myparser.parse_locations(sys.argv[2])

    #global_edit_alignment(tweets, locations)
    print(timeit.timeit(lambda: token_set_alignment(tweets, locations), number=1))
    #token_set_alignment(tweets, locations)


if __name__ == '__main__':
    main()

