from flask import Flask
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
'db': 'your_database',
'host': 'localhost',
'port': 27017
}
db = MongoEngine()
db.init_app(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

def run(debug: bool=False):
    app.run(debug=debug)
    