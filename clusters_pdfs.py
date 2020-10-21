#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import csv
import sys
import re
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import dateparser
from dateparser.search import search_dates
import unidecode
from dateutil.parser import parse
from collections import Counter
import os
import string
import nltk
import spacy 
nlp = spacy.load('pt_core_news_md')
exclude = set(string.punctuation)
nltk.download('stopwords')
from nltk.corpus import stopwords
from string import punctuation
stopw = list(set(stopwords.words('portuguese') + list(punctuation)))
from top2vec import Top2Vec
import umap.plot
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'notebook')
from bokeh.plotting import show, save, output_notebook, output_file
from bokeh.resources import INLINE 
output_notebook(resources=INLINE)
import hdbscan
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from joblib import dump, load
from sklearn.cluster import dbscan
import umap
import umap.plot
import tempfile
import warnings
import scipy
from scipy.sparse import csr_matrix
import dbmap as dm
import os
import gensim
import logging
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import strip_tags
from nltk.tokenize import word_tokenize
warnings.filterwarnings("ignore")


# In[ ]:


#Funcoes de apoio

def sub_str(x): 

    lista=[]

    for x in x.split():

        #x_1   = re.sub("([\d]+) *th",'',x)
        x_2=re.sub(r'[^a-zA-Z0-9]','',x)
        x_new = re.sub("\d+",'',x_2)
        #x_new = re.sub(r'(\d+)\s*(?:hours?\b|h?\b)','',x_)   
        lista+=[x_new]

    alpha_only_string = " ".join(lista)

    return alpha_only_string

def clean_ents(t):
    doc = nlp(t)
    return " ".join([ent.text for ent in doc if not ent.ent_type_])

def lemma(text,allowed=['VERB']):
    texts_out = []
    lista=[]
    for sent in text:
        #doc = nlp(" ".join(sent))
        doc=nlp(sent)
    #for token in doc:
        #texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed])
        final = " ".join([token.lemma_ for token in doc if token.pos_ in allowed and token.lemma_ not in stopw]) #
        lista+=[final]
    #return " ".join([token.lemma_ for token in doc if token.pos_ in allowed])
    return lista


# In[ ]:


#Dados
df = pd.read_csv('dados_pdf_falencias.csv')
df = df[df['tipo_documento']=='Decisão']
#df=df.sample(10000)
df=df.dropna()
df=df.reset_index(drop=True)
print(df.shape)
df.head()


# In[ ]:


#First replacements
for x in ['-lo','-la','-los','-las','-se']:
    df['string']=df['string'].str.replace(x,'')

#Stopwords
stopw+=['fls.','oab','são','paulo','no','em','ndeg','foro','hmin','sno','spfalenciastjspgovbr','paulo','fls','no','dr',
        '-se','erika','epp','-la','-las','carro','chefe','rocha','teani','eit','valinhos','eis','pessoa','min','jose','praça']


# In[ ]:


#Replace emails and links
df['string']=df['string'].apply(lambda x:" ".join(x.split('\n')))
df['string']=df['string'].apply(lambda x:clean_ents(x))
df['string']=df['string'].str.lower()
df['string']=df['string'].apply(lambda x:re.sub(r'http\S+', '', x))
df['string']=df['string'].apply(lambda x:re.sub('([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})', '', x))
df['string_clean']=df['string'].apply(lambda x: " ".join([z for z in x.split() if z not in stopw]))
df['string_clean']=df['string_clean'].apply(lambda texto:sub_str(unidecode.unidecode(''.join(ch for ch in texto if ch not in exclude))))
df['string_clean']=df['string_clean'].apply(lambda x:" ".join(z for z in x.split() if len(z)>2))


# In[ ]:


#More stopwords
stopw+=['fls.','oab','são','paulo','no','em','ndeg','foro','hmin','sno','spfalenciastjspgovbr','paulo','fls','no','dr',
        'copia','digitalmente','site','email','ashmin','art','ltda','rua','cep','janeiro','fevereiro','marco','abril',
        'maio','junho','julho','agosto','setembro','outubro','novembro','dezembro','marcelo','barbosa','sacramone','sob',
        'sobre','nome','assim','dias','apos','endereco','ainda','manifestese','decisaomandado','abib']

#Replace stopwords after cleaning
df['string_clean']=df['string_clean'].apply(lambda x: " ".join([z for z in x.split() if z not in stopw]))


# In[ ]:


#Check most frequent words
Counter(" ".join(df["string_clean"]).split()).most_common(150)


# In[ ]:


#Transforming data for vectorization
data = df['string_clean'].tolist()

#Lemmatize data
dados=lemma(data,allowed=['VERB'])


# In[ ]:


#Prepare for doc2vec
tagged_data=[TaggedDocument(words=word_tokenize(_d.lower()), tags=[str(i)]) for i, _d in enumerate(dados)]

#Doc2vec
max_epochs = 40
vec_size = 300
alpha = 0.025

model = Doc2Vec(size=vec_size,
                alpha=alpha, 
                min_alpha=0.00025,
                min_count=70,
                dm =1)#skipgram ou cbow
  
model.build_vocab(tagged_data)

for epoch in range(max_epochs):
    print('iteration {0}'.format(epoch))
    model.train(tagged_data,
                total_examples=model.corpus_count,
                epochs=model.iter)
    # decrease the learning rate
    model.alpha -= 0.0002
    # fix the learning rate, no decay
    model.min_alpha = model.alpha

model.save("d2v.model")
print("Model Saved")


# In[ ]:


#Load saved model
model= Doc2Vec.load("d2v.model")

#Collect document vectors
d=model.docvecs.vectors_docs


# In[ ]:


#dbMap for clustering
d2 = csr_matrix(d)

# Initialize the diffusor object, fit d2 and transform:
res = dm.diffusion.Diffusor().fit(d2).transform(d2)

# Embed graph with a fast approximate UMAP layout:
emb = dm.umapper.UMAP(min_dist=0.1).fit_transform(res.to_numpy(dtype='float32'))

#Clusters
clusters = hdbscan.HDBSCAN(min_cluster_size=15,
                                  metric='euclidean',
                                  cluster_selection_method='eom').fit(emb)


# In[ ]:


# Embed graph with vanilla UMAP:
 emb = dm.map.UMAP().fit(transform(res.to_numpy(dtype='float32'))
 
 plt.scatter(emb[:, 0], emb[:, 1], c=clusters.labels_, cmap='Spectral', s=5)
 plt.gca().set_aspect('equal', 'datalim')
 plt.colorbar(boundaries=np.arange(11)-0.5).set_ticks(np.arange(10))
 plt.title('Documents Projection', fontsize=24)
 plt.show()


# In[ ]:




