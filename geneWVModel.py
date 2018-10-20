import gensim
from gensim.models import Word2Vec
import nltk
from nltk.corpus import stopwords
import os

en_stopwords = set(stopwords.words('english'))

class TextReader(object):
    def __init__(self, dirName):
        self.dir = dirName
    
    def __iter__(self):
        for subdir, dirs, files in os.walk('data'):
            for filename in files:
                if filename.endswith('txt'):
                    fullname = os.path.join(subdir, filename)
                    for line in open(fullname, 'r'):
                        yield [w for w in nltk.word_tokenize(line) if w not in en_stopwords]

def generateWVModel(sents, iter=10):
    model = Word2Vec(sents, iter=iter)
    model.save("word2vec.model")

def testAccuracy(model):
    accu = model.accuracy('questions-words.txt')
    corr = 0
    incorr = 0
    for sec in accu:
        corr += len(sec['correct'])
        incorr += len(sec['incorrect'])
    return corr, incorr

def main():
    sents = TextReader('data')
    generateWVModel(sents, 20)

main()