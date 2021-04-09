import os
import secrets
from flask import render_template, url_for, flash, redirect, request
from reapp import app, db, bcrypt
from reapp.forms import registrationForm, loginForm, updateForm
from reapp.models import User
from flask_login import login_user, current_user, logout_user, login_required
import pandas as pd
import sqlite3

conn = sqlite3.connect("FinalDB.db")

houseData = pd.read_sql_query(
    "SELECT REAL_ESTATE.UNIQUE_RE_NUMBER, ADDRESS.ADDRSS, ADDRESS.LOCATION, PRICE.RE_PRICE, INFORMATION.RE_INFO FROM REAL_ESTATE INNER JOIN ADDRESS, PRICE, INFORMATION ON REAL_ESTATE.TYP_ID=1 AND REAL_ESTATE.ID=ADDRESS.RE_ID AND REAL_ESTATE.ID=PRICE.RE_ID AND REAL_ESTATE.ID=INFORMATION.RE_ID",
    conn)
flatsData = pd.read_sql_query(
    "SELECT REAL_ESTATE.UNIQUE_RE_NUMBER, ADDRESS.ADDRSS, ADDRESS.LOCATION, PRICE.RE_PRICE, INFORMATION.RE_INFO FROM REAL_ESTATE INNER JOIN ADDRESS, PRICE, INFORMATION ON REAL_ESTATE.TYP_ID=2 AND REAL_ESTATE.ID=ADDRESS.RE_ID AND REAL_ESTATE.ID=PRICE.RE_ID AND REAL_ESTATE.ID=INFORMATION.RE_ID",
    conn)
landsData = pd.read_sql_query(
    "SELECT REAL_ESTATE.UNIQUE_RE_NUMBER, ADDRESS.ADDRSS, ADDRESS.LOCATION, PRICE.RE_PRICE, INFORMATION.RE_INFO FROM REAL_ESTATE INNER JOIN ADDRESS, PRICE, INFORMATION ON REAL_ESTATE.TYP_ID=3 AND REAL_ESTATE.ID=ADDRESS.RE_ID AND REAL_ESTATE.ID=PRICE.RE_ID AND REAL_ESTATE.ID=INFORMATION.RE_ID",
    conn)
conn.close()


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/houses")
def houses():
    return render_template('houses.html', data=houseData)


@app.route("/flats")
def flats():
    return render_template('flats.html', data=flatsData)


@app.route("/lands")
def lands():
    return render_template('lands.html', data=landsData)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.rememberMe.data)
            nextPage = request.args.get('next')
            return redirect(nextPage) if nextPage else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please Check Email And Password.', 'danger')
    return render_template('login.html', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = registrationForm()
    if form.validate_on_submit():
        crypted_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=crypted_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


def savePicture(form_picture):
    randomHex = secrets.token_hex(8)
    fName, fExt = os.path.splitext(form_picture.filename)
    picFN = randomHex + fExt
    picPath = os.path.join(app.root_path, 'static/profilePics', picFN)
    form_picture.save(picPath)

    return picFN


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = updateForm()
    if form.validate_on_submit():
        if form.picture.data:
            pictureFile = savePicture(form.picture.data)
            current_user.profilePic = pictureFile
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    profilePic = url_for('static', filename='profilePics/' + current_user.profilePic)
    return render_template('account.html', title='Account',
                           profilePic=profilePic, form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/saved")
def saved():
    return render_template('saved.html')
