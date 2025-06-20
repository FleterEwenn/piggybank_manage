from flask import Flask, render_template, request, url_for, redirect, jsonify
import json

from DB_manage import insert_newuser, signin_user_forweb, signin_user_forapp, update_save_forapp

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

            user_table = signin_user_forweb(username, password)

            if user_table == None:
                return redirect(url_for("SignUp", error='Identifiant ou mot de passe incorrect'))
            
            else:
                color = user_table[0][1].split(',', 1)
                return render_template('Download.html', username=username, color=color[0])
            
    else:
        return redirect(url_for('Accueil'))

@app.route("/DBforApp", methods=["POST"])
def DBforApp():
    if request.method == "POST":
        dict_form = request.form
        request_type = dict_form['type']

        if request_type == 'signin':
            response = signin_user_forapp(dict_form['username'], dict_form['password'])
            return jsonify({ 'id' : response[0][0], 'username' : response[0][1], 'password' : response[0][2], 'money' : response[0][3], 'color' : response[0][4], 'listValue' : response[0][5]})

        elif request_type == 'update':
            response = update_save_forapp(dict_form['money'], dict_form['color'], dict_form['listValue'], dict_form['id'])
        
        else:
            return 'request does not exist'
    
    else: 
        return 'method is not allowed'
    
@app.route("/VerifUpdate", methods=["POST"])
def VerifUpdate():
    with open('static/AppInfo.json', 'r') as file:
        data = json.load(file)

    version_user = request.form
    major,minor,patch = data['version'].split('.', 2)
    majorU,minorU,patchU = version_user['version'].split('.', 2)

    if major > majorU:
        return 'Une mise à jour très importante est disponible. Voulez-vous l\'installer ?'
    elif minor > minorU:
        return 'Une mise à jour est disponible. Voulez-vous l\'installer ?'
    elif patch > patchU:
        return 'Une correction de bugs à été réalisée. Voulez-vous l\'installer ?'
    else:
        return 'NoUpdate'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)