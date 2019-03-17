from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

project_name = "BRING ME BROADWAY"
net_id = "Nainika D'Souza (nmd65), Julie Phan (jp2254), Brooke Greenstein (bdg74), Arjun Chattoraj (ac2582), Stephanie Mark (srm276)"

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	if not query:
		data = []
		output_message = ''
	else:
		output_message = "Your search: " + query
		data = range(5)
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)



