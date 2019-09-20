from flask import Flask, render_template,request
from tabledef import *
import os
from twilio.rest import Client
from challengefile import hashed_challenge

engine = create_engine('sqlite:///tutorial.db', echo=True)


app = Flask(__name__)


@app.route('/')
def welcome(tobeDisplayed="none"):
    return render_template('login.html',tobeDisplayed=tobeDisplayed)

@app.route('/home')
def home():
    #tobeDisplayed="block"
    return render_template('home.html')
def login2():
    tobeDisplayed = "block"

    return render_template('login.html', tobeDisplayed=tobeDisplayed)

@app.route('/login1',methods=['POST','GET'])
def login1():
    #Checking if computed resoinse key matches with the key generated
    if request.method == 'POST':
            h = 0
            s = str(hashed_challenge)
            for c in s:
                h = (31 * h + ord(c)) & 0xFFFFFFFF
            r=abs(((h + 0x80000000) & 0xFFFFFFFF) - 0x80000000)
    r_key = request.form['text']
    if int(r_key)==r:
        return home()
    else:
        error = "Invalid key"
        tobeDisplayed="block"

    return render_template("login.html", error=error,tobeDisplayed=tobeDisplayed)


@app.route('/login',methods=['POST','GET'])
def login():
    Session = sessionmaker(bind=engine)
    s=Session()
    error=None
    tobeDisplayed="block"

    # username and password entered
    p_usname=request.form['username']
    p_pwd=request.form['password']
    if request.method == 'POST':
        query = s.query(User).filter(User.username.in_([p_usname]), User.password.in_([p_pwd]))
        result = query.first()
        if result:

            account_sid ='<twilio account id>'
            auth_token = '<twilio token>'
            client = Client(account_sid, auth_token)
            message_body = 'Your challenge is : ' + str(hashed_challenge)
            from_number = ''
            to_number = ''
            message = client.messages \
                .create(
                body=message_body,
                from_=from_number,
                status_callback='https://hookb.in/LgEWelk1pyIMEMrOg21p',
                to=to_number
             )

            print(message.sid)
            return welcome("block")

        else:

            print("inside else")
            tobeDisplayed="none"
            error = "Invalid credentials ! Please try again."

    return render_template("login.html", error=error,tobeDisplayed=tobeDisplayed)



if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)
