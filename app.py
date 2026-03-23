from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Seed: 34567891387103"

