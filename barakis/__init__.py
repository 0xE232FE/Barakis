from ogame import OGame
from flask import *
from bot import *

empire = OGame('', '', '')
barakis = Flask(__name__, static_url_path='/', static_folder='/')
settings = {'active': '',
            'expedition': '',
            'inactive_farm': ''}


def inject_ogame(url):
    response = empire.session.get(empire.index_php + url)
    with open('injected.html') as file:
        injected = file.read()
    response = response.text + injected
    response = response.replace(empire.index_php, 'http://127.0.0.1:5000/')
    return render_template_string(response, fleet=len(empire.fleet()))


@barakis.route('/')
def index():
    response = Response()
    response.headers["Access-Control-Allow-Origin"] = "*"
    with open('bot_setup.html') as file:
        setup = file.read()
    setup = render_template_string(setup,
                                   active=settings['active'],
                                   expedition=settings['expedition'],
                                   inactive_farm=settings['inactive_farm'])
    load_script = "<script>document.getElementById('middle').innerHTML = '{}'</script>".format(setup)
    response.data = inject_ogame('page=ingame&component=preferences') + load_script.replace('\n', '')
    return response


@barakis.route('/<ogame_url>')
def ogame_pages(ogame_url='page=ingame&component=overview'):
    response = Response()
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.data = inject_ogame(ogame_url)
    return response


@barakis.route('/bot_settings', methods=['POST'])
def set_settings():
    global settings
    settings = {'active': '',
                'expedition': '',
                'inactive_farm': ''}
    new_settings = dict(request.form)
    for setting in new_settings:
        settings[setting] = 'checked'
    return redirect('/')


barakis.run()
