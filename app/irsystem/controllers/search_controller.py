from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import re

project_name = "BRING ME BROADWAY"
net_id = "Nainika D'Souza (nmd65), Julie Phan (jp2254), Brooke Greenstein (bdg74), Arjun Chattoraj (ac2582), Stephanie Mark (srm276)"

# ranker. lowercase all strings
simmat = np.genfromtxt('sim_matrix.csv', delimiter=',')
with open('name_to_index.json') as json_file:  
    name_to_index = json.load(json_file)
with open('index_to_name.json') as json_file:  
    index_to_name = json.load(json_file)

# lowercase the dictionaries
name_to_index = dict((k.lower(), v) for k,v in name_to_index.items())
print(name_to_index)

index_to_name = dict((k, v.lower()) for k,v in index_to_name.items())
print(index_to_name)

# https://stackoverflow.com/questions/1549641/how-to-capitalize-the-first-letter-of-each-word-in-a-string-python
def repl_func(m):
    """process regular expression match groups for word upper-casing problem"""
    return m.group(1) + m.group(2).upper()
# end

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')

	if not query:
		data = []
		query_title = ''
	else:
		# lowercase the query
		musical = query.lower()
		if name_to_index[musical]:
			mus_idx = name_to_index[musical]
			score_list = simmat[mus_idx]
			sorted_i = np.argsort(score_list)[::-1]
			# print(index_to_name)

			mus_score_list = [ re.sub("(^|\s)(\S)", repl_func, index_to_name[str(i)]) for i,score in enumerate(score_list)]
			query_title = musical.title()
			
			# get results except top result, which is the query
			data = np.array(mus_score_list)[sorted_i][:10]
			data = np.delete(data, 0)
		
	return render_template('search.html', name=project_name, netid=net_id, query_title=query_title, data=data)