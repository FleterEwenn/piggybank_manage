from flask import Flask, render_template, request, url_for, redirect

from DB_manage import insert_newuser, signin_user

app = Flask(__name__)

@app.route("/")
def Accueil():
    return render_template('Accueil.html')

@app.route("/SignIn")
def SignIn():
    return render_template('SignIn.html')

@app.route("/SignUp")
def SignUp():
    error_message = request.args.get('error')
    return render_template('SignUp.html', error=error_message)

@app.route("/Download", methods=["GET", "POST"])
def Download():
    if request.method == "POST":
        dict_form = request.form
        username = dict_form['username']
        password = dict_form['password']

        if dict_form['form_id'] == 'form_SI':
            insert_newuser(username, password)
            return render_template('Download.html', username=username, color=None)

        elif dict_form['form_id'] =='form_SU':

            user_table = signin_user(username, password)

            if user_table == None:
                return redirect(url_for("SignUp", error='Identifiant ou mot de passe incorrect'))
            
            else:
                color = user_table[0][1].split(',', 1)
                return render_template('Download.html', username=username, color=color[0])
            
    else:
        return redirect(url_for('Accueil'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)