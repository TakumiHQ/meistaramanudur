from flask.ext.admin.contrib import sqlamodel

from .models import Applicant
from .extensions import admin, db

class ApplicantModelView(sqlamodel.ModelView):
    column_searchable_list = ('name', 'email')
    column_filters = ('newcomer', )

admin.add_view(ApplicantModelView(Applicant, db.session))
