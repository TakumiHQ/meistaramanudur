from .extensions import db

from sqlalchemy import func

class Applicant(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, server_default=func.now())

    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone = db.Column(db.String)
    newcomer = db.Column(db.Boolean, default=False)
    blog_url = db.Column(db.String)
    age = db.Column(db.Integer)
    instagram = db.Column(db.String)
