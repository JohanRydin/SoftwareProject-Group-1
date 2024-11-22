import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

def init_game_id_dictionary(df):
    game_dict = {}
    id = 0
    for n in df['name']:
        game_dict[n] = id
        id += 1
    return game_dict

# Remove uninteresting symbols from a string
# docs - a single string
# returns a string without the specified symbols
def cleaning(docs):
    docs = re.sub('http\S+\s*', '', docs)  # remove URLs
    docs = re.sub('RT|cc', '', docs)  # remove RT and cc
    docs = re.sub('#\S+', '', docs)  # remove hashtags
    docs = re.sub('@\S+', '', docs)  # remove mentions
    docs = re.sub(r'[!"\$%&\'()*+,-./:;<=>?\[\\\]^_`{|}~]', '', docs)  # remove punctuations
    docs = re.sub(r'[^\x00-\x7f]', r'', docs)
    return docs

#Filters away stopwords in the given data
#data - list of strings to filter
def filter_stopwords(data):
    stop_words = stopwords.words("english")
    tokens = [[w.lower() for w in word_tokenize(cleaning(doc))] for doc in data]

    stop_words = set(stopwords.words('english'))

    filtered_sentences = [[w for w in token if not w.lower() in stop_words] for token in tokens]

    return filtered_sentences

def preprocess_games_description():

    df = pd.read_csv("./game_data/games_description.csv", usecols=["name","long_description","genres","overall_player_rating", "publisher", "link"])

    #print(df[df["short_description"].isna()].shape)
    #print(df[df["long_description"].isna()].shape)
    #print("Short average length: ", df['short_description'].dropna().str.len().mean())
    #print("Long average lenth: ", df['long_description'].dropna().str.len().mean())


    df["long_description"].fillna("", inplace=True)

    filtered_descriptions = filter_stopwords(list(df["long_description"]))

    for n in range(0, len(filtered_descriptions)):
        filtered_descriptions[n] = ' '.join(filtered_descriptions[n])
    #print(filtered_descriptions)

    df["filtered_descriptions"] = filtered_descriptions
    #print("Token average lenth: ", df['description_tokens'].apply((lambda x: sum(len(s) for s in x))).mean())
    #print(filtered_descriptions[0])

    df.to_csv("./game_data/filtered_descriptions.csv", index=True)

def preprocess_games_ranking():
    df = pd.read_csv("./game_data/games_ranking.csv")
    games_dict = init_game_id_dictionary(pd.read_csv("./game_data/games_description.csv", usecols=["name","long_description","genres","overall_player_rating", "publisher", "link"]))
    df['game_id'] = None

    
    for n in range(0, len(df['game_name'])):
        if df['game_name'][n] in games_dict:
            #df['game_id'][n] = games_dict[df['game_name'][n]]
            game_name = df.loc[n, 'game_name']
            df.loc[n, 'game_id'] = games_dict.get(game_name, None)

    df = df.dropna()

    df.to_csv("./game_data/games_ranking_indexed.csv", index=False)

    # TODO: split this into smaller CSVS and then use it to make a new category of recommendations

preprocess_games_ranking()
    
