from ogame import OGame
from flask import *

empire = OGame('Indus', 'marcos.gam7@gmail.com', 'MarcosDaniel')
barakis = Flask(__name__, static_url_path='')


def modefy_ogame(url):
    response = empire.session.get(empire.index_php + url)
    with open('injected.html') as file:
        injected = file.read()
    response = response.text + injected
    response = response.replace(empire.index_php, 'http://127.0.0.1:5000/')
    return render_template_string(response, fleet=len(empire.fleet()))


@barakis.route('/')
@barakis.route('/<ogame_url>')
def ogame_pages(ogame_url='page=ingame&component=overview'):
    response = Response()
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.data = modefy_ogame(ogame_url)
    return response


barakis.run()
