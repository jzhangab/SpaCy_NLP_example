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

nlp = spacy.load('en_core_web_sm')  # make sure to use larger model!

text = """procedures documentation contamination equipment requirements specifications compliance
        labeling packaging operations manufacturing components testing treatment analysis pests directions data"""
doc = nlp(text)

simlist = []

for t1 in doc:
    for t2 in doc:
        simlist.append([t1.text, t2.text, t1.similarity(t2)])
        
sim50 = []
for i in simlist:
    if i[2] > .5:
        sim50.append(i)
        
sim75 = []
for i in simlist:
    if i[2] > .75:
        sim75.append(i)
        
        
# ########### Testing ############################################
        
dff = pd.read_csv('FEATURES/AUDIT.csv')

features = ['external_count_audit', 'internal_count_audit',
                               'external_count_0_findings_site', 'internal_count_0_findings_site',
                               'external_count_findings', 'internal_count_findings',
                               'external_count_critical_findings_site', 'internal_count_critical_findings_site',
                               'external_count_major_findings_site', 'internal_count_major_findings_site',
                               'external_count_minor_findings_site', 'internal_count_minor_findings_site',
                               'external_count_repeat_findings_site', 'internal_count_repeat_findings_site']
#                               'WL_NLP_matches']

correlations = []
for f in features:
    c = dff[f].corr(dff['WL_NLP_matches'])
    correlations.append(c)
    
dfc = pd.DataFrame({'Features': features,
                    'Correlation': correlations})
    
dff['total_findings'] = dff['internal_count_findings'] + dff['external_count_findings']
dff['WL_NLP_normalized'] = dff['WL_NLP_matches']/dff['total_findings']

dff.to_csv('FEATURES/AUDIT_EXTRA.csv')
#dfc.to_csv('FEATURES/AUDIT_CORR.csv')

corr2 = []
for f in features:
    c = dff[f].corr(dff['WL_NLP_normalized'])
    corr2.append(c)
    
dfc2 = pd.DataFrame({'Features': features,
                    'Correlation': correlations,
                    'Correlation_normalized': corr2})

dfc2.to_csv('FEATURES/AUDIT_CORR.csv')
