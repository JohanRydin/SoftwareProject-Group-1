from similarity import similarity, sim_matrix, find_best_indices, combine_matrixes, combine_vectors
import pandas as pd
import time
import ast


class Recommender:
    matrix = None
    df = None
    rank_df = None

    def __init__(self, game_count, print_time=False):
        start_time = time.time()
        self.df = pd.read_csv("./game_data/filtered_descriptions.csv", usecols=['name', 'filtered_descriptions', 'genres'])
        self.df['genres_list'] = self.df['genres'].apply(ast.literal_eval)

        self.rank_df = pd.read_csv("./game_data/games_ranking_indexed.csv", usecols=['game_name', 'rank','rank_type', 'genre', 'game_id'])

        if (game_count > len(self.df['name'])):
            game_count = len(self.df['name'])
        self.df = self.df.iloc[:game_count]

        self.matrix = self.init_similarity_matrix(self.df)
        if (print_time):
            print("--- %s seconds ---" % (time.time() - start_time))

    def init_similarity_matrix(self, df):
        sim_matrixes = list()
        sim_matrixes.append(sim_matrix(list(df['filtered_descriptions'])))
        sim_matrixes.append(sim_matrix(list(df['genres'])))

        weights = list()
        weights.append(1)
        weights.append(1)

        return combine_matrixes(sim_matrixes, weights)

    def find_similar_games(self, game_ids, matrix):
        sim_vectors = list()
        for n in game_ids:
            sim_vectors.append(matrix[n])
        sim = combine_vectors(sim_vectors)
        for n in game_ids:
            sim[n] = 0
        return sim
    def find_similar_genres(self, game_ids, matrix, genre, df):
        vector = self.find_similar_games(game_ids, matrix)
        for n in range(0, len(vector)):
            genres = df['genres_list'][n]
            if (genre not in genres):
                vector[n] = 0
        return vector

    def find_best(self, rank_df, genre, num_of_games, rank_type):
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

    def extract_games(self, indices, df):
        games = list()
        for n in indices:
            games.append(df['name'][n])
        return games

    # args: arguments on the form: {user: {name, [game_ids], [genres]}, rows: [similar_to : [1, 5, 2], best_reviewed : "Action", similar_to : [5], best_sales : "Adventure"]}
    def get_recommendations(self, user, row_requests, num = 10):
        game_ids = user['game_ids']

        games_list = list()

        for request in row_requests:
            command = list(request.keys())[0]
            similar = None
            if (command == 'similar_to_games'):
                if (request[command] == 'all'):
                    similar = self.find_similar_games(game_ids, self.matrix)
                else:
                    similar = self.find_similar_games(request[command], self.matrix)
            elif (command == 'similar_to_genre'):
                similar = self.find_similar_genres(game_ids, self.matrix, request[command], self.df)
            elif (command == 'best_reviewed'):
                similar = self.find_best(self.rank_df, request[command], len(self.df), 'Review')
            elif (command == 'best_sales'):
                similar = self.find_best(self.rank_df, request[command], len(self.df), 'Sales')
            
            if (similar):
                indices = find_best_indices(num, similar)
                games = self.extract_games(indices, self.df)
                games_list.append(games)

        return games_list
