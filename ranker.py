import json
import numpy as np

lyrsim = np.genfromtxt('sim_matrix.csv', delimiter=',') # lyrics similarity
with open('name_to_index.json') as json_file:  
    name_to_index = json.load(json_file)
with open('index_to_name.json') as json_file:  
    index_to_name = json.load(json_file)
compsim = np.genfromtxt('composer_sim.csv', delimiter=',') # composer similarity
descsim = np.genfromtxt('SVM_sim.csv', delimiter=',') # description similarity
revsim = np.genfromtxt('review_sim.csv', delimiter=',') # description similarity

w_lyr = 0.10
w_comp = 0.10
w_desc = 0.50
w_rev = 0.30

lyrsim_weighted = lyrsim*w_lyr
compsim_weighted = compsim*w_comp
descsim_weighted = descsim*w_desc
revsim_weighted = revsim*w_rev

def rank_mus(musical):
	mus_idx = name_to_index[musical]
	score_list = lyrsim_weighted[mus_idx] + compsim_weighted[mus_idx] + descsim_weighted[mus_idx] + revsim_weighted[mus_idx]
	sorted_i = np.argsort(score_list)[::-1]
	mus_score_list = [(index_to_name[str(i)], score) for i,score in enumerate(score_list)]
	return np.array(mus_score_list)[sorted_i]


