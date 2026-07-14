from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route("/", methods=["POST"])
def home():
    return "hi Maurice"

@app.route("/index", methods=["POST"])
def index():
    return "Helloworld"
    
if __name__ == "__main__":
    app.run(debug=True, port=5000)
        
    
