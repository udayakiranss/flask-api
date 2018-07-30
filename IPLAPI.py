from flask import Flask

app = Flask(__name__)


@app.route('/')
def welcome_message():
    return "Welcome to Python IPL API"


if __name__ == '__main__':
    app.run(debug=1)
