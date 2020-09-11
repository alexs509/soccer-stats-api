from flask import Flask, jsonify, request
import http.client
import json
from pymongo import MongoClient
import jwt
from flask_cors import CORS



""" --- Connection at DB --- """

client = MongoClient('localhost', 27017)
db = client.foot
users = db['users']


""" --- Declare global variable --- """

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
match = None
API_FOOT_ENDPOINT = http.client.HTTPSConnection("v3.football.api-sports.io")
headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': "86c4c54e5372c1e8f78a5c32ae8122f2"
}


""" --- Global functions --- """
def allCountries():
    global match
    API_FOOT_ENDPOINT.request("GET", "/countries", headers=headers)
    res = API_FOOT_ENDPOINT.getresponse()
    data = res.read()
    API_FOOT_ENDPOINT.close()
    jsonData = json.loads((data.decode("utf-8")))
    return jsonData

def ranking():
    global match
    API_FOOT_ENDPOINT.request("GET", "/standings?league=61&season=2020", headers=headers)
    res = API_FOOT_ENDPOINT.getresponse()
    data = res.read()
    API_FOOT_ENDPOINT.close()
    jsonData = json.loads((data.decode("utf-8")))
    return jsonData


def nextMeet():
    global match
    API_FOOT_ENDPOINT.request("GET", "/fixtures?league=61&season=2020", headers=headers)
    res = API_FOOT_ENDPOINT.getresponse()
    data = res.read()
    API_FOOT_ENDPOINT.close()
    jsonData = json.loads((data.decode("utf-8")))
    return jsonData


def allLeagues():
    global match
    API_FOOT_ENDPOINT.request("GET", "/leagues", headers=headers)
    res = API_FOOT_ENDPOINT.getresponse()
    data = res.read()
    API_FOOT_ENDPOINT.close()
    jsonData = json.loads((data.decode("utf-8")))
    return jsonData


def teamsStats(x):
    global match
    API_FOOT_ENDPOINT.request("GET", "/teams/statistics?league=61&season=2020&team="+x, headers=headers)
    res = API_FOOT_ENDPOINT.getresponse()
    data = res.read()
    API_FOOT_ENDPOINT.close()
    jsonData = json.loads((data.decode("utf-8")))
    return jsonData


def headToHead(x, y):
    global match
    API_FOOT_ENDPOINT.request(
        "GET", "/fixtures/headtohead?h2h="+x+"-"+y, headers=headers)
    res = API_FOOT_ENDPOINT.getresponse()
    data = res.read()
    API_FOOT_ENDPOINT.close()
    jsonData = json.loads((data.decode("utf-8")))
    return jsonData


def connection(username, password):
    checkUser = users.find_one({'username': username})
    
    if checkUser.get('password') == password:
        valueReturn = jwt.encode({'some': 'payload'}, 'secret', algorithm='HS256')
    else:
        return {"result":"error"}

    return valueReturn


def inscription(username, password):
    if username != None and password != None:
        users.insert_one(
            {"username": username, "password": password})
        return {"result":"added"}
    else:
        return {"result":"error"}


""" --- Routes --- """
@app.route('/')
def index():
    return "Server run !"


@app.route('/api/v1.0/next-match', methods=['GET'])
def next_meet():
    return nextMeet()


@app.route('/api/v1.0/teams-stats', methods=['GET'])
def teams_stats():
    team = request.args.get('team')
    return teamsStats(team)


@app.route('/api/v1.0/countries', methods=['GET'])
def get_countries():
    return allCountries()

@app.route('/api/v1.0/ranking', methods=['GET'])
def get_ranking():
    return ranking()


@app.route('/api/v1.0/headtohead', methods=['GET'])
def get_headtohead():
    team1 = request.args.get('team1')
    team2 = request.args.get('team2')
    return headToHead(team1,team2)


@app.route('/api/v1.0/leagues', methods=['GET'])
def get_leagues():
    return allLeagues()


@app.route('/api/v1.0/connection', methods=['POST'])
def connectionRoute():
    getForm = json.loads(request.data)
    return connection(getForm.get('username'), getForm.get('password'))


@app.route('/api/v1.0/inscription', methods=['POST'])
def inscriptionRoute():
    getForm = json.loads(request.data)
    return inscription(getForm.get('username'), getForm.get('password'))


if __name__ == '__main__':
    app.run(debug=True)
