from flask import Flask, jsonify, request, render_template, session, redirect
from flask_modules.loggraph.repository import loggraprepo
from flask_modules.loggraph.repository import exptrepo
from flask_modules.loggraph.repository import poprepo
from flask_modules.exceptions.dbhost import HostNotFoundException
from models.bollingerband import BollingerBand
app = Flask(__name__)
app.secret_key = 'milkcocholate'


@app.route("/", methods=['GET'])
def index():
    return render_template('connection.html')


@app.route("/reconnect", methods=['GET', 'POST'])
def reconnect():
    return redirect("/")


@app.route("/home", methods=["GET", "POST"])
def home():
    if 'host' in session:
        pass
    else:
        try:
            host = request.form['host']
            session['host'] = host
        except Exception:
            return render_template('connection.html')
    return render_template('home.html')


@app.route("/experiments", methods=['GET', 'POST'])
def experiments():
    if 'host' in session:
        host = session.get('host')
    else:
        return render_template('connection.html')
    try:
        repository = exptrepo.ExperimentRepository(host=host)
        experiment_list = repository.get_experiments()
    except HostNotFoundException:
        del session['host']
        return render_template('connection.html', has_error=host)
    return render_template('experiments.html', experiments=experiment_list)


@app.route("/populations", methods=['GET', 'POST'])
def populations():
    if 'host' in session:
        experiment_id = request.form['experiment_id']
        host = session.get('host')
    else:
        return render_template('connection.html')
    try:
        repository = poprepo.PopulationRepository(host=host)
        population_list = repository.get_populations(experiment_id=experiment_id)
        repository = exptrepo.ExperimentRepository(host=host)
        experiment = repository.get_experiment(experiment_id=experiment_id)
    except HostNotFoundException:
        del session['host']
        return render_template('connection.html', has_error=host)
    return render_template('populations.html', populations=population_list, experiment=experiment)


@app.route("/graph", methods=['GET', 'POST'])
def graph():
    if 'host' in session:
        population_id = request.form['population_id']
        host = session.get('host')
    else:
        return render_template('connection.html')
    try:
        repository = loggraprepo.LogGraphRepository(host=host)
        log_graph = repository.get_log_graph(population_id=population_id)
        repository = poprepo.PopulationRepository(host=host)
        population = repository.get_population(population_id=population_id)
    except HostNotFoundException:
        del session['host']
        return render_template('connection.html', has_error=host)
    return render_template('graph.html', log_graph=log_graph, population=population)


@app.route("/bollingerband", methods=['GET', 'POST'])
def bollingerband():
    if 'host' in session:
        host = session.get('host')
    else:
        return render_template('connection.html')
    try:
        bollingerband_controller = BollingerBand(host=host)
        bollingerbands = bollingerband_controller()
        return render_template('bollingerband.html', bollingerbands=bollingerbands)
    except HostNotFoundException:
        del session['host']
        return render_template('connection.html', has_error=host)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
