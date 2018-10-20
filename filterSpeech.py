import nltk
import json
import os
import csv
import collections

all_roles = collections.defaultdict(list)

for subdir, dirs, files in os.walk('data'):
    for filename in files:
        if filename.endswith('json'):
            fullname = os.path.join(subdir, filename)
            data_file = open(fullname, 'r')
            data = json.load(data_file)
            filteredData = dict()
            for role in data:
                filteredData[role] = filter(lambda x : len(nltk.word_tokenize(x)) < 10, data[role])
                all_roles[role].extend(filteredData[role])
            data_file.close()
            newFile = open(fullname, 'w')
            json.dump(filteredData, newFile)

print(all_roles)

csv_file = open('gender_name_id.csv')
filtered_csv = open('filtered_name_id.csv', 'w')
csv_reader = csv.reader(csv_file)
csv_writer = csv.writer(filtered_csv)

for row in csv_reader:
    if row[0] in all_roles and len(all_roles[row[0]]) > 0:
        csv_writer.writerow(row)