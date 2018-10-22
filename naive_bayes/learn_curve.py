import bayes
import parser
from validation import *
import validation
import ss
import math
import json
import draw

basename = 'sentiment_labelled_sentences/'
data_filenames = ['amazon_cells_labelled.txt', 'imdb_labelled.txt', 'yelp_labelled.txt']

def shrink(train_set, ratio):
    '''shrink train data size by a ratio'''
    shrink_size = int(math.ceil(len(train_set) * (ratio/10.0)))
    return train_set[:shrink_size]

def learn_curve(fold_number, classifier, train_data):
    '''run stratified cross validation for different size'''
    train_data,partition_index = prepare_train_data(train_data)
    portion1 = make_portion(fold_number, 0, partition_index)
    portion2 = make_portion(fold_number, partition_index, len(train_data))
    performances = []
    for i in range(fold_number):
        s1,e1 = portion1[i]
        s2,e2 = portion2[i]
        train_set0 = train_data[:s1] + train_data[e1:partition_index]
        train_set1 =  train_data[partition_index:s2] + train_data[e2:]
        test_set = train_data[s1:e1] + train_data[s2:e2]
        ratio_performances = []
        for i in range(1,11):
            random.shuffle(train_set0)
            random.shuffle(train_set1)
            shrinked_train_set0 = shrink(train_set0,i)
            shrinked_train_set1 = shrink(train_set1,i)
            shrinked_train_set = shrinked_train_set0 + shrinked_train_set1
            random.shuffle(shrinked_train_set)
            classifier.train(shrinked_train_set)
            performance = check_classifier_performance(classifier, test_set)
            ratio_performances.append(performance)
        performances.append(ratio_performances)
    return performances

# def main():
#     basename = 'sentiment_labelled_sentences/'
#     lines = {}
#     colors = ['yellow','blue','red','green','black','orange']
#     for filename in ['amazon_cells_labelled.txt', 'imdb_labelled.txt', 'yelp_labelled.txt']:
#         print 'dataset: %s' % filename
#         train_data = parser.load_train_data('%s%s' % (basename, filename))
#         #generate lines
#         for m in range(2):
#             print 'smooth %d' % m
#             line_name = '%s_m=%d' % (filename[:filename.index('_')], m)
#             trainer = bayes.BayesClassifer(m)
#             performances = learn_curve(10, trainer, train_data)
#             del trainer
#             lines[line_name] = {
#                 'x':[],'y':[],'errorBar':[],
#                 'color':colors.pop()}
#             for i in range(10):
#                 lines[line_name]['x'].append((float(i) / 10))
#                 numbers = []
#                 for j in range(10):
#                     numbers.append(performances[j][i])
#                 average = sum(numbers) / float(len(numbers))
#                 std = ss.pstdev(numbers)
#                 lines[line_name]['y'].append(average)
#                 lines[line_name]['errorBar'].append(std)
#     json.dump(lines, open('size_cache.json', 'w')) # cache result (to adjust plot)
#     draw.drawPlot(lines,'size')

# main()
# lines = json.load(open('size_cache.json', 'r'))
# draw.drawPlot(lines,'size',errBar=True)