from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gibdd.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class PassportData(db.Model):
    __tablename__ = 'passport_data'
    passport_code = db.Column(db.Integer, primary_key=True)
    series = db.Column(db.String(120), nullable=False)
    number = db.Column(db.String(120), nullable=False)
    issued_who = db.Column(db.String(120))
    issued_when = db.Column(db.String(120), nullable=False)
    surname = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    patronymic = db.Column(db.String(120), nullable=False)
    residence = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<PassportData %r>' % self.passport_code


class Pts(db.Model):
    pts_code = db.Column(db.Integer, primary_key=True)
    passport_code = db.Column(db.Integer, nullable=False)
    vin_number = db.Column(db.String(120), nullable=False)
    series = db.Column(db.String(120), nullable=False)
    number = db.Column(db.String(120), nullable=False)
    issued_who = db.Column(db.String(120))

    def __repr__(self):
        return '<Pts %r>' % self.pts_code


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/pts')
def pts():
    pts = Pts.query.order_by(Pts.pts_code).all()
    return render_template('pts.html', pts=pts)


@app.route('/pts/add', methods=['POST', 'GET'])
def pts_add():
    if request.method == "POST":
        passport_code = request.form['passport_code']
        vin_number = request.form['vin_number']
        series = request.form['series']
        number = request.form['number']
        issued_who = request.form['issued_who']

        pts = Pts(passport_code=passport_code, vin_number=vin_number, series=series, number=number,
                           issued_who=issued_who)
        try:
            db.session.add(pts)
            db.session.commit()
            return redirect('/pts')
        except:
            return "При добавлении данных произошла ошибка"
    else:
        return render_template("pts_add.html")


@app.route('/pts/<int:pts_code>/delete')
def pts_delete(pts_code):
    pts = Pts.query.get_or_404(pts_code)

    try:
        db.session.delete(pts)
        db.session.commit()
        return redirect('/pts')
    except:
        return "При удалении произошла ошибка"


@app.route('/pts/<int:pts_code>/update', methods=['POST', 'GET'])
def pts_update(pts_code):
    pts = Pts.query.get(pts_code)
    if request.method == "POST":
        pts.passport_code = request.form['passport_code']
        pts.vin_number = request.form['vin_number']
        pts.series = request.form['series']
        pts.number = request.form['number']
        pts.issued_who = request.form['issued_who']

        try:
            db.session.commit()
            return redirect('/pts')
        except:
            return "При обновлении данных произошла ошибка"
    else:
        pts = Pts.query.get(pts_code)
        return render_template("pts_update.html", pts=pts)


@app.route('/passports')
def passports():
    passports = PassportData.query.order_by(PassportData.surname).all()
    return render_template('passports.html', show_passport_data=passports)


@app.route('/passports/add', methods=['POST', 'GET'])
def passports_add():
    if request.method == "POST":
        series = request.form['series']
        number = request.form['number']
        issued_who = request.form['issued_who']
        issued_when = request.form['issued_when']
        surname = request.form['surname']
        name = request.form['name']
        patronymic = request.form['patronymic']
        residence = request.form['residence']

        passport = PassportData(series=series, number=number, issued_who=issued_who, issued_when=issued_when,
                                surname=surname, name=name, patronymic=patronymic, residence=residence)
        try:
            db.session.add(passport)
            db.session.commit()
            return redirect('/passports')
        except:
            return "При добавлении данных произошла ошибка"
    else:
        return render_template("passports_add.html")


@app.route('/passports/<int:passport_code>/delete')
def passports_delete(passport_code):
    passport = PassportData.query.get_or_404(passport_code)

    try:
        db.session.delete(passport)
        db.session.commit()
        return redirect('/passports')
    except:
        return "При удалении произошла ошибка"


@app.route('/passports/<int:passport_code>/update', methods=['POST', 'GET'])
def passports_update(passport_code):
    passport = PassportData.query.get(passport_code)
    if request.method == "POST":
        passport.series = request.form['series']
        passport.number = request.form['number']
        passport.issued_who = request.form['issued_who']
        passport.issued_when = request.form['issued_when']
        passport.surname = request.form['surname']
        passport.name = request.form['name']
        passport.patronymic = request.form['patronymic']
        passport.residence = request.form['residence']

        try:
            db.session.commit()
            return redirect('/passports')
        except:
            return "При обновлении данных произошла ошибка"
    else:
        passport = PassportData.query.get(passport_code)
        return render_template("passports_update.html", show_passport_data=passport)


if __name__ == '__main__':
    app.run(debug=True)
