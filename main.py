import json
import os
import nltk
from nltk.corpus import stopwords
from TFIDFEncode import ngram_vectorize
from classifier import train_ngram_model
import csv
import numpy as np
from random import shuffle

en_stopwords = set(stopwords.words('english'))

class DataReader(object):
    def __init__(self, dirName):
        self.dir = dirName
    
    def __iter__(self):
        for subdir, dirs, files in os.walk(self.dir):
            for filename in files:
                if filename.endswith('json'):
                    fullname = os.path.join(subdir, filename)
                    data_file = open(fullname, 'r')
                    data = json.load(data_file)
                    for role in data:
                        for line in data[role]:
                            yield [w for w in nltk.word_tokenize(line) if w not in en_stopwords and w.isalpha()], role


def loadTagMap(filename):
    tagMap = {}
    with open(filename, 'r') as tag_file:
        csv_reader = csv.reader(tag_file);
        for row in csv_reader:
            tagMap[row[0]] = row[1]
    return tagMap

def loadTrainData(tagMap, data):
    trains = []
    for item in data:
        if item[1] in tagMap:
            trains.append((' '.join(item[0]), int(tagMap[item[1]])))
    shuffle(trains)
    return map(list, zip(*trains))

def main():
    #load data
    print("load data in")
    tagMap = loadTagMap('../gender_tag.csv')
    data = DataReader('data')
    trains, labels = loadTrainData(tagMap, data)
    train_data = trains[:-100]
    val_data = trains[-100:]
    train_label = labels[:-100]
    val_label = labels[-100:]
    print('train & evaluate')
    acc, loss = train_ngram_model(((train_data, train_label), (val_data, val_label)))


main()