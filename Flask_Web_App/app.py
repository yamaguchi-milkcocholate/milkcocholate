from flask import Flask, jsonify, request, render_template
from flask_modules.loggraph.repository import loggraprepo
from flask_modules.loggraph.repository import exptrepo
from flask_modules.loggraph.repository import poprepo
from flask_modules.exceptions import dbhost
app = Flask(__name__)


@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')


@app.route("/experiments", methods=['GET', 'POST'])
def experiments():
    try:
        host = request.form['host']
    except Exception:
        return render_template('error.html')
    try:
        repository = exptrepo.ExperimentRepository(host=host)
        experiment_list = repository.get_experiments()
    except dbhost.HostNotFoundException:
        return render_template('error.html', has_error=host)
    return render_template('experiments.html', experiments=experiment_list, host=host)


@app.route("/populations", methods=['GET', 'POST'])
def populations():
    try:
        experiment_id = request.form['experiment_id']
        host = request.form['host']
    except Exception:
        return render_template('error.html')
    try:
        repository = poprepo.PopulationRepository(host=host)
        population_list = repository.get_populations(experiment_id=experiment_id)
    except dbhost.HostNotFoundException:
        return render_template('error.html', has_error=host)
    return render_template('populations.html', populations=population_list, host=host)


@app.route("/graph", methods=['GET', 'POST'])
def graph():
    try:
        population_id = request.form['population_id']
        host = request.form['host']
    except Exception:
        return render_template('error.html')
    try:
        repository = loggraprepo.LogGraphRepository(host=host)
        log_graph = repository.get_log_graph(population_id=population_id)
    except dbhost.HostNotFoundException:
        return render_template('error.html', has_error=host)
    return render_template('graph.html', log_graph=log_graph)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
