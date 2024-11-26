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
    