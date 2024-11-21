from similarity import similarity, sim_matrix, find_best_indices, combine_matrixes
import pandas as pd
import time


df = pd.read_csv("./game_data/filtered_descriptions.csv", usecols=['name', 'filtered_descriptions', 'genres'])

df = df.iloc[:100]
#tokenList = list(df['filtered_descriptions'])

#matrix = sim_matrix(tokenList)

sim_matrixes = list()
sim_matrixes.append(sim_matrix(list(df['filtered_descriptions'])))
sim_matrixes.append(sim_matrix(list(df['genres'])))

weights = list()
weights.append(1)
weights.append(1)

matrix = combine_matrixes(sim_matrixes, weights)

#print(matrix)
sim = matrix[1]
#print(sim)

amount = 10
res = find_best_indices(amount, sim)
#Idea: filter out very similiar recomendations
print(df['name'][1])
for n in range(0, amount):
    print(df['name'][res[n]], "  ")#, tokenList[res[n]])

#fifth = tokenList.pop(5)
#start_time = time.time()
#sim = similarity(tokenList, [fifth])
#print("--- %s seconds ---" % (time.time() - start_time))
#print(sim)

