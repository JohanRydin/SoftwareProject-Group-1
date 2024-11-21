from nltk.tokenize import word_tokenize
import re
import gensim
import numpy as np

def tokenize(data):
    tokens = [[w.lower() for w in word_tokenize(doc)] for doc in data]
    return tokens

def cleaning(data):
    data = re.sub('http\S+\s*', '', data)  # remove URLs
    data = re.sub('RT|cc', '', data)  # remove RT and cc
    data = re.sub('#\S+', '', data)  # remove hashtags
    data = re.sub('@\S+', '', data)  # remove mentions
    data = re.sub(r'[!"\$%&\'()*+,-./:;<=>?\[\\\]^_`{|}~]', '', data)  # remove punctuations
    data = re.sub(r'[^\x00-\x7f]', r'', data)
    return data


def similarity(data, query, isTokens = False):
    #data = cleaning(data)
    if (isTokens):
        tokens = data
        query_doc = query
    else:
        tokens = tokenize(data)
        query_doc = tokenize(query)
    print(tokens)

    dictionary = gensim.corpora.Dictionary(tokens)
    #print(dictionary.token2id, '\n')
    corpus = [dictionary.doc2bow(doc) for doc in tokens]
    #print(corpus, '\n')

    tf_idf = gensim.models.TfidfModel(corpus)
    #for doc in tf_idf[corpus]:
    #    print([[dictionary[id], np.around(freq, decimals=2)] for id, freq in doc])

    # building the index
    sims = gensim.similarities.Similarity('workdir/',tf_idf[corpus], num_features=len(dictionary))


    #query_doc = tokenize(query)
    query_doc_bow = dictionary.doc2bow(query_doc[0])

    query_doc_tf_idf = tf_idf[query_doc_bow]
    # print(document_number, document_similarity)
    #print('Comparing Result:', sims[query_doc_tf_idf]) 
    print(sims[query_doc_tf_idf])
    sum_of_sims =(np.sum(sims[query_doc_tf_idf], dtype=np.float32))
    similarity = round(float(sum_of_sims / len(data)), 2)
    #print(f'Average similarity float: {float(sum_of_sims / len(data))}')
    #print(f'Average similarity percentage: {float(sum_of_sims / len(data)) * 100}')
    #print(f'Average similarity rounded percentage: {percentage_of_similarity}')

    return similarity

