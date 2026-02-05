from flask import Blueprint, render_template, request, redirect, url_for

from app.extensions import db
from app.models import DataPoint

app_blueprint = Blueprint('main', __name__)


@app_blueprint.route('/')
def index():
    data = DataPoint.query.all()
    return render_template('index.html', data_points=data)


@app_blueprint.route('/add', methods=['GET', 'POST'])
def add_point():
    if request.method == 'POST':
        try:
            f1 = float(request.form['weight'])
            f2 = float(request.form['height'])
            cat = int(request.form['category'])

            new_point = DataPoint(weight=f1, height=f2, category=cat)
            db.session.add(new_point)
            db.session.commit()

            return redirect(url_for('main.index'))

        except (ValueError, KeyError):
            return render_template('error.html',
                                   code=400,
                                   message="Invalid data provided. "
                                           "Please enter numbers."), 400

    return render_template('add_form.html')


@app_blueprint.route('/delete/<int:record_id>', methods=['POST'])
def delete_point(record_id):
    point = DataPoint.query.get(record_id)

    if point:
        db.session.delete(point)
        db.session.commit()
        return redirect(url_for('main.index'))
    else:
        return render_template('error.html',
                               code=404,
                               message="Record not found in the "
                                       "database."), 404
