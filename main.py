import json
from flask import Flask
from flask_cors import CORS
from database.database import countAll, fetchAll
from Threads import Threads

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
dings = "djdjdj"

"""
@app.route('/getJSON', methods=["GET"])
def getJSON():
    # Example call: curl -X GET http://127.0.0.1:5000/getJSON?hash=RvDQus7ubBlBcAeu
    hash = request.args.get('hash')

    db_entry = load(hash)

    result = db_entry["config"]
    response = app.response_class(
        response=json.dumps(result),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/getResults', methods=["GET", "POST"])
def getResults():
    hash = request.args.get('hash')
    db_entry = load(hash)


    return "response"


@app.route('/saveJSON', methods=["POST"])
def saveJSON():
    # Example call: curl -H Content-type:application/json -X POST -d@test.json http://127.0.0.1:5000/saveJSON
    # With test.json in the same folder
    json = request.get_json()
    saveChart(json)
    return 'success'

wpsUrl = 'https://csl-lig.hcu-hamburg.de/geoserver/ows?service=WPS&request=EXECUTE&version=1.0.0'

@app.route('/curl', methods=['POST'])
def reRouteCurl():
    # Example call: curl -H Content-type:text/xml -X POST -d@PointUnitQuery.xml http://127.0.0.1:5000/curl
    # With PointUnitQuery.xml in the same folder
    if request.method == 'POST':
        #result = execute(xml=request.get_data())
        return "result"
"""

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


if __name__ == "__main__":
    app.run(host= '127.0.0.1',debug=True,threaded=True,)


