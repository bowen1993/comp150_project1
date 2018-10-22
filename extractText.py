from lxml import etree
from bs4 import BeautifulSoup
from collections import defaultdict
import json
import os
import csv
import nltk

# get all dialogs for xml file. extract both role id and text
def get_dialogs(filename):
    texts = defaultdict(list)
    with open(filename, 'r') as f:
        tree = etree.fromstring(bytes(bytearray(str(BeautifulSoup(f.read(), "xml")), encoding='utf-8')))
        for sp in tree.iter('sp'):
            if 'who' not in sp.attrib:
                continue
            speaker = sp.attrib['who']
            p = sp.find('p')
            if speaker is not None and p is not None:
                stage = p.find('stage')
                if stage is not None:
                    p.remove(stage)
                text_list = []
                for text in p.itertext():
                    text = text.strip(' \t\n')
                    text = text.replace('\r\n', " ")
                    print(text)
                    text_list.append(text)
                texts[speaker].append(' '.join(text_list))
                
    return texts

#ignore this method
def get_role_id_map(filename):
    roleIdMap = {}
    with open(filename, 'r') as f:
        tree = etree.fromstring(bytes(bytearray(str(BeautifulSoup(f.read(), "xml")), encoding='utf-8')))
        for sp in tree.iter('sp'):
            speaker = sp.find('speaker')
            if 'who' not in sp.attrib or speaker is None:
                continue
            roleIdMap[sp.attrib['who']] = speaker.text
    return roleIdMap

#ignore this method
def generateRoleIdMapFile():
    res_file = open('name_id.csv', 'w')
    csv_writer = csv.writer(res_file)
    with open('data_list', 'r') as data_file:
        for line in data_file.readlines():
            line = line.strip()
            roleIdMap = get_role_id_map(line)
            for role in roleIdMap:
                csv_writer.writerow([role, roleIdMap[role], line])
    res_file.close()
            

# iter through all assigned files
def main():
    with open('data_list', 'r') as data_file:
        for line in data_file.readlines():
            line = line.strip()
            res = get_dialogs(line)
            path = 'data/%s' % os.path.split(line)[0]
            print(path)
            if not os.path.exists(path):
                os.mkdir(path)
            filename = os.path.splitext(line)[0]
            print(filename)
            f = open('data/%s.json' % filename, 'w')
            json.dump(res, f)
    generateRoleIdMapFile()

main()