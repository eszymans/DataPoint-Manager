from flask import render_template

from app.extensions import db
from app.web.routes_web import app_blueprint


@app_blueprint.errorhandler(404)
def not_found_error():
    return render_template('error.html'), 404


@app_blueprint.errorhandler(500)
def internal_error():
    db.session.rollback()
    return render_template('error.html'), 500
