
editdistance.py:
    
    Prints the associated location (query) matches with the tweets using the algorithms
    explored in Project 1 (see report).

    usage: editdistance.py tweets-file locations-file [num-tweets]

        tweets-file: is the preprocessed tweets-file
        locations-file: is the preprocessed locations-file
        num-tweets: optional parameter specifying the number of tweets (a random sample) 
            to compare against all of the location queries. This parameter should be used
            to avoid extremely long processing times!!

    dependencies:
        my-smith-waterman
        my-subdist
        myparser.py
        Levenshtein https://github.com/ztane/python-Levenshtein/

    example output:
        Twitter User 8216952:
            Tweet ID: 5384915507
             Tweet Text: krislan webstock second love hear speak


        Whole String Needlemen-Wunsch Algorithm

        Twitter User 8216952:
            Tweet ID: 5384915507
             Matches: []

        1.42146897316

        Tokenised Needlemen-Wunsch Algorithm

        Twitter User 8216952:
            Tweet ID: 5384915507
             Matches: [('love', 1.0), ('speak', 1.0)]

        4.86723184586

        Smith-Waterman Algorithm

        Twitter User 8216952:
            Tweet ID: 5384915507
             Matches: [('cond', 1.0), ('ear', 1.0), ('isl', 1.0), ('isla', 1.0), ('kri', 1.0), ('love', 1.0), ('peak', 1.0), ('seco', 1.0), ('speak', 1.0), ('stock', 1.0)]

        6.70874595642

        N-W and S-W Algorithm

        Twitter User 8216952:
            Tweet ID: 5384915507
             Matches: [('kri', 1.0), ('love', 1.0), ('seco', 1.0), ('second cove', 0.9090909090909091), ('speak', 1.0)]

        3.04115605354

tweets-extractor.py:
    Used to preprocess the tweets.

    usage: tweets-extractor.py FLAG src-file destination-file 

    FLAG: -A or -B
        -A: convert tweets to lower case and remove all non-alphabetic characters excluding space
        -B: perform ALL preprocessing steps outlined in the report

location-extractor.py:
    Used to preprocess the locations.

    usage: tweets-extractor.py FLAG src-file destination-file  

    FLAG: -A or -B
        -A: convert locations to lower case
        -B: perform ALL preprocessing steps outlined in the report
     