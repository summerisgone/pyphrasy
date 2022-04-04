# -*- coding: utf-8 -*-
from os.path import dirname, join

import pymorphy2
from aiohttp import web
from aiohttp.web_response import Response
from multidict import MultiDictProxy

from inflect import PhraseInflector, GRAM_CHOICES

PROJECT_ROOT = dirname(__file__)
routes = web.RouteTableDef()


@routes.post('/inflect')
async def post_handler(request: web.Request):
    params = await request.post()
    return _inflect(params)


@routes.get('/inflect')
async def get_handler(request: web.Request):
    params = request.query
    return _inflect(params)


def _inflect(params: MultiDictProxy) -> Response:
    if 'phrase' not in params:
        web.json_response({'error': 'укажите слово'}, status=400)
    if 'forms' not in params and 'cases' not in params:
        web.json_response({'error': 'выберите падежи или/и числа'}, status=400)
    phrase = params['phrase']
    form_sets = params.getall('forms') if params.getall('forms') else params.getall('cases')
    morph = pymorphy2.MorphAnalyzer()
    inflector = PhraseInflector(morph)
    result = {'orig': phrase}
    for forms_string in form_sets:
        form_set = set(forms_string.split(',')) & set(GRAM_CHOICES)
        result[forms_string] = inflector.inflect(phrase, form_set)
    return web.json_response(result)


if __name__ == '__main__':
    app = web.Application()
    app.router.add_routes(routes)
    app.add_routes([web.static('/', join(PROJECT_ROOT, 'static'))])
    web.run_app(app, port=8000)
