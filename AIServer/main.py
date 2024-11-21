from similarity import similarity
import pandas as pd

df = pd.read_csv("./game_data/filtered_descriptions.csv", usecols=['description_tokens'])

tokenList = list(df['description_tokens'].iloc[:5])

sim = similarity(tokenList, [tokenList[2]], isTokens=True)
print(sim)

