from surveyapp import db, loginManager
from flask_login import UserMixin


@loginManager.user_loader
def load_user(user_id):
    return HashTable.query.get(int(user_id))

#module where the tablles in the database are created
class Employees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    depId = db.Column(db.String(5),  nullable=False)
    firstName = db.Column(db.String(20), nullable=False)
    lastName = db.Column(db.String(20), nullable=False)
    empHash = db.Column(db.String(60), nullable=False)
    accounts = db.relationship('Accounts', backref='account', lazy=True)
    surveys = db.relationship('Surveys', backref='survey', lazy=True)
    responses = db.relationship('Responses', backref='response', lazy=True)

    def __repr__(self):
        return 'Employee({}, {}, {}, {})'.format(self.firstName, self.lastName, self.depId, self.empHash)


class Accounts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    empId = db.Column(db.Integer, db.ForeignKey(
        'employees.id'), nullable=False)
    accountLevel = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return 'Account({}, {})'.format(self.empId, self.accountLevel)


class HashTable(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return 'HashTable({}, {}, {})'.format(self.username, self.email, self.password)


class Surveys(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    surveyTitle = db.Column(db.Text, nullable=False)
    issuer = db.Column(db.Integer, db.ForeignKey(
        'employees.id'), nullable=False)
    startDate = db.Column(db.DateTime, nullable=False)
    endDate = db.Column(db.DateTime, nullable=False)
    question = db.Column(db.Text, nullable=False)
    participantId = db.Column(db.String(5),  nullable=False)

    def __repr__(self):
        return 'Survey({}, {}, {}, {}, {}, {})'.format(self.surveyTitle, self.issuer, self.startDate,
                                                       self.endDate, self.question, self.participantId)


class Responses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    surveyId = db.Column(db.Integer, db.ForeignKey(
        'surveys.id'), nullable=False)
    respondent = db.Column(db.Integer, db.ForeignKey(
        'employees.id'), nullable=False)
    timeStamp = db.Column(db.DateTime, nullable=False)
    response = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return 'Response({}, {}, {}, {})'.format(self.surveyId, self.respondent, self.timeStamp, self.response)
