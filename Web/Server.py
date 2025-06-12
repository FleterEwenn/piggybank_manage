from flask import Flask, render_template, request, url_for, redirect

from DB_manage import insert_newuser

app = Flask(__name__)

@app.route("/")
def Accueil():
    return render_template('Accueil.html')

@app.route("/SignIn")
def SignIn():
    return render_template('SignIn.html')

@app.route("/Download", methods=["GET", "POST"])
def Download():
    if request.method == "POST":
        dict_form = request.form
        username = dict_form['username']
        password = dict_form['password']
        insert_newuser(username, password)
        return render_template('Download.html', username=username)
    else:
        return redirect(url_for('Accueil'))

if __name__ == '__main__':
    app.run(debug=True)