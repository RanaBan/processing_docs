import os
import pandas as pd
from tqdm import tqdm
import numpy as np
import re
import nltk
nltk.download('punkt')
from nltk import word_tokenize, sent_tokenize
import spacy
nlp = spacy.load("en_core_web_sm")
#   =================================================

path = './BBC News Summary/'
dirs = ['business', 'entertainment', 'politics', 'sport', 'tech']
texts, summaries = [], []
for adir in dirs:
    text_dir = os.fsencode(path+'News Articles/'+adir)
    filenames = os.listdir(text_dir)
    filenames = [str(s).split('\'')[1] for s in filenames]
    filenames = sorted(filenames)
    print(text_dir, ':', len(filenames))

    for filenm in filenames:
        thefile = path+'News Articles/'+adir+'/'+filenm

        with open(thefile, 'rb') as fp:
            temp = fp.readlines()
            texts.append(''.join([t.decode('ISO-8859-1') for t in temp]))
#   =================================================
    summ_dir = os.fsencode(path+'Summaries/'+adir)
    filenames = os.listdir(summ_dir)
    filenames = [str(s).split('\'')[1] for s in filenames]
    filenames = sorted(filenames)
    print(summ_dir, ':', len(filenames))

    for filenm in filenames:
        thefile = path+'Summaries/'+adir+'/'+filenm
        with open(thefile, 'rb') as fp:
            temp = fp.readlines()
            summaries.append(''.join([t.decode('ISO-8859-1') for t in temp]))
#   =================================================
def treat_num(s):
    if '.' in str(s.group(0)):
        return re.sub('\.', '_', str(s.group(0)))
    else:
        return re.sub(',', '', str(s.group(0)))

document_wise_sentences, summary_sentences, labels = [], [], []
for text, summ in tqdm(zip(texts, summaries)):
    text = re.sub('\n+', '. ', text)
    text = re.sub('\.\.', '.', text)
    text = re.sub(r'[^0-9a-zA-Z\.]+', ' ', text)
    text = re.sub(r'[0-9]+\.[0-9]+', treat_num, text)
    temp_sentences = [re.sub('\.', '', s).strip() for s in sent_tokenize(text)]
    temp_sentences = [s for s in temp_sentences if s]

    document_wise_sentences.append(temp_sentences)

    summ = re.sub(r'[^0-9a-zA-Z\.]+', ' ', summ)
    summ = re.sub(r'[0-9]+\.[0-9]+', treat_num, summ)
    summ = re.sub(r'\.', '. ', summ)

    temp_summ_sentences = [re.sub('\.', '', s).strip() for s in sent_tokenize(summ)]
    summary_sentences.append(temp_summ_sentences)
    labeling = lambda s : 1 if s.strip() in temp_summ_sentences else 0
#     summary_sentences_in_text = [labeling(s) for s in sent_tokenize(summ)]
    labels.append([labeling(s) for s in temp_sentences])            
            
