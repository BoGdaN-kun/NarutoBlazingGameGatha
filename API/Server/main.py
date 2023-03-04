import jsonpickle
import requests
from flask import Flask, render_template, request, redirect, Response
from jsonpickle import json

from API import NBlazingAPI

app = Flask(__name__)

# Initialize the API
api = NBlazingAPI.NBlazingApi()


@app.route('/characters/<name>')
def searchAllCharactersWithName(name):
    characterR = api.searchAllCharactersWithName(name)
    jsonR = jsonpickle.loads(characterR)
    return Response(json.dumps(jsonR, indent=4), content_type='application/json')


@app.route('/characters')
def allCharacters():
    characterR = api.AllCharacters()
    jsonR = jsonpickle.loads(characterR)
    return Response(json.dumps(jsonR, indent=4), content_type='application/json')


@app.route('/character/<name>/info')
def character(name):
    characterR = api.getCharacterInfoByName(name)
    jsonR = jsonpickle.loads(characterR)
    return Response(json.dumps(jsonR, indent=4), content_type='application/json')


if __name__ == '__main__':
    app.run(debug=True)
