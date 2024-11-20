from similarity import similarity

def test1():
    data = ["Mars is the fourth planet in our solar system.",
            "It is second-smallest planet in the Solar System after Mercury.", 
            "Saturn is yellow planet."]
    query = ["Saturn is the sixth planet from the Sun."]
    sim = similarity(data, query)
    print(sim)
    assert(sim > 0.25 and sim < 0.27, "Incorrect similarity with data from example")
