from similarity import similarity, sim_matrix, find_best_indices, combine_matrixes, combine_vectors
import pandas as pd
import time
import ast
import random

class Recommender:
    matrix = None
    df = None
    rank_df = None

    # Constructor >:)
    # game_count - The number of games to consider. At most around 300, but it will take several minutes to initialize with all games.
    # print_time - Set to True to print the time it took to initialize the state variables
    def __init__(self, game_count=300, print_time=False):
        start_time = time.time()
        self.df = pd.read_csv("./game_data/filtered_descriptions.csv", usecols=['name', 'filtered_descriptions', 'genres'])
        self.df['genres_list'] = self.df['genres'].apply(ast.literal_eval)

        self.rank_df = pd.read_csv("./game_data/games_ranking_indexed.csv", usecols=['game_name', 'rank','rank_type', 'genre', 'game_id'])

        if (game_count < len(self.df['name'])):
            self.df = self.df.iloc[:game_count]

        self.matrix = self.init_similarity_matrix(self.df)
        if (print_time):
            print("--- %s seconds ---" % (time.time() - start_time))

    # Initialize similarity matrix, n^2 time complexity :(
    # df - dataframe containing games
    # Returns matrix
    def init_similarity_matrix(self, df):
        sim_matrixes = list()
        sim_matrixes.append(sim_matrix(list(df['filtered_descriptions'])))
        sim_matrixes.append(sim_matrix(list(df['genres'])))

        weights = list()
        weights.append(1)
        weights.append(1)

        return combine_matrixes(sim_matrixes, weights)
    
    # Finds similiar games based on the games chosen
    #game_ids - chosen games
    #matrix - similarity matrix
    def find_similar_games(self, game_ids, matrix):
        sim_vectors = list()
        for n in game_ids:
            sim_vectors.append(matrix[n])
        sim = combine_vectors(sim_vectors)
        for n in game_ids:
            sim[n] = 0
        return sim
    
    # Finds similiar games based on the games chosen and a specific genre
    #game_ids - chosen games
    #matrix - similarity matrix
    #genre - the chosen genre
    #df - pandas dataframe with games and their genres
    def find_similar_genres(self, game_ids, matrix, genre, df):
        vector = self.find_similar_games(game_ids, matrix)
        for n in range(0, len(vector)):
            genres = df['genres_list'][n]
            if (genre not in genres):
                vector[n] = 0
        return vector

    # Finds the best games within a genre based on a criteria
    # rank_df - dataframe with game rankings
    # genre - string with genre to retrieve
    # num_of_games - number of games in system
    # rank_type - criteria (ex: 'Sales', 'Review')
    # return ranking vector of games
    def find_best(self, rank_df, genre, num_of_games, rank_type):
        df = rank_df[rank_df['genre'] == genre]
        df = df[df['rank_type'] == rank_type]
        vector = list()
        for n in range(0, num_of_games):
            vector.append(0)

        count = len(df['game_id'])
        current = count
        for i in df['game_id']:
            if i<num_of_games:
                vector[i] = current / count
            current = current - 1
        return vector
    
    # Extracts game names based on the ids sent in
    # game_ids - all the games that the user wants the name of
    # df - pandas dataframe with the game names and their correspondingg id
    def extract_games(self, game_ids, df):
        games = list()
        for n in game_ids:
            games.append(df['name'][n])
        return games

    # Get a list of lists of game recommendations
    # user - dictionary containing user information such as game preferences and genre preferences
    # row_requests - commands and data for different types of recommendations
    # num - the number of recommendations for each command
    # returns a list of lists of recommendations where each recommendation ID
    # Example: example post that the API ggets: {user: {name, [game_ids], [genres]}, rows: [similar_to : [1, 5, 2], best_reviewed : "Action", similar_to : [5], best_sales : "Adventure"]}
    def get_recommendations(self, user, row_requests, num = 10):
        game_id_strings = user['game_ids']
        game_ids = list()
        for id_string in game_id_strings:
            game_ids.append(int(id_string))

        games_list = list()

        for request in row_requests:
            command = list(request.keys())[0]
            request_data = request[command]

            if (not request_data):
                if len(user['genres']) > 0:
                    request_data = user['genres'][random.randint(0, len(user['genres']) - 1)]
                else:
                    request_data = 'Action' # deal with it >:)

            similar = None
            
            # Handle each request separately depending on their command
            if (command == 'similar_to_games'):
                if (request_data == 'all'): # Compare to all the games the user likes
                    similar = self.find_similar_games(game_ids, self.matrix)
                else:   # Compare to a custom set of games
                    data_ids = list()
                    for id in request_data:
                        data_ids.append(int(id))
                    similar = self.find_similar_games(request_data, self.matrix)
            elif (command == 'similar_to_genre'):   # Compare all the games the user likes that are part of a specific genre
                similar = self.find_similar_genres(game_ids, self.matrix, request_data, self.df)
            elif (command == 'best_reviewed'):      # Compare the best reviewed games with a genre
                similar = self.find_best(self.rank_df, request_data, len(self.df), 'Review')
            elif (command == 'best_sales'):         # Compare the best sold games with a genre
                similar = self.find_best(self.rank_df, request_data, len(self.df), 'Sales')
            
            if (similar):
                indices = find_best_indices(num, similar)
                games_list.append(indices)
                #games = self.extract_games(indices, self.df)
                #games_list.append(games)

        return games_list
