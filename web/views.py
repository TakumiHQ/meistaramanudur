# encoding=utf-8

import os
import datetime

from flask import Blueprint, jsonify, render_template, request
from mailchimp import Mailchimp
from sqlalchemy.sql.expression import extract

from .models import Applicant
from .extensions import db

mailchimp = Mailchimp(os.environ['MAILCHIMP_API_KEY'])
views = Blueprint('views', __name__)


@views.route('/')
def index():
    return render_template('index.html')


@views.route('/signup', methods=["POST"])
def signup():

    data = request.form.to_dict()
    newcomer = not bool(data.pop("oldie", False))
    try:
        age = int(data.pop("age"))
    except ValueError:
        age = None

    applicant = Applicant(age=age, newcomer=newcomer, **data)
    db.session.add(applicant)
    db.session.commit()

    mailchimp.lists.subscribe(
        '493cdb0d3b',
        {'email': applicant.email.lower()},
        {'NAME': applicant.name, 'OLD': "No" if newcomer else "Yes"},
        email_type='html',
        update_existing=True,
        double_optin=False,
    )

    applicants_this_year = Applicant.query.filter(
        extract('year', Applicant.created) == datetime.datetime.now().year)
    return jsonify(number=applicants_this_year.count())


@views.route('/en')
def english():
    return render_template('english.html')
