from flask import Flask, request
from flask import render_template

app = Flask(__name__,
            static_folder="static", 
            template_folder="templates")

@app.route("/")
def main():
    return "nothing"

if __name__ == "__main__":
    app.run(host='0.0.0.0')