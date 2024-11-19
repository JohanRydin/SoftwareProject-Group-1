from nltk.tokenize import word_tokenize
import re

def tokenize(data):
    tokens = [w.lower() for w in word_tokenize(data)]
    return tokens

def cleaning(data):
    data = re.sub('http\S+\s*', '', data)  # remove URLs
    data = re.sub('RT|cc', '', data)  # remove RT and cc
    data = re.sub('#\S+', '', data)  # remove hashtags
    data = re.sub('@\S+', '', data)  # remove mentions
    data = re.sub(r'[!"\$%&\'()*+,-./:;<=>?\[\\\]^_`{|}~]', '', data)  # remove punctuations
    data = re.sub(r'[^\x00-\x7f]', r'', data)
    return data

data = "Mars is a cold desert world. It is half the size of Earth. "
data = cleaning(data)
data = tokenize(data)

print(data)

