import jsonpickle
import requests
from flask import Flask, render_template, request, redirect, Response
from jsonpickle import json

from API import NBlazingAPI

app = Flask(__name__)


@app.route('/')
def character():
    n = NBlazingAPI.NBlazingApi()
    # n = n.getCharacters('Naruto')
    n = n.getCharacterInfo('https://naruto-blazing.fandom.com/wiki/Minato_Namikaze_%22Unfading_Courage%22_(%E2%98%855)')
    js = jsonpickle.loads(n)
    return Response(json.dumps(js, indent=4), content_type='application/json')


if __name__ == '__main__':
    app.run(debug=True)
