
# coding: utf-8

# In[110]:


import nltk
import csv
reader = csv.reader(open('filtered_name_id.csv', 'r'))
data = {}
for sp,n,p,g in reader:
    data[sp] = {}
    data[sp]['name'] = n
    data[sp]['path'] = 'data/' + p[:-4] + '/' + sp + '.txt'
    data[sp]['gender'] = g


# In[111]:


traits = {}
traits['m'] = {}
traits['f'] = {}
male = traits['m']
female = traits['f']
# TODO clean text for stop words and punctuation
male['text'] = ""
female['text'] = ""
for sp in data.keys():
    f = open(d[sp]['path'])
    t = f.read()
    f.close()
    if data[sp]['gender'] == 'MALE':
        male['text'] += t
    elif data[sp]['gender'] == 'FEMALE':
        female['text'] += t


# In[112]:


male['words'] = mText.split()
female['words'] = fText.split()
male['vocab'] = sorted(set(mWords))
female['vocab'] = sorted(set(fWords))
male['lex_div'] = len(male['vocab'])/len(male['words'])
female['lex_div'] = len(female['vocab'])/len(female['words'])


# In[113]:


print("Text Length\nMale  ", len(male['text']), "\nFemale ", len(female['text']))
print("\nVocab Size\nMale  ", len(male['vocab']), "\nFemale", len(female['vocab']))
print("\nLexical Diversity\nMale  ", male['lex_div'], "\nFemale", female['lex_div'])

