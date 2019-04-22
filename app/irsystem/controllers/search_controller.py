from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import re
import pickle

project_name = "BRING ME BROADWAY"
net_id = "Nainika D'Souza (nmd65), Julie Phan (jp2254), Brooke Greenstein (bdg74), Arjun Chattoraj (ac2582), Stephanie Mark (srm276)"

# ranker
simmat = np.genfromtxt('sim_matrix.csv', delimiter=',')
with open('name_to_index.json') as json_file:  
    name_to_index = json.load(json_file)
with open('index_to_name.json') as json_file:  
    index_to_name = json.load(json_file)

# json of proper names ("Phantom of the Opera, The" --> "The Phantom of the Opera")
with open('proper_to_backend.json') as json_file:  
    proper_to_backend = json.load(json_file)
with open('backend_to_proper.json') as json_file:  
    backend_to_proper = json.load(json_file)

# list of proper names for display
proper_names_list = [*proper_to_backend]

# UNLEASH THE PICKLE
pickle_in = open("broadway_lyrics_v5.pkl","rb")
big_dict = pickle.load(pickle_in)
print(big_dict['Phantom of the Opera, The'])
# keys: composer (str), img_name (str), currently_playing (bool)
# description (str), script (list)

#### SEARCH FUNCITON START ####
@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')

	if not query:
		data = []
		query_title = ''
		results_list = []
	else:
		# convert from backend name to proper name
		query_title = backend_to_proper[query]

		if name_to_index[query]:
			mus_idx = name_to_index[query]
			score_list = simmat[mus_idx]
			sorted_i = np.argsort(score_list)[::-1]

			mus_score_list = [ backend_to_proper[ index_to_name[str(i)] ] for i,score in enumerate(score_list)]
			
			# get 11 results and delete top result, which is the query
			data = np.array(mus_score_list)[sorted_i][:11]
			data = np.delete(data, 0)

			# list of dictionaries
			results_list = []

			for musical_name in data:
				backend_name = proper_to_backend[musical_name]
				info = big_dict[backend_name]
				results_list.append(
					{'name': musical_name, \
					 'composer': info['composer'], \
					 'img_name': info['img_name'], \
					 'currently_playing': info['currently_playing']
					})

	return render_template('search.html', \
		name=project_name, netid=net_id, \
		query_title=query_title, data_list_dicts=results_list, allshows=proper_names_list, proper_to_backend_dict=proper_to_backend)