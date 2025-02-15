from django.contrib import admin

from exam_organization.models import Campus, Exam, Subject, SubjectUnit, Teacher


admin.site.register(Campus)
admin.site.register(Exam)
admin.site.register(Subject)
admin.site.register(SubjectUnit)
admin.site.register(Teacher)
