from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

project_name = "BRING ME BROADWAY"
net_id = "Nainika D'Souza (nmd65), Julie Phan (jp2254), Brooke Greenstein (bdg74), Arjun Chattoraj (ac2582), Stephanie Mark (srm276)"

# ranker
simmat = np.genfromtxt('sim_matrix.csv', delimiter=',')
with open('name_to_index.json') as json_file:  
    name_to_index = json.load(json_file)
with open('index_to_name.json') as json_file:  
    index_to_name = json.load(json_file)

print(name_to_index)
print(index_to_name)

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	if not query:
		data = []
		output_message = ''
	else:
		musical = query
		mus_idx = name_to_index[musical]
		score_list = simmat[mus_idx]
		sorted_i = np.argsort(score_list)[::-1]
		# print(index_to_name)
		mus_score_list = [(index_to_name[str(i)], score) for i,score in enumerate(score_list)]
		output_message = 'TADAAAA'
		
		data = np.array(mus_score_list)[sorted_i]
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)



