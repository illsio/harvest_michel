import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import xml.etree.ElementTree as ET
from database.database import saveChart, load, loadAll
from backend.compose import composeXml, joinConfig
from backend.wps import execute

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/parseQuery', methods=["POST"])
def parseQuery():
    ## Hier das Parsen der JSON
    return 'success'


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
    if db_entry is not None:
        config = joinConfig(db_entry["config"], request)
        print(json.dumps(config, indent=4))
        requestXml = composeXml(config)
        print(requestXml)

        result = execute(requestXml, config=config)
        response = app.response_class(
            response=result,
            status=200,
            mimetype='application/json'
        )
    else:
        response = app.response_class(
            response="Could retrieve Request from DB",
            status=404,
            mimetype='text/plain'
        )

    return response

@app.route('/getAllResults', methods=["GET"])
def getAllResults():
    # Example call: curl -X GET http://127.0.0.1:5000/getAllResults
    results = loadAll()
    response = app.response_class(
        response=json.dumps(results),
        status=200,
        mimetype='application/json'
    )
    return response

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
        result = execute(xml=request.get_data())
        return result

if __name__ == "__main__":
    app.run(host= '127.0.0.1',debug=True,threaded=True)
