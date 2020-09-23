from flask import Flask, flash, redirect, url_for, render_template, request, session
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# Session secret key
app.secret_key = 'smm'
app.config['SQLALCHEMY_DATABSE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Date time session
app.permanent_session_lifetime = timedelta(minutes=5)

# SQL
db = SQLAlchemy(app)

# Model to store info


class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

# Pages


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/view')
def view():
    return render_template('view.html', values=users.query.all())

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        # permanent session
        session.permanent = True
        # data in form
        user = request.form['nm']
        session['user'] = user

        found_user = users.query.filter_by(name=user).first()

        if found_user:
            session['email'] = found_user.email
        else:
            usr = users(user, '')
            # add to the model
            db.session.add(usr)
            # commit changes
            db.session.commit()

        flash('Login Succesful!')
        return redirect(url_for('user'))
    else:
        if 'user' in session:
            flash('Already Logged In!')
            return redirect(url_for('user'))

        return render_template('login.html')


@app.route('/user', methods=['POST', 'GET'])
def user():
    email = None
    if 'user' in session:
        user = session['user']
        if request.method == 'POST':
            email = request.form['email']
            session['email'] = email
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            flash('Email was saved!')
        else:
            if 'email' in session:
                email = session['email']

        return render_template('user.html', email=email)
    else:
        flash('Youare not logged in!')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    flash('You have been logged out!', 'info')
    session.pop('user', None)
    session.pop('email', None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
