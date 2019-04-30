from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import re
import pickle
import json
import numpy as np

project_name = "BRING ME BROADWAY"
net_id = "Nainika D'Souza (nmd65), Julie Phan (jp2254), Brooke Greenstein (bdg74), Arjun Chattoraj (ac2582), Stephanie Mark (srm276)"

# ranker - updated 4/29
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

# json of proper names ("Phantom of the Opera, The" --> "The Phantom of the Opera")
with open('proper_to_backend.json') as json_file:  
    proper_to_backend = json.load(json_file)
with open('backend_to_proper.json') as json_file:  
    backend_to_proper = json.load(json_file)

#json of adjectives
with open('adjs.json') as json_file:  
    adj_dict = json.load(json_file)

# list of proper names for display
proper_names_list = [*proper_to_backend]

# UNLEASH THE PICKLE
pickle_in = open("broadway_lyrics_v5.pkl","rb")
big_dict = pickle.load(pickle_in)
# keys: composer (str), img_name (str), currently_playing (bool)
# description (str), script (list)

# data for javascript. key=name, val=img path
search_data = {k : big_dict[v]['img_name'] for (k,v) in proper_to_backend.items()}

#### SEARCH FUNCITON START ####
@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')

	if not query:
		data = []
		results_list = []
		query_data = None
	else:
		# convert from proper name to backend name
		query_backend = proper_to_backend[query]

		# print(big_dict[query_backend])

		if name_to_index[query_backend]:
			# new ranker, updated 4/29
			mus_idx = name_to_index[query_backend]
			score_list = lyrsim_weighted[mus_idx] + compsim_weighted[mus_idx] + descsim_weighted[mus_idx] + revsim_weighted[mus_idx]
			sorted_i = np.argsort(score_list)[::-1]

			# tuple of proper name and similiarity dictionary
			mus_score_list = [ 
				( backend_to_proper[index_to_name[str(i)]], \
					{	'overall_sim': round(score, 3), \
						'lyric_sim': round(lyrsim_weighted[mus_idx][i], 3), \
						'composer_sim': round(compsim_weighted[mus_idx][i], 3), \
						'desc_sim': round(descsim_weighted[mus_idx][i], 3),\
						'review_sim': round(revsim_weighted[mus_idx][i], 3) \
					} 
				) for i, score in enumerate(score_list) ]

			data = np.array(mus_score_list)[sorted_i][1:13]
			# print(data)
			# 
			
			# list of dictionaries
			results_list = []

			for musical_name, musical_dict in data:
				backend_name = proper_to_backend[musical_name]
				info = big_dict[backend_name]
				# remove weird periods in composer str
				composer_str = re.sub('[!@#$\.]', '', info['composer'])

				# if there is a ticket link:
				if 'ticket_link' in info:
					results_list.append(
						{'name': musical_name, \
						'description': info['show_score_description'], \
						'show_score': info['show_score'], \
						'composer': composer_str, \
						'img_name': info['img_name'], \
						'currently_playing': info['currently_playing'], \
						'ticket_link': info['ticket_link'], \
						'sim_dict': musical_dict, \
						'adj_list': adj_dict[backend_name]
						})
				else: 
					# if there is NOT a ticket link:
					results_list.append(
						{'name': musical_name, \
						'description': info['show_score_description'], \
						'show_score': info['show_score'], \
						'composer': composer_str, \
						'img_name': info['img_name'], \
						'currently_playing': info['currently_playing'], \
						'ticket_link': None, \
						'sim_dict': musical_dict, \
						'adj_list': adj_dict[backend_name]
						})

			# info for query
			query_info = big_dict[query_backend]
			# remove weird periods in composer str
			composer_str = re.sub('[!@#$\.]', '', query_info['composer'])
			print(composer_str)

			# if there is a ticket link:
			if 'ticket_link' in query_info:
				query_data = {'name': query, 
					'description': query_info['show_score_description'], \
					'show_score': query_info['show_score'], \
					'composer': composer_str, \
					'img_name': query_info['img_name'], \
					'currently_playing': query_info['currently_playing'], \
					'ticket_link': query_info['ticket_link'], \
					'adj_list': adj_dict[query_backend] }
			else:
				query_data = {'name': query, 
					'description': query_info['show_score_description'], \
					'show_score': query_info['show_score'], \
					'composer': composer_str, \
					'img_name': query_info['img_name'], \
					'currently_playing': query_info['currently_playing'], \
					'ticket_link': None, \
					'adj_list': adj_dict[query_backend] }

	return render_template('search.html', \
		name=project_name, netid=net_id, \
		query_title=query, data_list_dicts=results_list, proper_to_backend_dict=proper_to_backend, search_data=search_data, query_data=query_data )