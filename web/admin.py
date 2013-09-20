from flask.ext.admin.contrib import sqlamodel

from .models import Applicant
from .extensions import admin, db

admin.add_view(sqlamodel.ModelView(Applicant, db.session))
