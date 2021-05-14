from flask import Flask
from pymemcache.client import base

app = Flask(__name__)
cache = base.Client(('cache-memcached', 11211))

@app.route("/")
def hello():
    increment_my_item()
    curcount = get_my_item()
    return "<h1 style='color:green'>Service Mesh rules!!!!<br/>current count is {} </h1>".format(curcount)


@app.route("/health")
def health():
    return "Ok!"


@app.route("/version")
def version():
    return "12.0.0"


def get_my_item():
    rv = cache.get('count')
    return int(rv)


def increment_my_item():
    rv = cache.get('count')
    if rv is None:
        rv = 1
    rv = int(rv) + 1
    cache.set('count', rv)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
