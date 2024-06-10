from flask import Flask
from flask_cors import CORS


#from app.models import models

app = Flask(__name__)
CORS(app)

#db = sqlAlchemy

#from app import routes

if __name__ == '__main__':
    app.run(debug=True)