import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def filter_stopwords(data):
    stop_words = stopwords.words("english")
    tokens = [[w.lower() for w in word_tokenize(doc)] for doc in data]

    stop_words = set(stopwords.words('english'))

    filtered_sentences = [[w for w in token if not w.lower() in stop_words] for token in tokens]

    return filtered_sentences

df = pd.read_csv("./game_data/games_description.csv", usecols=["name","long_description","genres","overall_player_rating", "publisher", "link"])

#print(df[df["short_description"].isna()].shape)
#print(df[df["long_description"].isna()].shape)
#print("Short average length: ", df['short_description'].dropna().str.len().mean())
#print("Long average lenth: ", df['long_description'].dropna().str.len().mean())


df["long_description"].fillna("", inplace=True)

filtered_descriptions = filter_stopwords(list(df["long_description"]))
df["description_tokens"] = filtered_descriptions
print("Token average lenth: ", df['description_tokens'].apply((lambda x: sum(len(s) for s in x))).mean())
#print(filtered_descriptions[0])

df.to_csv("./game_data/filtered_descriptions.csv", index=False)

