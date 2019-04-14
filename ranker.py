import json
import numpy as np

simmat = np.genfromtxt('sim_matrix.csv', delimiter=',')
with open('name_to_index.json') as json_file:  
    name_to_index = json.load(json_file)
with open('index_to_name.json') as json_file:  
    index_to_name = json.load(json_file)

def rank_mus(musical):
	mus_idx = name_to_index[musical]
	score_list = simmat[mus_idx]
	sorted_i = np.argsort(score_list)[::-1]
	# print(index_to_name)
	mus_score_list = [(index_to_name[str(i)], score) for i,score in enumerate(score_list)]
	return np.array(mus_score_list)[sorted_i]


