#!/usr/bin/python
""" Program extracts the location names from a file with 
    the same format as US.txt """

import sys
import re
from nltk.corpus import stopwords
from nltk.stem.porter import *

def parse_us_locations_file(filename):
    """ Reads in the raw locations names from filename """
    # Read in file, ignore windows vs unix line endings
    f = open(filename, 'rU')
    lines = f.readlines()
    f.close()

    locations = []
    for line in lines:
        # match the US place ascii name (3rd column)
        match = re.search(r'\d+\t[\S ]+\t([\S ]+)\t', line)
        locations.append(match.group(1))

    return locations

def modify_us_locations(locations, flag):
    """ Modifies original location names according to various heuristics """
    
    # make all the locations lower-case strings
    locations = [location.lower() for location in locations]

    if flag == '-B':
        # remove the non-alphabetic characters from locations (excluding space)
        locations = [re.sub(r'[^a-z ]', '', location) 
                     for location in locations]

        # stem words, then remove words of 2 characters or less, 
        # common words and additional white space
        stop = stopwords.words('english')
        stemmer = PorterStemmer()
        mlocations = []
        for location in locations:
            # stem the location words
            location_words = [stemmer.stem(word) for word in location.split()]

            # remove small words
            location_words = [word for word in location_words if
                              len(word) > 2]

            # remove common english words
            location_words = [word for word in location_words if 
                              word not in stop]

            # only append the location if it consists of one or more words
            if location_words:
                mlocations.append(' '.join(location_words))
        locations = mlocations

        # remove the duplicate locations name
        locations = list(set(locations))

        # sort the locations lexiographically
        locations = sorted(locations)

        # create a list of words
        locations_words = [location.split(' ') for location in locations]
        
        # remove locations which share the first 2 words or more in common
        locations = []
        last = None
        for location_words in locations_words:
            if (not last or len(location_words) == 1 or len(last) == 1 
                or last[0:2] != location_words[0:2]):
                locations.append(location_words)
                last = location_words
        
        # join the location lists into a single string again
        locations = [' '.join(location) for location in locations]
    
    # add a newline at the end of each location
    locations = [location + '\n' for location in locations]

    return locations



def write_locations_to_file(dest_filename, locations):
    """ Writes the locations specified to a .csv """
    f = open(dest_filename, 'w')
    f.writelines(locations)
    f.close()


def main():
    """ Entry point of the program """
    if len(sys.argv) == 4 and re.search(r'-[ABC]', sys.argv[1]):
        flag = sys.argv[1]
        src_filename = sys.argv[2]
        dest_filename = sys.argv[3] 
    else:
        print('usage: us-locations-extractor.py' 
              '-FLAG source_file destination_file')
        sys.exit()


    locations = parse_us_locations_file(src_filename)
    
    # modify locations list based on clever heuristics
    locations = modify_us_locations(locations, flag)
    
    write_locations_to_file(dest_filename, locations)


if __name__ == '__main__':
    main()

