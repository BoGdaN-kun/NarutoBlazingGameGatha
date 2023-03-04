import time

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
    start_time = time.time()
    characterR = api.searchAllCharactersWithName(name)
    jsonR = jsonpickle.loads(characterR)
    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")
    return Response(json.dumps(jsonR, indent=4), content_type='application/json')


@app.route('/characters')
def allCharacters():
    start_time = time.time()

    characterR = api.AllCharacters()
    jsonR = jsonpickle.loads(characterR)
    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")
    return Response(json.dumps(jsonR, indent=4), content_type='application/json')


@app.route('/character/<name>/info')
def character(name):
    # calculate the time it takes to get the character info using timeit
    start_time = time.time()
    characterR = api.getCharacterInfoByName(name)
    jsonR = jsonpickle.loads(characterR)
    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")
    return Response(json.dumps(jsonR, indent=4), content_type='application/json')


if __name__ == '__main__':
    app.run(debug=True)
