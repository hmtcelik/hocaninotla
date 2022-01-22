from django.contrib import admin
from .models import City, University, Faculty, Departmant, Doctor, Comment

# Register your models here.

admin.site.register(City)
admin.site.register(University)
admin.site.register(Faculty)
admin.site.register(Departmant)
admin.site.register(Doctor)
admin.site.register(Comment)

