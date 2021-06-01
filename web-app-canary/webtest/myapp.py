from flask import Flask
from pymemcache.client import base

app = Flask(__name__)
cache = base.Client(('cache-memcached', 11211))

@app.route("/")
def hello():
    curcount = increment_my_item()
    f = open("/app/data/data", "r")
    data = f.read()
    ret = "<h1 style='color:red'>Canary v7<br/>current count is {} </h1>".format(curcount)
    ret += "<p>Data content is:<p><br>{}<br>".format(data)
    return ret


@app.route("/health")
def health():
    return "Ok!"


@app.route("/version")
def version():
    return "15.0.0"


def get_my_item():
    rv = cache.get('count')
    return int(rv)


def increment_my_item():
    rv = cache.get('count')
    if rv is None:
        rv = 1
    rv = int(rv) + 1
    cache.set('count', rv)
    return rv


if __name__ == "__main__":
    app.run(host='0.0.0.0')
