from similarity import similarity
import numpy as np
from recommendations import Recommender

def test1():
    docs = ["Mars is the fourth planet in our solar system.",
            "It is second-smallest planet in the Solar System after Mercury.", 
            "Saturn is yellow planet."]
    query = ["Saturn is the sixth planet from the Sun."]
    similarities = similarity(docs, query)
    sum_of_sims =(np.sum(similarities, dtype=np.float32))
    sim = round(float(sum_of_sims / len(docs)), 2)
    #print(sim)
    assert sim > 0.25 and sim < 0.27, "Incorrect similarity with docs from example"

def test2():
	docs1 = ["Mars is the fourth planet in our solar system.",
            "It is second-smallest planet in the Solar System after Mercury.", 
	        "Saturn is yellow planet."]
	docs2 = ["Saturn is the sixth planet from the Sun.", "Saturn is yellow planet."]
 
	similarity1 = similarity(docs1, [docs1[1]])
	similarity2 = similarity(docs2, [docs2[0]])

	assert similarity1[1] >= 0.99, "Incorrect similarity 1 with docs from example"
	assert similarity2[0] >= 0.99, "Incorrect similarity 2 with docs from example"
      
def test_create_recommender():
      rec = Recommender(10)
      assert rec, "rec is None ! >:("
      
def test_recommendations_1():
	rec = Recommender(100)
	request_user = {"id": 5, "game_ids": [3, 5], "genres": ["Action", "Strategy", "Adventure"]}
	request_rows = [{"similar_to_games": [1, 7, 3]}, {"similar_to_games": "all"}, {"similar_to_genre": "Sports"}, {"best_reviewed": "Adventure"}, {"best_sales": "Action"}]
	recommendations = rec.get_recommendations(request_user, request_rows)
	assert len(recommendations) == 5, ">:( NO"
 
def test_recommendations_default():
	rec = Recommender(100)
	request_user = {"id": 5, "game_ids": [3, 5], "genres": ["Action", "Strategy", "Adventure"]}
	request_rows = [{'similar_to_games':'all'},{"similar_to_genre": None}, {"best_reviewed": None}, {"best_sales": None}]
	recommendations = rec.get_recommendations(request_user, request_rows)
	assert len(recommendations) == 4, ">:( NO"
 
def test_recommendations_default_no_genres():
	rec = Recommender(100)
	request_user = {"id": 5, "game_ids": [3, 5], "genres": []}
	request_rows = [{'similar_to_games':'all'},{"similar_to_genre": None}, {"best_reviewed": None}, {"best_sales": None}]
	recommendations = rec.get_recommendations(request_user, request_rows)
	assert len(recommendations) == 4, ">:( NO"

def test_all_super_genres():
	rec = Recommender(100)
	genre_types = ["Action", "Adventure", "Role-Playing", "Simulation", "Strategy", "Sports & Racing"]
	for genre in genre_types:
		request_user = {"id": 5, "game_ids": [3, 5], "genres": [genre]}
		request_rows = [{'similar_to_games':'all'},{"similar_to_genre": None}, {"best_reviewed": None}, {"best_sales": None}]
		recommendations = rec.get_recommendations(request_user, request_rows)
		assert len(recommendations) == 4, ">:( NO"
	
def test_recommendations_game_count():
	rec = Recommender(100)
	request_user = {"id": 5, "game_ids": [3, 5], "genres": ["Action", "Strategy", "Adventure"]}
	request_rows = [{"similar_to_games": [1, 7, 3]}, {"similar_to_games": "all"}, {"similar_to_genre": "Sports"}, {"best_reviewed": "Adventure"}, {"best_sales": "Action"}]
	recommendations = rec.get_recommendations(request_user, request_rows, num = 5)
	assert len(recommendations) == 5, ">:( NO"

	recommendation_count = 0
	for r in recommendations:
		recommendation_count = recommendation_count + len(r)
	assert recommendation_count == 25, ":?"

	