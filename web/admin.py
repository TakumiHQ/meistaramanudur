import csv
import cStringIO as StringIO
from flask.ext.admin.contrib import sqlamodel
from flask.ext.admin.actions import action

from .models import Applicant
from .extensions import admin, db

class ApplicantModelView(sqlamodel.ModelView):
    column_searchable_list = ('name', 'email')
    column_filters = ('newcomer', )

    @action('download', 'Download')
    def download_csv(self, ids):
        output = StringIO.StringIO()
        csvf = csv.writer(output)
        for a in Applicant.query.order_by(Applicant.created):
            row = [str(a.id), a.created.isoformat(), a.name, a.blog_url, str(int(a.newcomer)), a.age, a.instagram, a.phone, a.email]
            row = map(lambda s: unicode(s).encode('utf-8') if s else '', row)
            csvf.writerow(row)
        contents = output.getvalue()
        output.close()
        return contents, 200, {
            'Content-Disposition': 'attachment; filename="gcm-skraningar.csv"',
            'Content-Type': 'text/csv'
        }

admin.add_view(ApplicantModelView(Applicant, db.session))
