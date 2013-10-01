#!/usr/bin/env python

import sys
import random 
import twitter

api = twitter.Api(consumer_key='iSEl0ZY0RLnIYc9aBVLQtQ', consumer_secret='PcrM2KGFT5Dcp6xETlKCektQVcy5qiYTcqGqLDX6DM', access_token_key='618745013-E1eSryRjEkqkk77cOVhgQJDZ886T3LOmsbGoctqb', access_token_secret='KIzFnnZES5UOQeHI59akTFyAhYIFo0dd6ksnWNtkUg')

def make_chains(corpus):
    """Takes an input text as a string and returns a dictionary of
    markov chains."""
    dict_markov = {}
    for line in corpus: 
        list_words = line.split()
        for i in range(len(list_words) - 2):
            dict_key = (list_words[i] + " " + list_words[i + 1])
            if dict_key in dict_markov.keys():
                dict_markov[dict_key].append(list_words[i + 2])
            else: 
                dict_markov[dict_key] = [list_words[i + 2]]
    return dict_markov

def make_text(chains):
    """Takes a dictionary of markov chains and returns random text
    based off an original text."""
    
    a_tweet = ""
    is_tweet = False

    while is_tweet == False: 
        a_test_tweet = a_tweet + " " + make_sentence(chains)
        if len(a_test_tweet) >= 140: 
            is_tweet = True
        else: 
            a_tweet = a_test_tweet

    return a_tweet

def make_sentence(words_dict):

    # start sentence 
    sentence_text = ""
    first_two = random.choice(words_dict.keys())
    while first_two[0].islower():
        first_two = random.choice(words_dict.keys())
    sentence_text += first_two + " " + words_dict[first_two][random.randint(0,len(words_dict[first_two])-1)]

    # add to sentence until it is a true sentence
    sentence = False  
    while sentence == False: 
        list_last_two = sentence_text.split()
        last_two = list_last_two[-2] + " " + list_last_two[-1]
        if last_two in words_dict.keys():
            sentence_text += " " + words_dict[last_two][random.randint(0,len(words_dict[last_two])-1)]
        else:
            sentence = True 
        if sentence_text[-1] in ".?!": 
            sentence = True

    return sentence_text

def main():
    input_text = open(sys.argv[1])

    chain_dict = make_chains(input_text)
    random_text = make_text(chain_dict)
    print random_text
    status = api.PostUpdate(random_text)
    print status.text

if __name__ == "__main__":
    main()