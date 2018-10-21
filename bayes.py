'''train and predict with naive bayes'''

import numpy
import re

class BayesClassifer(object):
    '''train with naive bayes'''
    def __init__(self, smooth=0):
        '''constructor'''
        self.smooth = smooth
        self.p0vec, self.p1vec = None, None #vector of pw|0
        self.p1 = 0.0
        self.vocabulary = []
        self.wordRe = re.compile('[\w\']*')

    def _doc2Vec(self, doc):
        '''trans a doc to a postion vec'''
        resVec = [0] * len(self.vocabulary)
        for word in doc:
            if word in self.vocabulary:
                resVec[self.vocabulary.index(word)] = 1
        return resVec
    
    def _buildVocabulary(self, train_data):
        '''build trainer vocabulary and remove stop words'''
        self.vocabulary = []
        vocabSet = set([])
        for doc in train_data:
            vocabSet = vocabSet | set(doc[0])
        self.vocabulary = list(vocabSet)

    def _logify(self):
        '''log with probabilities'''
        for x in numpy.nditer(self.p1vec, op_flags=['readwrite']):
            if x != 0:
                x[...] = numpy.log(x)
        for x in numpy.nditer(self.p0vec, op_flags=['readwrite']):
            if x != 0:
                x[...] = numpy.log(x)
        
    
    def train(self, train_data):
        '''train with naive bayes'''
        self._buildVocabulary(train_data)
        numOfTrains = len(train_data)
        numOfWords = len(self.vocabulary)
        #how many time a word appears in a class
        wordPos0, wordPos1 = numpy.zeros(numOfWords), numpy.zeros(numOfWords)
        totalWord0, totalWord1 = 0.0, 0.0
        numOf1 = 0
        for doc, label in train_data:
            docVec = self._doc2Vec(doc)
            if label == 0:
                wordPos0 += docVec
                totalWord0 += sum(docVec)
            if label == 1:
                numOf1 += 1
                wordPos1 += docVec
                totalWord1 += sum(docVec)
        self.p1vec = (wordPos1 + self.smooth) / (totalWord1 + self.smooth * numOfWords)
        self.p0vec = (wordPos0 + self.smooth) / (totalWord0 + self.smooth* numOfWords)
        self._logify()
        self.p1 = numOf1 / float(numOfTrains)
    
    def predict(self, doc):
        '''predict label of a given doc'''
        docVec = numpy.array(self._doc2Vec(doc))
        prob1 = sum(docVec * self.p1vec) + numpy.log(self.p1)
        prob0 = sum(docVec * self.p0vec) + numpy.log(1-self.p1)
        if prob1 > prob0:
            return 1
        else:
            return 0
