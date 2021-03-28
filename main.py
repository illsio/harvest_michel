import json
from flask import Flask
from flask_cors import CORS
from database.database import countAll, fetchAll
from Threads import Threads
import os

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/test', methods=["GET"])
def test():
    # Example call: curl -X GET http://127.0.0.1:5000/test
    return "up and running"


@app.route('/getAllResults', methods=["GET"])
def getAllResults():
    # Example call: curl -X GET http://127.0.0.1:5000/getAllResults
    results = fetchAll()
    response = app.response_class(
        response=json.dumps(results),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/getResultsCount', methods=["GET"])
def getResultsCount():
    # Example call: curl -X GET http://127.0.0.1:5000/getResultsCount
    results = countAll()
    response = app.response_class(
        response=json.dumps(results),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/start', methods=["GET"])
def startEndlessRequestThread():
    # Example call: curl -X GET http://127.0.0.1:5000/start
    threads = Threads()
    return threads.startThread()


if __name__ == '__main__':
    isDocker = os.getenv("DOCKER")
    if isDocker:
        print("Environment is Docker")
        app.run(host='0.0.0.0', debug=True, threaded=True)
    else:
        print("Environment is NOT Docker")
        app.run(host= '127.0.0.1', debug=True, threaded=True)

