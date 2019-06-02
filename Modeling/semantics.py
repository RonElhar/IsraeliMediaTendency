import multiprocessing
from time import time
import numpy as np

from gensim import utils
from gensim.models import Word2Vec
import os


# Pre processing of articles, in order to make them fit Word2Vec model input
def parse_articles(path):
    i = 0
    sentences = []
    files_list = os.listdir(path)
    for file in files_list:
        with open(path + '\\' + file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                terms = utils.simple_preprocess(line)
                sentences.append(terms)
    return sentences


# Train Word2Vec model, save it to bin file
def train(model_name, sentences):
    model = Word2Vec(size=200, window=5, min_count=2, workers=16)
    t = time()
    model.build_vocab(sentences)
    print('Time to build vocab: {} mins'.format(round((time() - t) / 60, 2)))
    model.train(sentences, total_examples=len(sentences), epochs=50)
    model.save(model_name + '.bin')


# test prediction of model for one word
def test(model_name, target_word):
    new_model = Word2Vec.load(model_name + '.bin')
    similar = new_model.wv.most_similar(positive=target_word)
    print(similar)


# sents = parse_articles('C:\\Users\\ronel\\Desktop\\IsraeliMediaTendency\\ynet')
# train('ynetAllTime', sents)
test('ynetAllTime240', 'מירי')
