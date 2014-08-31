#!/usr/bin/python
""" Uses the fuzzywuzzy module to do global edit distance matching
    and local edit distance matching for strings """

import sys
import myparser
import timeit
import mysubdist
import mysmithwaterman
import Levenshtein

# def token_set_alignment(tweets, locations):
#     d = {}

#     for tweet in tweets:
#         matches = []
#         tweet_text = tweet[2]
#         for location in locations:
#             score = fuzz.token_set_ratio(location, tweet_text)
#             if score >= 90:
#                 matches.append((location, score))
        
#         if d.get(tweet[0]):
#             d[tweet[0]].append((tweet[1], matches))
#         else:
#             d[tweet[0]] = [(tweet[1], matches)]

#     print('\nToken Set Alignment\n')
#     print_matches_dictionary(d)



def nw_sw_combined(tweets, locations):
    """ Uses middle gorund between a N-W and S-W algorithm
        to search a tweet text for instances of a location name"""

    #TODO change this algorithm so it associates whitespace and 1st
    # char after with a cost of zero and preceding chars with a cost
    # of the length of substring of word

    d = {}

    for tweet in tweets:
        matches = []
        tweet_text = tweet[2]

        for location in locations:
            score = mysubdist.get_score(unicode(location), unicode(tweet_text))
            if score >= 0.90:
                matches.append((location, score))
        
        if d.get(tweet[0]):
            d[tweet[0]].append((tweet[1], matches))
        else:
            d[tweet[0]] = [(tweet[1], matches)]


    print('\nN-W and S-W Algorithm\n')
    print_matches_dictionary(d)

def smith_waterman(tweets, locations):
    """ Smith-Waterman (local) alignment between the tweet bodies
        and the location queries """
    d = {}

    for tweet in tweets:
        matches = []
        for location in locations:
            score = mysmithwaterman.get_score(unicode(location), unicode(tweet[2]))
            if score >= 0.90:
                matches.append((location, score))

        if d.get(tweet[0]):
            d[tweet[0]].append((tweet[1], matches))
        else:
            d[tweet[0]] = [(tweet[1], matches)]

    print('\nSmith-Waterman Algorithm\n')
    print_matches_dictionary(d)


def tokenised_needlemen_wunsch(tweets, locations):
    """ Tokenize the location and the tweets into words,
        and compare """ 
    d = {}

    for tweet in tweets:
        matches = []
        tweet_words = tweet[2].split(' ')
        
        for location in locations:
            num_location_words = len(location.split(' '))
            for i in range(0, len(tweet_words)):
                score = Levenshtein.ratio(location, 
                                   ' '.join(tweet_words[i:i+num_location_words]))
                if score >= 0.95:
                    matches.append((location, score))

        if d.get(tweet[0]):
            d[tweet[0]].append((tweet[1], matches))
        else:
            d[tweet[0]] = [(tweet[1], matches)]

    print('\nTokenised Needlemen-Wunsch Algorithm\n')
    print_matches_dictionary(d)

    # ideal_locations = []
    # for matches in d.values():
    #     for match_tuple in matches:
    #         for match in match_tuple[1]:
    #             ideal_locations.append(match[0]) 

    # return ideal_locations


def whole_string_needleman_wunsch(tweets, locations):
    """ The baseline Needlemen-Wunsch alogithm which calculates the
        Levenshtein score of the entire tweet body against a location name"""
    d = {}
    
    for tweet in tweets:
        matches = []
        for location in locations:
            score = Levenshtein.ratio(location, tweet[2]) 
            if score >= 0.60:
                matches.append((location, score))

        if d.get(tweet[0]):
            d[tweet[0]].append((tweet[1], matches))
        else:
            d[tweet[0]] = [(tweet[1], matches)]

    print('\nWhole String Needlemen-Wunsch Algorithm\n')
    print_matches_dictionary(d)

def print_matches_dictionary(d):
    """ Used to print the matched location names for the dictionary
        of tweets """
    for key in d.keys():
        print('Twitter User ' + key + ':')
        for tweet_match in d[key]:
            print('\tTweet ID: ' + str(tweet_match[0]))
            sys.stdout.write('\t Matches: ')
            print(tweet_match[1])
        print('')

def print_tweets_text(tweets):
    for tweet in tweets:
        print('Twitter User ' + tweet[0] + ':')

        print('\tTweet ID: ' + tweet[1])
        
        sys.stdout.write('\t Tweet Text: ')
        print(tweet[2])
        
        print('')        


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

    print_tweets_text(tweets)

    print(timeit.timeit(lambda: whole_string_needleman_wunsch(tweets, locations), 
                        number=1))
    
    print(timeit.timeit(lambda: tokenised_needlemen_wunsch(tweets, locations), 
                        number=1))
    
    print(timeit.timeit(lambda: smith_waterman(tweets, locations), number=1))

    print(timeit.timeit(lambda: nw_sw_combined(tweets, locations), number=1))

    #print(timeit.timeit(lambda: token_set_alignment(tweets, locations), 
    #                    number=1))


if __name__ == '__main__':
    main()

