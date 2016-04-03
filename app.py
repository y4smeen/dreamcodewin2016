from flask import Flask, render_template, request, session, redirect, url_for
import database, os
app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home(): 
    if ('id' not in session):
        session['id'] = -1
    session['id'] = -1
    if session['id'] == -1:
        return render_template("home.html")
    else:
        return render_template("study.html")

@app.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        repeat_password = request.form['repeat_password']
        name = request.form['name']
        email = request.form['email'].lower()
        result = database.valid_create(username, password, repeat_password, name, email)
        if result[0]:
            return redirect("login")
        else:
            message = result[1]
            return render_template("create.html", error=True, message=message)
    else:
        return render_template("create.html")
        
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verifylogin = database.valid_login(username, password)
        if verifylogin != -1:
            session['type'] = 'parent'
            session['id'] = verifylogin
            return redirect("home")
        else:
            return render_template("login.html", error=True)
    else:
        return render_template("login.html")
        
@app.route("/search", methods=['GET', 'POST'])
def search():
    if session['id'] == -1:
        return redirect(url_for("home"))
    if request.method == 'POST':
        return render_template("results.html")
    else:
        return render_template("search.html")
        
@app.route("/logout")
def logout():
    #resets the session to none
    session['id'] = -1
    return redirect(url_for("home"))
        
if __name__ == "__main__":
    app.debug = True
    app.secret_key = "adashljdoiqdm"
    #app.run('0.0.0.0',port=8000)
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)))
