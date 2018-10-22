import math
import random

#code for cross valitaion
def make_portion(portion_number,start, length):
    '''return interval index for each protion'''
    size_of_portion = int(math.ceil(float(length-start) / portion_number))
    res = [] # list of [start,end]
    for i in range(start, length, size_of_portion):
        res.append((i, i + size_of_portion))
    return res

def check_classifier_performance(classifier, test_data):
    '''check performance of classifier'''
    correct_count = 0
    for data in test_data:
        doc, label = data[0], data[1]
        correct_count += 1 if classifier.predict(doc) == label else 0
    return float(correct_count) / len(test_data)
        
def cross_validation(fold_number, classifier, train_data):
    '''do cross validation'''
    intervals = make_portion(fold_number,0, len(train_data))
    performances = []
    for start, end in intervals:
        classifier.train(train_data[:start] + train_data[end:])
        performances.append(check_classifier_performance(classifier, train_data[start:end]))
    average_performance = float(sum(performances)) / len(performances)
    return average_performance, performances

# code for stratified cross validation
def find_change_index(train_data):
    '''find where label changed (split of classed)'''
    for index in range(1, len(train_data)):
        if train_data[index][1] != train_data[index-1][1]:
            return index
    return len(train_data)

def prepare_train_data(train_data):
    '''sort docs based on label, and shuffle'''
    train_data = sorted(train_data, key=lambda x:x[1])
    mid_index = find_change_index(train_data)
    # TODO: check whether there are two labels or not
    tmp1 = train_data[:mid_index]
    random.shuffle(tmp1)
    train_data[:mid_index] = tmp1
    tmp2 = train_data[mid_index:]
    random.shuffle(tmp2)
    train_data[mid_index:] = tmp2
    return train_data, mid_index

def stratified_cross_validation(fold_number, classifier, train_data):
    '''do stratified cross validation'''
    train_data,partition_index = prepare_train_data(train_data)
    portion1 = make_portion(fold_number, 0, partition_index)
    portion2 = make_portion(fold_number, partition_index, len(train_data))
    performances = []
    for i in range(fold_number):
        s1,e1 = portion1[i]
        s2,e2 = portion2[i]
        train_set = train_data[:s1] + train_data[e1:s2] + train_data[e2:]
        test_set = train_data[s1:e1] + train_data[s2:e2]
        random.shuffle(train_set)
        classifier.train(train_set)
        performances.append(check_classifier_performance(classifier, test_set))
    average_performance = float(sum(performances)) / len(performances)
    return average_performance, performances