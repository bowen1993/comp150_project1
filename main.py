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
            if len(row) > 2:
                tagMap[row[0]] = 0 if row[-1] == 'MALE' else 1
    return tagMap

def loadTrainData(dirname, label):
    trains = []
    labels = []
    for d in os.listdir(dirname):
        if d.endswith('txt'):
            with open(os.path.join(dirname, d)) as f:
                trains.append(f.read())
                labels.append(label)
    
    return trains, labels

def main():
    #load data
    print("load data in")
    tagMap = loadTagMap('./Comp150 - filtered_name_id.csv')
    male_trains, male_labels = loadTrainData('data/train/male', 0)
    female_trains, female_labels = loadTrainData('data/train/female', 1)

    male_val, male_val_labels = loadTrainData('data/test/male', 0)
    female_val, female_val_labels = loadTrainData('data/test/female', 1)
    
    train_data = male_trains + female_trains
    train_label = male_labels + female_labels
    val_train = male_val + female_val
    val_label = male_val_labels + female_val_labels
    print(len(train_data), len(train_label ))
    print('train & evaluate')
    acc, loss = train_ngram_model(((train_data, train_label), (val_train, val_label)))


main()