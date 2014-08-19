#!/usr/bin/python3
""" Program extracts the location names from a file with 
    the same format as US.txt """

import sys
import random
import re

def parse_us_locations_file(filename, num_lines=None):
    """ Reads in the raw locations names from filename """
    # Read in file, ignore windows vs unix line endings
    f = open(filename, 'rU')
    lines = f.readlines()
    
    if num_lines:
        lines = random.sample(lines, num_lines)

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

    if flag == '-C':
        # remove the substring '(historical)' from location if it is present
        locations = [re.sub(r'\(historical\)', '', location) 
                     for location in locations]

    if flag == '-B' or flag == '-C':
        # remove locations that contain characters which are non-alphabetic
        locations = [location + '\n' for location in locations
                     if re.search(r'^[a-z ]+$', location)]

        # remove the duplicate locations name
        locations = list(set(locations))

        # sort the locations lexiographically
        locations = sorted(locations)

    return locations



def write_locations_to_file(dest_filename, locations):
    """ Writes the locations specified to a .csv """
    f = open(dest_filename, 'w')
    f.writelines(locations)


def main():
    """ Entry point of the program """
    if len(sys.argv) >= 4 and re.search(r'-[ABC]', sys.argv[1]):
        flag = sys.argv[1]
        src_filename = sys.argv[2]
        dest_filename = sys.argv[3] 
    else:
        print('usage: extractor.py -FLAG source_file destination_file [num_lines]')
        sys.exit()

    if len(sys.argv) == 5:
        num_lines = int(sys.argv[4])
        locations = parse_us_locations_file(src_filename, num_lines=num_lines)
    else:
        locations = parse_us_locations_file(src_filename)

    locations = modify_us_locations(locations, flag)
    write_locations_to_file(dest_filename, locations)


if __name__ == '__main__':
    main()

