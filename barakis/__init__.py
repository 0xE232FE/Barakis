from flask import *
from io import BytesIO
from gevent.pywsgi import WSGIServer
from threading import Thread
from ogame import OGame

try:
    from settings import *
    import bot
except ImportError:
    from barakis.settings import *
    import barakis.bot as bot

barakis = Flask(__name__, static_url_path='/', static_folder='/')


def inject_ogame(url, X_Requested_With=False):
    if X_Requested_With:
        response = empire.session.get(empire.index_php + url, headers={'X-Requested-With': 'XMLHttpRequest'})
        return response.text
    else:
        response = empire.session.get(empire.index_php + url)
        with open('injected.html') as file:
            injected = file.read()
        response = response.text + injected
        response = response.replace(empire.index_php, 'http://{}:5000/'.format(ip_adress))
        js_index_php = 'https:\/\/s{}-{}.ogame.gameforge.com\/game\/index.php?'.format(empire.server_number,
                                                                                       empire.server_language)
        response = response.replace(js_index_php, 'http:\/\/{}:5000/'.format(ip_adress))
        response = response.replace('https://gf1.geo.gfsrv.net/', 'http://{}:5000/GEO/1/'.format(ip_adress))
        response = response.replace('https://gf2.geo.gfsrv.net/', 'http://{}:5000/GEO/2/'.format(ip_adress))
        response = response.replace('https://gf3.geo.gfsrv.net/', 'http://{}:5000/GEO/3/'.format(ip_adress))
        return render_template_string(response, fleet=len(empire.fleet()))


@barakis.route('/')
def index():
    response = Response()
    response.headers["Access-Control-Allow-Origin"] = "*"
    with open('bot_setup.html') as file:
        setup = file.read()
    setup = render_template_string(setup,
                                   main_planet=bot_settings['main_planet'],
                                   expedition=bot_settings['expedition'],
                                   expedition_large_transporter=bot_settings['expedition_large_transporter'],
                                   inactive=bot_settings['inactive'],
                                   inactive_large_transporter=bot_settings['inactive_large_transporter'],
                                   build_mines=bot_settings['build_mines'],
                                   repeat=bot_settings['repeat'])
    load_script = "<script>document.getElementById('middle').innerHTML = '{}'</script>".format(setup)
    response.data = inject_ogame('page=ingame&component=preferences') + load_script.replace('\n', '')
    return response


@barakis.route('/<ogame_url>', methods=['GET'])
def ogame_pages(ogame_url):
    response = Response()
    response.headers["Access-Control-Allow-Origin"] = "*"
    if 'X-Requested-With' in request.headers:
        response.data = inject_ogame(ogame_url, X_Requested_With=True)
    else:
        response.data = inject_ogame(ogame_url)
    return response


@barakis.route('/<ogame_url>', methods=['POST'])
def ogame_post(ogame_url):
    response = Response()
    if 'X-Requested-With' in request.headers:
        response.data = empire.session.post(
            url=empire.index_php + ogame_url,
            data=dict(request.form),
            headers={'X-Requested-With': 'XMLHttpRequest'}
        ).text
    else:
        response.data = empire.session.post(empire.index_php + ogame_url, data=dict(request.form)).text
    return response


@barakis.route('/GEO/<nr>/<dir>/<res>', methods=['GET'])
def ogame_GEO(nr, dir, res):
    response = empire.session.get('https://gf{}.geo.gfsrv.net/{}/{}'.format(nr, dir, res)).content
    return send_file(BytesIO(response), attachment_filename=res)


@barakis.route('/bot_settings', methods=['POST'])
def set_settings():
    new_settings = dict(request.form)
    for setting in bot_settings:
        bot_settings[setting] = ''
    for setting, value in new_settings.items():
        bot_settings[setting] = value
    Thread(target=bot.start_tasks, args=(empire,)).start()
    return redirect('/')


if universum == '' or username == '' or password == '':
    print('PLS input User Info')
    universum = input('Universum: ')
    username = input('Usernameor Email: ')
    password = input('Password: ')
try:
    empire = OGame(universum, username, password)
except TypeError:
    raise Exception('Bad Login')
worker = Thread(target=bot.worker, args=(empire,))
worker.start()
proxy = WSGIServer(('0.0.0.0', 5000), barakis)
print('Visit: http://{}:5000'.format(ip_adress))
proxy.serve_forever()
