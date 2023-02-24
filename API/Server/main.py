import jsonpickle
import requests
from flask import Flask, render_template, request, redirect, Response
from API import NBlazingAPI

app = Flask(__name__)


@app.route('/character')
def workkkk():
    n = NBlazingAPI.NBlazingApi()
    n = n.getCharacter('Naruto')
    js = jsonpickle.loads(n)
    return js


if __name__ == '__main__':
    app.run(debug=True)
