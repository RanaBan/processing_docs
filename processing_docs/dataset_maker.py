import os
import pandas as pd

import re
def clean(text):
    # new line characters
    text = re.sub('\\n',' ',str(text))
    
    # apostrophes
    text = re.sub("'s", '', text)

    # multiple white-space
    text = re.sub('  \+', ' ', text)
    
    # references to outside text
    text = re.sub("[\(\[].*?[\)\]]", "", text)
    
    # html/xml tags
    text = re.sub('<[^<]+>', "",text)

    # url
    text = re.sub(r'^https?:\/\/.*[\r\n]*', ' ', text, flags=re.MULTILINE)

    # Only alpha-numeric allowed
    text = re.sub('[^0-9a-zA-Z\.]+', ' ', text)
    
    return text

dirs = ['business', 'entertainment', 'politics', 'sport', 'tech']
#====================== DOCUMENT ======================#
texts = []
for adir in tqdm(dirs):
    directory = os.fsencode('News Articles/'+adir)
    filenames = os.listdir(directory)
    filenames = [str(s).split('\'')[1] for s in filenames]
    filenames = sorted(filenames)
    print(directory, ':', len(filenames))
    
    for filenm in filenames:
        thefile = 'News Articles/'+adir+'/'+filenm
#         print(thefile)
#     print('=================')
        with open(thefile, 'rb') as fp:
            texts.append(fp.readlines())
#====================== SUMMARY ======================#            
summaries = []
for adir in dirs:
    directory = os.fsencode('Summaries/'+str(adir))
    filenames = os.listdir(directory)
    filenames = [str(s).split('\'')[1] for s in filenames]
    filenames = sorted(filenames)
    print(directory, ':', len(filenames))
    
    for filenm in filenames:    
        thefile = 'Summaries/'+adir+'/'+filenm
#         print(thefile)
#     print('=================')
        with open(thefile, 'rb') as fp:
            summaries.append(fp.readlines())
#============================================#
assert len(text) == len(summaries)
#pd.DataFrame({'texts': text, 'summaries': summary}).to_pickle('texts_summaries.pkl')
def tokenize(text):
    text = clean(text)
    text = " ".join([tok.lemma_.strip() for tok in nlp(text)]) ## LEMMATIZED
    return [tok.text for tok in nlp.tokenizer(text)]
def treat_frac(s):
    if '.' in str(s.group(0)):
        s = re.sub('\.', '_', str(s.group(0)))
    else:
        s = re.sub(',', '', str(s.group(0)))
    return s

#=============== MAKE EACH DOCUMENT AND ITS SUMMARY A LIST OF SENTENCES ===============#
#====================== DOCUMENT ======================#
texts_sent_lists = []
# try:
text_sent_count = []
for text in tqdm(texts):
    temp = []
    for t in text:
        temp.append(t.decode('ISO-8859-1'))
    text = '. '.join(temp)
    text = re.sub("'s", '', text)
    text = re.sub("% ", 'percent ', text)
    text = re.sub('[0-9]+,[0-9]+', treat_frac, text)
    text = re.sub('[^0-9a-zA-Z\.]+', ' ', text)
    text = re.sub('[0-9]+\.[0-9]+', treat_frac, text)
#     temp = [clean(sent.decode('ISO-8859-1')).strip() for sent in text if clean(sent.decode('ISO-8859-1')).strip()]
    temp = []
    for sent in nlp(text).sents:#sent_tokenize(text):
        sent = clean(sent.text).strip()
        if sent and len(sent.split())>2:
            temp.append(sent)
#     temp = [clean(sent).strip() for sent in sent_tokenize(text) if clean(sent).strip()] #nlp(text).sents
    if temp:
        text_sent_count.append(len(temp))
        texts_sent_lists.append(temp) #unicode_escape
#====================== SUMMARY ======================#
summr_sent_lists = []
summr_sent_count = []
for summary in tqdm(summaries):
    temp = []
    summary = summary[0].decode('ISO-8859-1')
    summary = re.sub("'s", '', summary)
    summary = re.sub('[^0-9a-zA-Z\.]+', ' ', summary)
    summary = re.sub('[0-9]+\.[0-9]+', treat_frac, summary)
    summary = re.sub('[0-9]+,[0-9]+', treat_frac, summary)
    summary = re.sub('\.', '. ', summary)
    for sent in nlp(summary).sents:
        sent = clean(sent.text).strip()
        if len(sent.split())>2:
            temp.append(sent)
#     temp = [clean(sent).strip() for sent in nlp(text[0].decode("utf-8")).sents]
    if temp:                             #sent_tokenize(text[0].decode("utf-8"))
        summr_sent_count.append(len(temp))
        summr_sent_lists.append(temp)
