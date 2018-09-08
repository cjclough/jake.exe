import numpy as np
import random

def build_corpus(filename):
    file = open(filename, encoding='utf8').read()
    return file.split()

def make_pairs(corpus):
    for i in range(len(corpus)-1):
        yield (corpus[i], corpus[i+1])

def build_dict(corpus):
    pairs = make_pairs(corpus)
    word_dict = {}
    for word_1, word_2 in pairs:
        if word_1 in word_dict.keys():
            word_dict[word_1].append(word_2)
        else:
            word_dict[word_1] = [word_2]

    return word_dict    

def build_sentence(matrix, corpus, n_words):
    chain = [np.random.choice(corpus)]

    for x in range(n_words):
        chain.append(np.random.choice(matrix[chain[-1]]))

    sentence = " ". join(chain)
    sentence = sentence[0:len(sentence)]

    if random.randint(1,100) >= 70:
        sentence += "?"
    else:
        sentence += "."   

    return sentence

def do_markov(filename):
    corpus = build_corpus(filename)
    matrix = build_dict(corpus)
    return build_sentence(matrix, corpus, random.randint(4,8))