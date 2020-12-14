import pandas as pd
import numpy as np
import string
import re
import nltk
from nltk.tokenize import word_tokenize


def main():
    df = pd.read_csv('dados_pdf_falencias.csv')
    stopwords = nltk.corpus.stopwords.words('portuguese')
    text = df['string'].str.cat(sep=' ').lower()
    text = text.replace('\n', ' ')
    text = text.replace('\x0c', ' ')
    text_tokens = word_tokenize(text)
    tokens_without_sw = [
        word for word in text_tokens if not word in stopwords and not word in string.punctuation]
        
    bigrams = nltk.bigrams(tokens_without_sw)

    freqdist = nltk.FreqDist(bigrams)

    df_bgms = pd.DataFrame(data=freqdist)
    df_bgms = df_bgms.rename(columns={0: 'bigrams', 1: 'freq'})
    df_bgms = df_bgms.sort_values(by=['freq'], ascending=False)
    df_bgms = df_bgms[df_bgms['freq'] > 4]
    df_bgms.to_csv('bigrams.csv', index=False)

if __name__ == '__main__':
    main()
