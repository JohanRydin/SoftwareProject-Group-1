import similarity

def test1():
    data = ["Mars is the fourth planet in our solar system.",
            "It is second-smallest planet in the Solar System after Mercury.", 
            "Saturn is yellow planet."]
    query = ["Saturn is the sixth planet from the Sun."]
    sim = similarity.similarity(data, query)
    assert(sim > 25 and sim < 27)
