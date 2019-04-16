# in progress, ignore for now --steph
from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder


# @app.route('/', methods=['GET'])
def mainpage():
    project_name = "BRING ME BROADWAY"
    net_id = "Nainika D'Souza (nmd65), Julie Phan (jp2254), Brooke Greenstein (bdg74), Arjun Chattoraj (ac2582), Stephanie Mark (srm276)"

    return render_template('main.html', name=project_name, netid=net_id)