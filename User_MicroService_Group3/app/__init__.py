from flask import Flask

from app.models import login

app = Flask(__name__)

from app import routes

if __name__ == '__main__':
    app.run(debug=True)