from similarity import similarity, sim_matrix, find_best_indices, combine_matrixes, combine_vectors
import pandas as pd
import time
import ast


def init_similarity_matrix(df):
    sim_matrixes = list()
    sim_matrixes.append(sim_matrix(list(df['filtered_descriptions'])))
    sim_matrixes.append(sim_matrix(list(df['genres'])))

    weights = list()
    weights.append(1)
    weights.append(1)

    return combine_matrixes(sim_matrixes, weights)

def find_similar_games(game_ids, matrix):
    sim_vectors = list()
    for n in game_ids:
        sim_vectors.append(matrix[n])
    sim = combine_vectors(sim_vectors)
    for n in game_ids:
        sim[n] = 0
    return sim
def find_similar_genres(game_ids, matrix, genre, df):
    vector = find_similar_games(game_ids, matrix)
    for n in range(0, len(vector)):
        genres = df['genres_list'][n]
        if (genre not in genres):
            vector[n] = 0
    return vector

def find_best(rank_df, genre, num_of_games, rank_type):
    df = rank_df[rank_df['genre'] == genre]
    df = df[df['rank_type'] == rank_type]
    vector = list()
    for n in range(0, num_of_games):
        vector.append(0)

    count = len(df['game_id'])
    current = count
    for i in df['game_id']:
        vector[i] = current / count
        current = current - 1
    return vector

def extract_games(indices, df):
    games = list()
    for n in indices:
        games.append(df['name'][n])
    return games

# args: arguments on the form: {user: {name, [game_ids], [genres]}, rows: [similar_to : [1, 5, 2], best_reviewed : "Action", similar_to : [5], best_sales : "Adventure"]}
def get_recommendations(user, row_requests, num = 10):
    game_ids = user['game_ids']

    games_list = list()

    for request in row_requests:
        command = list(request.keys())[0]
        similar = None
        if (command == 'similar_to_games'):
            if (request[command] == 'all'):
                similar = find_similar_games(game_ids, matrix)  # TODO: accessing global variable 'matrix'
            else:
                similar = find_similar_games(request[command], matrix)  # TODO: accessing global variable 'matrix'
        elif (command == 'similar_to_genre'):
            similar = find_similar_genres(game_ids, matrix, request[command], df)   # TODO: accessing global variables 'matrix', 'df'
        elif (command == 'best_reviewed'):
            similar = find_best(rank_df, request[command], len(df), 'Review')   # TODO: accessing global variables 'rank_df', 'df
        elif (command == 'best_sales'):
            similar = find_best(rank_df, request[command], len(df), 'Sales')   # TODO: accessing global variables 'rank_df', 'df
        
        if (similar):
            indices = find_best_indices(num, similar)
            games = extract_games(indices, df)
            games_list.append(games)

    return games_list

df = pd.read_csv("./game_data/filtered_descriptions.csv", usecols=['name', 'filtered_descriptions', 'genres'])
df['genres_list'] = df['genres'].apply(ast.literal_eval)

rank_df = pd.read_csv("./game_data/games_ranking_indexed.csv", usecols=['game_name', 'rank','rank_type', 'genre', 'game_id'])

num_of_games = len(df['name'])

df = df.iloc[:100]

start_time = time.time()
matrix = init_similarity_matrix(df)
print("--- %s seconds ---" % (time.time() - start_time))



start_time = time.time()
#sim = find_similar_games([1,55,56,57], matrix)
sim = find_similar_genres([1,55,56,57, 8, 4, 6, 86, 76, 75, 73], matrix, 'Aliens', df)
print("--- %s seconds ---" % (time.time() - start_time))

amount = 10
best_sales = find_best(rank_df, 'Action', num_of_games, 'Sales')
best_reviews = find_best(rank_df, 'Action', num_of_games, 'Review')
res = find_best_indices(amount, best_sales)
#Idea: filter out very similiar recomendations
#print(df['name'][1])
for n in range(0, amount):
    print(df['name'][res[n]], "  ")#, tokenList[res[n]])

