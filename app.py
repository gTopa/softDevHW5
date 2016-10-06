from flask import Flask, render_template, request, redirect, url_for, session
import hashlib, os

app=Flask(__name__)
app.secret_key=os.urandom(32)

@app.route("/")
def disp_loginpage():
    if 'username' in session:
        return redirect(url_for('disp_loggedin'))
    return render_template("input.html")

@app.route("/auth", methods=['POST'])
def disp_auth():
    myHashObj = hashlib.sha1()
    myHashObj.update(request.form['passwd'])
    f = open('data/loginInfo.csv', 'r')
    userPass = f.read()
    f.close()
    userPass=userPass.split('\n')[0:-1]
    userPassDic={}
    for stuff in userPass:
        stuff=stuff.split(',')
        userPassDic[stuff[0]]=stuff[1]
    if 'login' in request.form.keys():
        if request.form['username'] in userPassDic.keys():
            if myHashObj.hexdigest()==userPassDic[request.form['username']]:
                session['username']=request.form['username']
        return redirect(url_for('disp_loginpage'))
    else:
        if request.form['username'] in userPassDic.keys():
            return render_template('badregister.html')
        f = open('data/loginInfo.csv', 'a')
        f.write(request.form['username']+','+myHashObj.hexdigest()+'\n')
        f.close()
        return redirect(url_for('disp_loginpage'))

@app.route("/logout")
def disp_logout():
    session.pop('username')
    return redirect(url_for('disp_loginpage'))
                    
@app.route("/loggedin")
def disp_loggedin():
    return render_template('home.html')

if __name__ == "__main__":
    app.debug = True
    app.run()
