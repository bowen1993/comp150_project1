from validation import *
from learn_curve import learn_curve
import bayes
import json
import os
import nltk
import csv
import numpy as np
from random import shuffle
import ss
import draw

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
    print('load data')
    tagMap = loadTagMap('./Comp150 - filtered_name_id.csv')
    male_trains, male_labels = loadTrainData('data/train/male', 0)
    female_trains, female_labels = loadTrainData('data/train/female', 1)
    train_data = male_trains + female_trains
    train_label = male_labels + female_labels
    trains = []
    for i in range(len(train_data)):
        trains.append((train_data[i], train_label[i]))
    trainer = bayes.BayesClassifer(1)
    average_performance, performances = stratified_cross_validation(20, trainer, trains)
    print("ave performance: %lf" % average_performance)
    print(performances)

def makePlot():
    tagMap = loadTagMap('./Comp150 - filtered_name_id.csv')
    male_trains, male_labels = loadTrainData('data/train/male', 0)
    female_trains, female_labels = loadTrainData('data/train/female', 1)
    train_data = male_trains + female_trains
    train_label = male_labels + female_labels
    trains = []
    for i in range(len(train_data)):
        trains.append((train_data[i], train_label[i]))
    trainer = bayes.BayesClassifer(1)
    performances = learn_curve(10, trainer, trains)
    lines = {}
    lines['shakespeare'] = {
        'x':[],'y':[],'errorBar':[],
        'color':'blue'}
    for i in range(10):
        lines['shakespeare']['x'].append((float(i) / 10))
        numbers = []
        for j in range(10):
            numbers.append(performances[j][i])
        average = sum(numbers) / float(len(numbers))
        std = ss.pstdev(numbers)
        lines['shakespeare']['y'].append(average)
        lines['shakespeare']['errorBar'].append(std)
    json.d ump(lines, open('size_cache.json', 'w')) # cache result (to adjust plot)
    draw.drawPlot(lines,'size')


makePlot()