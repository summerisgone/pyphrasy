# -*- coding: utf-8 -*-
import json
import pymorphy2
from flask import Flask, request, render_template
from inflect import PhraseInflector, CASE_CHOICES

app = Flask(__name__)
app.debug = True

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/inflect", methods=['GET', 'POST'])
def inflect():
    if request.method == 'POST':
        params = request.form
    else:
        params = request.args

    if 'phrase' not in params:
        return u'укажите слово', 400,  {'Content-Type':'text/plain; charset=utf-8'}
    if 'cases' not in params:
        return u'выберите падежи', 400,  {'Content-Type':'text/plain; charset=utf-8'}

    phrase = params['phrase']
    cases = params.getlist('cases')
    cases = set(CASE_CHOICES).intersection(cases)

    morph = pymorphy2.MorphAnalyzer()
    inflector = PhraseInflector(morph)
    result = {'orig': phrase}
    for case in cases:
        result[case] = inflector.inflect(phrase, case)
    return json.dumps(result), 200, {'Content-Type':'text/json; charset=utf-8'}

if __name__ == "__main__":
    app.run()
