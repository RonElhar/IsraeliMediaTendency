from collections import OrderedDict

from gensim.models import Word2Vec
from gensim import utils
import numpy as np
from parties_dictionary import parties_vocab
from scipy import spatial


# Get party relations with other parties.
def get_relations(target_party):
    sims = {}
    for party in parties_vocab:
        if party == target_party:
            continue
        sims[party] = calculate_parties_similarity(target_party, party)
    return sims


# Tokenize words of parties_vocab[party]
def get_processed_words(party):
    words = []
    for phrase in parties_vocab[party]:
        phrase = utils.simple_preprocess(phrase)
        words.extend(phrase)
    return words


# Calculate similarity between two parties with word2vec vectors
def calculate_parties_similarity(party_1, party_2):
    party_1_words = get_processed_words(party_1)
    party_2_words = get_processed_words(party_2)
    sim_sum = 0
    sim_count = 0
    for first in party_1_words:
        for second in party_2_words:
            if first in model and second in model:
                sim_sum += model.wv.similarity(first, second)
                sim_count += 1
    avg_sim = sim_sum / sim_count
    return avg_sim


# Helper Method, create list with no duplicates
def ordered_set(in_list):
    out_list = []
    added = set()
    for val in in_list:
        if not val in added:
            out_list.append(val)
            added.add(val)
    return out_list


def get_sentence_similarity(sentence):
    global model
    similar = []
    sentence = utils.simple_preprocess(sentence)
    for word in sentence:
        if word in model:
            temp = model.wv.most_similar(word)
            similar.extend([t for t in temp if not word in t[0] and not t[0] in sentence])
    sorted(similar, key=lambda x: x[1], reverse=True)
    similar = ordered_set([sim[0] for sim in similar])
    return similar[:20]


# Load the model of site from certain period
def load_model(site, period):
    global model
    model = Word2Vec.load('models\\' + site + period + '.bin')


model = None
