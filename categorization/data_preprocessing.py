import pandas as pd
from tqdm import tqdm
from nltk.corpus import stopwords
from pymystem3 import Mystem
import re
import math
import numpy as np
from gensim.models import Word2Vec

def clean_data(data_rows):
    stop_words = stopwords.words('russian')
    stem = Mystem()
    clean_rows = []
    for processing_row in tqdm(data_rows):
        try:
            processing_row = processing_row.strip()
            processing_row = re.sub("^\s+|\n|\r|\s+$", '', re.sub('<(.*?)>', '', processing_row)).lower()
            split_row = []
            for word in stem.lemmatize(processing_row):
                if re.findall('([A-Za-z]{1,})|([А-Яа-я]{1,})', word):
                    if word not in stop_words:
                        split_row.append(word)
            
            processing_row = ' '.join(split_row)
            clean_rows.append(processing_row)
        except:
            clean_rows.append(np.nan)
    return clean_rows


def apply_n_grams(text, word2vec_model):
    text = text.split()
    tokens = []
    
    i = 1
    
    while i <= len(text):
        if i == len(text):
            tokens.append(text[i-1])
            break
        prev_word = text[i-1]
        cur_word = text[i]
        bigram = prev_word + '_' + cur_word
        if bigram in word2vec_model.wv.key_to_index.keys():
            tokens.append(bigram)
            i += 2
        else:
            tokens.append(prev_word)
            i += 1
    return tokens

def vectorize_text(text, word2vec_model):
    
    word_vectors = []
    for word in text:
        try:
            word_vectors.append(word2vec_model.wv[word])
        except:
            pass
        
    try:
        text_vector = [0]*100
        for v_i in word_vectors:
            for j in range(100):
                text_vector[j] += v_i[j]

        rms = 0 
        for i in range(100):
            rms = rms + text_vector[i] * text_vector[i] 
        rms = math.sqrt(rms / 100) 

        for i in range(100):
            text_vector[i] = text_vector[i] / rms 

        return text_vector
    except:
        pass

