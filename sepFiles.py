import json
import csv
import os
import nltk
import random

def loadTagNameMap(filename):
    tagNameMap = dict()
    with open(filename, 'r') as tagFile:
        csv_reader = csv.reader(tagFile)
        for row in csv_reader:
            if len(row) > 2:
                tagNameMap[row[0]] = row[-1].lower()
    return tagNameMap

def sepFiles(tagNameMap):
    data = dict()
    data['male'] = []
    data['female'] = []
    for subdir, dirs, files in os.walk('data'):
        for filename in files:
            if filename.endswith('json'):
                fullname = os.path.join(subdir, filename)
                with open(fullname, 'r') as jsonFile:
                    fileData = json.load(jsonFile)
                    for role in fileData:
                        if role in tagNameMap:
                            if len(fileData[role]) > 0:
                                data[tagNameMap[role]].extend(fileData[role])
    print("num of male speech: %d, female: %d, total: %d" % (len(data['male']), len(data['female']), len(data['male']) + len(data['female']) ))
    random.shuffle(data['male'])
    # data['male'] = data['male'][:len(data['female'])]
    dir_path = 'data/train'
    splitIndex = int(len(data['female']) * 0.8)
    #generate train data
    for gender in data:
        sub_dir_path = os.path.join(dir_path, gender)
        
        for index, item in enumerate(data[gender]):
            with open("%s.txt" % os.path.join(sub_dir_path, str(index)), 'w') as f:
                f.write(item)
    #generate test data
    # dir_path = 'data/test'
    # for gender in data:
    #     sub_dir_path = os.path.join(dir_path, gender)
        
    #     for index, item in enumerate(data[gender][splitIndex:]):
    #         with open("%s.txt" % os.path.join(sub_dir_path, str(index)), 'w') as f:
    #             f.write(item)
    
    
tagMap = loadTagNameMap('./Comp150 - filtered_name_id.csv')
sepFiles(tagMap)