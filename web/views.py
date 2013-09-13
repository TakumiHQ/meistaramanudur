# encoding=utf-8

import os
from flask import Blueprint, jsonify, render_template, request, abort
from mailchimp import Mailchimp, Error as MailchimpError

from .models import Applicant
from .extensions import db

mailchimp = Mailchimp(os.environ['MAILCHIMP_API_KEY'])
views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('index.html')

@views.route('/signup', methods=["POST"])
def signup():

    """
    try:
        mailchimp.subscribe(
            '493cdb0d3b',
            request.json['email'],
            email_type='html',
            update_existing=True
        )
    except MailchimpError, e:
        return jsonify(message=str(e)), 403
    """

    data = request.form.to_dict()
    newcomer = bool(data.pop("newbie", False))
    blog_url = data.pop("blog")
    try:
        age = int(data.pop("age"))
    except ValueError:
        age = None

    applicant = Applicant(age=age, blog_url=blog_url, newcomer=newcomer, **data)
    db.session.add(applicant)
    db.session.commit()

    return jsonify(number=Applicant.query.count())
