from nltk.tokenize import word_tokenize
import gensim
import numpy as np

#Extracts the tokens in the docs
# docs - a list of strings/documents
# returns the string tokenized, thereby returning a list of words 
def tokenize(docs):
    tokens = [[w.lower() for w in word_tokenize(doc)] for doc in docs]
    return tokens

# Calculate the average similarity of the query to each document in docs
# docs - a list of strings/documents
# query - a list of strings (should have length 1)
# returns a value from 0 to 1 specifying the level of similarity between the query and the docs
def similarity(query, dictionary, tf_idf, sims):
    
    query_doc = tokenize(query)

    query_doc_bow = dictionary.doc2bow(query_doc[0])

    query_doc_tf_idf = tf_idf[query_doc_bow]
    return sims[query_doc_tf_idf]

# Initialize the parameters for querying the similarity of a document
# docs - all documents to account for
# returns A bunch of shit
def init_similarity_parameters(docs):
    tokens = tokenize(docs)
    dictionary = gensim.corpora.Dictionary(tokens)
    #print(dictionary.token2id, '\n')
    corpus = [dictionary.doc2bow(doc) for doc in tokens]
    #print(corpus, '\n')

    tf_idf = gensim.models.TfidfModel(corpus)
    #for doc in tf_idf[corpus]:
    #    print([[dictionary[id], np.around(freq, decimals=2)] for id, freq in doc])

    # building the index
    sims = gensim.similarities.Similarity('workdir/',tf_idf[corpus], num_features=len(dictionary))
    return dictionary, tf_idf, sims

# Creates similarity matrix for the given dataset of documents
# docs - contains a list of descriptions
# returns the matrix that can be indexed by matrix[queryindex] to get all the similarities for that particular index
#WARNING: Runtime of approx 6-7 mins with 300 elems
def sim_matrix(docs):
    dictionary, tf_idf, sims = init_similarity_parameters(docs)
    sim_matrix = list()
    for n in range(0, len(docs)):
        sim = similarity([docs[n]], dictionary, tf_idf, sims)
        sim[n] = 0
        sim_matrix.append(sim)
    return sim_matrix

# Finds the top X indices
# number - the number of indices to take
# similarities - a vector of numeric similarity values
# returns a list of top indices
def find_best_indices(number, similarities):
    return sorted(range(len(similarities)), key = lambda sub: similarities[sub], reverse=True)[:number]

# Combine several matrixes into one, weighing them with different weights
# PRE - each matrix must have the same dimensions, and len(matrixes) must be equal to len(weights)
# matrixes - the matrixes to combine
# weights - the weights for each matrix
# returns one matrix
def combine_matrixes(matrixes, weights):
    size = len(matrixes[0])
    matrix = list()
    for n in range(0,size):
        matrix.append([0] * size)
    
    for i in range(0, len(matrixes)):
        for n in range(0,size):
            for m in range(0,size):
                matrix[n][m] += matrixes[i][n][m] * weights[i]
    return matrix
    
# Add several vectors into one
# PRE - vectors must be equal in length
# vectors - the vectors to combine
# returns one vector
def combine_vectors(vectors):
    size = len(vectors[0])
    vector = list()
    for n in range(0,size):
        vector.append(0)

    for i in range(0, len(vectors)):
        for n in range(0,size):
                vector[n] += vectors[i][n]
    return vector
