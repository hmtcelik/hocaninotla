from django.contrib import admin
from .models import Uni, Faculty, Depart, Doctor, Comment


admin.site.register(Uni)
admin.site.register(Faculty)
admin.site.register(Depart)
admin.site.register(Doctor)
admin.site.register(Comment)