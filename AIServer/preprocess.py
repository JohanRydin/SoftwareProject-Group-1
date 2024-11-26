import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import ast

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

# Preprocess games descriptions
# PRE: './game_data/games_description.csv' and has columns "name","long_description","genres","overall_player_rating", "publisher", "link"
# POST: creates "./game_data/filtered_descriptions.csv" with filtered descriptions
# Returns None
def preprocess_games_description():
    df = pd.read_csv("./game_data/games_description.csv", usecols=["name","long_description","genres","overall_player_rating", "publisher", "link"])

    # Replace missing descriptions with an empty string
    df["long_description"].fillna("", inplace=True)

    # Remove stopwords from the descriptions
    filtered_descriptions = filter_stopwords(list(df["long_description"]))

    # Join stopwords into one string, we tokenize it later
    for n in range(0, len(filtered_descriptions)):
        filtered_descriptions[n] = ' '.join(filtered_descriptions[n])

    df["filtered_descriptions"] = filtered_descriptions

    df.to_csv("./game_data/filtered_descriptions.csv", index=True)

# Preprocess games ranking
# PRE: 'games_description.cvs' exists in subfolder 'game_data' and has columns "name","long_description","genres","overall_player_rating", "publisher", "link"
#      './game_data/games_ranking.csv' exists
# POST: creates "./game_data/games_ranking_indexed.csv" where games have an index
# Returns None
def preprocess_games_ranking():
    df = pd.read_csv("./game_data/games_ranking.csv")
    games_dict = init_game_id_dictionary(pd.read_csv("./game_data/games_description.csv", usecols=["name","long_description","genres","overall_player_rating", "publisher", "link"]))
    df['game_id'] = None

    
    for n in range(0, len(df['game_name'])):
        if df['game_name'][n] in games_dict:
            game_name = df.loc[n, 'game_name']
            df.loc[n, 'game_id'] = games_dict.get(game_name, None)

    df = df.dropna()

    # df contains both sales and revenue ranking, we remove revenue rankings since these are so highly correlated and sales is more interesting
    df = df[df["rank_type"] != "Revenue"]

    df.to_csv("./game_data/games_ranking_indexed.csv", index=False)

# Create a list of genres ranked on their appearance in games
# PRE: "./game_data/games_description.csv" exists
# POST: "./game_data/genres.csv" exists with genres and their count
# Returns None
def do_genre_csv():
    df = pd.read_csv("./game_data/games_description.csv", usecols=["genres"])
    df['genres_list'] = df['genres'].apply(ast.literal_eval)
    
    genre_dict = {}
    for genres in df['genres_list']:
        for genre in genres:
            if (genre in genre_dict):
                genre_dict[genre] = genre_dict[genre] + 1
            else:
                genre_dict[genre] = 1
            
    sorted_genre_kvps = sorted(genre_dict.items(), key=lambda item: item[1], reverse=True)

    keys, values = zip(*sorted_genre_kvps)
    genre_df = pd.DataFrame({'Genre' : keys, 'Count' : values})

    genre_df.to_csv("./game_data/genres.csv", index=True, index_label='genre_id')

# Add ids to csv with list of games
# PRE: "./game_data/games_description.csv" exists
# POST: "./game_data/games_description.csv" contains the column 'game_id' with unique int indexes
# Returns None
def add_ids_to_csv():
    df = pd.read_csv("./game_data/games_description.csv")
    df.to_csv("./game_data/games_description_indexed.csv", index=True, index_label='game_id')

#preprocess_games_ranking()
#do_genre_csv()
#add_ids_to_csv()
    

# "./games_description.csv" -> "./../csvs/games_description.csv"

