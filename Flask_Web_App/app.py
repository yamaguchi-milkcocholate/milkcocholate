from flask import Flask, jsonify, request, render_template
from flask_modules.loggraph import expt
app = Flask(__name__)


@app.route("/", methods=['GET'])
def index():
    experiment = expt.Experiment(
        crossover_name='uniform',
        fitness_function_name='simple_macd_params',
        situation=None,
        mutation_rate=50,
        cross_rate=2,
        population=100,
        elite_num=1,
        start_time="2018-10-21 12:34:56",
        end_time="2018-10-22 12:34:56",
        execute_time=86400
    )
    return render_template('index.html', experiments=[experiment, experiment, experiment])


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
