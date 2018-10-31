from flask import Flask, jsonify, request, render_template
from flask_modules.loggraph.repository import loggraprepo
from flask_modules.loggraph.repository import exptrepo
app = Flask(__name__)


@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')


@app.route("/experiments", methods=['GET'])
def experiments():
    host = 'mariadb'
    repository = exptrepo.ExperimentRepository(host=host)
    experiment_list = repository.get_experiments()
    return render_template('experiments.html', experiments=experiment_list)


@app.route("/graph/<population_id>", methods=['GET'])
def graph(population_id):
    host = 'mariadb'
    repository = loggraprepo.LogGraphRepository(host=host)
    log_graph = repository.get_log_graph(population_id=population_id)
    return render_template('graph.html', log_graph=log_graph)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
