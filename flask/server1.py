import flask 

app = flask.Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, Server1!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)