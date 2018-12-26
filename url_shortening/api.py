from datetime import datetime, timedelta

from flask import Flask, request, jsonify, redirect, current_app
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

from url_shortening.model.models import TinyUrl
from url_shortening.service.shorten import HashShorten, PoolShorten, get_origin_url
from url_shortening.lru_cache import local_cache


@app.route('/shortening', methods=['POST'])
def shortening():
    jdata = request.get_json(force=True, silent=True)
    if jdata is None:
        return jsonify({'code': -1, 'message': 'arguments error', 'data': None}), 400

    origin_url = jdata.get('origin_url')
    custom_key = jdata.get('custom_key')
    expiration = jdata.get('expiration')
    if not origin_url:
        return jsonify({'code': -1, 'message': 'arguments error', 'data': None}), 400

    shorten_algo = current_app.config.get('SHORTEN_ALGO', 'HashShorten')
    shorten = eval('{}()'.format(shorten_algo))

    tiny_url, write_db = shorten.shorten_url(origin_url, custom_key)
    if tiny_url is None:
        return jsonify({'code': -1, 'message': 'system error', 'data': None}), 400

    if write_db:
        m = TinyUrl.model(key=tiny_url)(key=tiny_url, origin_url=origin_url)
        if expiration:
            m.expiration = datetime.now() + timedelta(days=int(expiration))
        m.save()

    data = {'tiny_url': tiny_url}
    return jsonify({'code': 0, 'message': 'success', 'data': data})


@app.route('/<string:key>', methods=['GET'])
def redirect_to_origin(key):
    origin_url = local_cache.get(key)
    if origin_url:
        print(local_cache)
        return redirect(origin_url, code=301)

    rec = get_origin_url(key)
    if not rec or not rec.origin_url:
        return jsonify({'code': -1, 'message': 'invalid tiny url', 'data': None}), 400


    local_cache.add(key, rec.origin_url)
    print(local_cache)
    return redirect(rec.origin_url, code=301)


