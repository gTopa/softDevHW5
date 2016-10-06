from flask import Flask, render_template, request, redirect, url_for, session
import hashlib

app=Flask(__name__)

@app.route("/")
def disp_loginpage():
    if 'username' in session:
        redirect(url_for('disp_loggedin'))
    return render_template("home.html")

@app.route("/auth", methods=['POST'])
def disp_auth():
    myHashObj = hashlib.sha1()
    myHashObj.update(request.form['passwd'])
    if 'login' in request.form.keys():
        f = open('data/loginInfo.csv', 'r')
        userPass = f.read()
        f.close()
        userPass=userPass.split('\n')[0:-1]
        userPassDic={}
        for stuff in userPass:
            stuff=stuff.split(',')
            userPassDic[stuff[0]]=stuff[1]
        if request.form['username'] in userPassDic.keys():
            if myHashObj.hexdigest()==userPassDic[request.form['username']]:
                session['username']=request.form['username']
                return render_template("auth.html", status='success')
        return render_template("auth.html", status='fail')
    else:
        f = open('data/loginInfo.csv', 'a')
        f.write(request.form['username']+','+myHashObj.hexdigest()+'\n')
        f.close()
        return render_template("register.html")

@app.route("/logout")
def disp_logout():
    session.pop('username')
    return redriect(url_for('disp_loginpage'))
                    
@app.route("/loggedin")
def disp_loggedin():
    return "welcome to special place"

if __name__ == "__main__":
    app.debug = True
    app.run()
