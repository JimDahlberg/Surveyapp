from flask import render_template, url_for, flash, redirect, request
from surveyapp import app, db, bcrypt
from surveyapp.models import Employees, Accounts, HashTable, Surveys, Responses
from surveyapp.forms import RegistrationForm, LoginForm, CreateForm, AskForm, ResponseForm
from flask_login import login_user, current_user, logout_user, login_required
import datetime


@app.route("/")
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/survey', methods=['GET', 'POST'])
@login_required
def survey():
    surveyList = Surveys.query.filter_by(
        participantId=Employees.query.get(current_user.id).depId).all().copy()
    for survey in surveyList:
        if survey.endDate.date() < datetime.date.today():
            surveyList.pop(surveyList.index(survey))
    print(surveyList)
    return render_template('survey.html', title='Surveys', surveyList=surveyList)


@app.route('/ask', methods=['GET', 'POST'])
@login_required
def ask():
    form = AskForm()
    issuer = Employees.query.get(
        current_user.id).firstName + ' ' + Employees.query.get(current_user.id).lastName
    if form.validate_on_submit():
        question = Surveys(surveyTitle=form.surveyTitle.data, issuer=issuer,
                           startDate=datetime.datetime.now(), endDate=form.endDate.data,
                           question=form.surveyQuestion.data, participantId=form.participantId.data)
        db.session.add(question)
        db.session.commit()

        return redirect(url_for('home'))
    return render_template('ask.html', title='Ask', form=form)


@app.route('/answer/<int:surveyId>', methods=['GET', 'POST'])
@login_required
def answer(surveyId):
    question = Surveys.query.get(surveyId).question
    form = ResponseForm()
    if form.validate_on_submit():
        response = Response(surveyId=surveyId, respondent=current_user.id,
                            timeStamp=datetime.datetime.now(), response=form.response.data)

        db.session.add(response)
        db.session.commit()

        return redirect(url_for('home'))
    return render_template('answer.html', title='Survey+{}'.format(surveyId), form=form, question=question)


@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashedPassword = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        accountInfo = HashTable(username=form.username.data,
                                email=form.email.data, password=hashedPassword)
        db.session.add(accountInfo)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@ app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        email = HashTable.query.filter_by(email=form.email.data).first()
        if email and bcrypt.check_password_hash(email.password, form.password.data):
            login_user(email, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@ app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@ app.route("/settings")
@ login_required
def settings():
    return render_template('settings.html', title='Settings')


@ app.route("/create", methods=['GET', 'POST'])
def create():
    form = CreateForm()
    if form.validate_on_submit():
        hashString = form.firstName.data + form.lastName.data
        hashedEmpId = bcrypt.generate_password_hash(
            hashString).decode('utf-8')
        emp = Employees(depId=form.depId.data, firstName=form.firstName.data,
                        lastName=form.lastName.data, empHash=hashedEmpId)

        db.session.add(emp)
        db.session.commit()
        empId = Employees.query.filter_by(empHash=hashedEmpId).first().id
        acc = Accounts(empId=empId, accountLevel=form.accountLevel.data)
        db.session.add(acc)
        db.session.commit()
        print(emp, acc)
        flash('Employee {}, {} is now added!'.format(
            form.firstName.data, form.lastName.data), 'success')
        return redirect(url_for('home'))
    return render_template('create.html', title='Create Employee', form=form)
