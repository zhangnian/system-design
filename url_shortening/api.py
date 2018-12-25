from datetime import datetime, timedelta

from flask import Flask, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

from url_shortening.model.models import TinyUrl
from url_shortening.service.shorten import shorten_url, get_origin_url


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

    tiny_url, write_db = shorten_url(origin_url, custom_key)
    if tiny_url is None:
        return jsonify({'code': -1, 'message': 'system error', 'data': None}), 400

    if write_db:
        m = TinyUrl(key=tiny_url, origin_url=origin_url)
        if expiration:
            m.expiration = datetime.now() + timedelta(days=int(expiration))
        m.save()

    data = {'tiny_url': tiny_url}
    return jsonify({'code': 0, 'message': 'success', 'data': data})


@app.route('/<string:key>', methods=['GET'])
def redirect_to_origin(key):
    rec = get_origin_url(key)
    if not rec or not rec.origin_url:
        return jsonify({'code': -1, 'message': 'invalid tiny url', 'data': None}), 400

    return redirect(rec.origin_url, code=301)


