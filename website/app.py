# -*- coding: utf-8 -*-
from flask import Flask, render_template, g
from pymongo import Connection


try:
    from local_settings import *
except ImportError:
    sys.exit("No Flask Local Settings found!")

app = Flask(__name__)
app.debug = True


@app.route("/")
def hello():
    tweets = g.coll.find(sort=[('created_at', -1)], limit=10)
    return render_template('test.html', tweets=tweets)

if __name__ == "__main__":
    app.run()


@app.before_request
def before_request():
    g.conn = Connection(MONGO_HOST)
    g.db = g.conn[MONGO_DB]
    g.coll = g.db[MONGO_COLLECTION]


@app.teardown_request
def teardown_request(exception):
    g.conn.disconnect()
