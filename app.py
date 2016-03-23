from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def login():
    return render_template("home.html")

if __name__ == "__main__":
    app.debug = True
    app.secret_key = "adashljdoiqdm"
    app.run('0.0.0.0',port=8000)
