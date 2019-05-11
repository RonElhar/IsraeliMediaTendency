from gensim import utils
from gensim.models import Word2Vec
import os


class Semantics:
    def __init__(self, file_path, model_name):
        self.path = file_path
        self.sentences = []
        self.model_name = model_name

    def parse_articles(self):
        i = 0
        files_list = os.listdir(self.path)
        for file in files_list:
            with open(self.path + '\\' + file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    terms = utils.simple_preprocess(line)
                    self.sentences.append(terms)

    def start(self):
        # train model
        model = Word2Vec(self.sentences, size=150, window=10, min_count=2, workers=10)
        model.train(self.sentences, total_examples=len(self.sentences), epochs=10)
        # save model
        model.save(self.model_name + '.bin')

    def test(self):
        # load model
        new_model = Word2Vec.load(self.model_name + '.bin')
        # access vector for one word
        w1 = 'נתניהו'
        similar = new_model.wv.most_similar(positive=w1)
        print(similar)


# terms = gensim.utils.simple_preprocess(text)
# tokens = gensim.utils.simple_tokenize(text)
# print terms
sem = Semantics("C:\\Users\\USER\\Desktop\\IsraeliMediaTendency\\ynet", "ynet")
sem.test()
# sem.read_corpus()
# sem.parse_articles()
# sem.start()