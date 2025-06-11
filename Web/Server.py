from flask import Flask, render_template, request, url_for, redirect

from DB_manage import recup

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
        res = recup()
        print(res)
        return render_template('Download.html')
    else:
        return redirect(url_for('Accueil'))

if __name__ == '__main__':
    app.run(debug=True)