# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 12:33:23 2018

@author: zhangj
"""
import pandas as pd
import spacy
from collections import Counter
import nltk
nltk.download("stopwords")
from nltk.corpus import stopwords


# Read warning letter
def WL_read(filename = 'Test_Data_NLP/Warning_Letters.xlsx'):
    df = pd.read_excel(filename)
    return(df)

# Perform warning letter NLP
def WL_nlp(df):
    nlp = spacy.load('en_core_web_sm')
    
    df['Finding Description'] = df['Finding Description'].astype(str)
    fd_list = list(df['Finding Description'])
      
    chunks = []
    for i in range(0, len(fd_list)):
        print ('Processing WL row: '+str(i)+' of '+str(len(fd_list)))
        try:
            doc = nlp(fd_list[i])

            for chunk in doc.noun_chunks:
                chunks.append(chunk.text)
        except: pass

    return(chunks)

def chunk_frequency(chunks):
    counts = Counter(chunks)
    top = counts.most_common(100)
    s=set(stopwords.words('english'))
    
    # Filter by nltk stop words and length > 3
    top_filtered = []
    for c in top:
        if (c[0].lower() not in s) and (len(c[0]) > 3) and ('(' not in c[0]) and (')' not in c[0]) and ('CFR' not in c[0]):
            top_filtered.append(c)
            
    
    df_top_chunks = pd.DataFrame(top_filtered, columns=['chunk', 'frequency'])
    return(df_top_chunks)
    

df_WL = WL_read()

chunk_list = WL_nlp(df_WL)

df_chunks = chunk_frequency(chunk_list)

df_chunks.to_excel('Test_Data_NLP/topchunks.xlsx')