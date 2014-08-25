""" Module is used to parse the modified tweet and location files """

import re
import random

def parse_tweets(filename, num_tweets=None):
    """ Used to extract a list of tweets from the modified tweet files
        or the ideal tweet-location pairs """
    f = open(filename, 'rU')
    lines = f.readlines()
    f.close()

    if num_tweets and num_tweets > 0:
        lines = random.sample(lines, num_tweets)

    # remove the new line character from the end of the tweet text
    lines = [re.sub(r'\n', '', line) for line in lines]    
    lines = [line.split('\t') for line in lines]
    return lines

def parse_locations(filename):
    """ Used to extract the a list of locations from the modified locations
        file. """
    f = open(filename, 'rU')
    lines = f.readlines()
    f.close()

    # remove the new line character from the end of the location
    lines = [re.sub(r'\n', '', line) for line in lines] 

    return lines
