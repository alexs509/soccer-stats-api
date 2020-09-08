from flask import Flask, jsonify
import http.client
import json


""" --- Declare global variable --- """

app = Flask(__name__)

API_FOOT_ENDPOINT = http.client.HTTPSConnection("v3.football.api-sports.io")
headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': "c8ba2608a4945269ae8378865c55cbb5"
    }
match = None

""" --- Global functions --- """
def allCountries():
    global match
    API_FOOT_ENDPOINT.request("GET", "/countries", headers=headers)
    res = API_FOOT_ENDPOINT.getresponse()
    data = res.read()
    jsonData = json.loads((data.decode("utf-8")))
    return jsonData

def allTeams():
    global match
    API_FOOT_ENDPOINT.request("GET", "/teams", headers=headers)
    res = API_FOOT_ENDPOINT.getresponse()
    data = res.read()
    jsonData = json.loads((data.decode("utf-8")))
    return jsonData

def teamsStats(x):
    global match
    API_FOOT_ENDPOINT.request("GET", "/teams?id="+x, headers=headers)
    res = API_FOOT_ENDPOINT.getresponse()
    data = res.read()
    jsonData = json.loads((data.decode("utf-8")))
    return jsonData

def headToHead(x,y):
    global match
    API_FOOT_ENDPOINT.request("GET", "/fixtures/headtohead?h2h="+x+"-"+y, headers=headers)
    res = API_FOOT_ENDPOINT.getresponse()
    data = res.read()
    jsonData = json.loads((data.decode("utf-8")))
    return jsonData


""" --- Routes --- """
@app.route('/')
def index():
    return "Server run !"

@app.route('/api/v1.0/teams', methods=['GET'])
def get_teams():
    return allTeams()

@app.route('/api/v1.0/teams-stats', methods=['GET'])
def teams_stats():
    return teamsStats("33")

@app.route('/api/v1.0/countries', methods=['GET'])
def get_countries():
    return allCountries()

@app.route('/api/v1.0/headtohead', methods=['GET'])
def get_headtohead():
    return headToHead("33","34")
    

if __name__ == '__main__':
    app.run(debug=True)