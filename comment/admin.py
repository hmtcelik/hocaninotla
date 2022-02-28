from django.contrib import admin
from .models import Uni, Faculty, Depart, Doctor, Comment, CommentAnswer, ReportComment


class CommentAdmin(admin.ModelAdmin):
    list_filter = ('date_time',) #bu yana filter ekliyor
    list_display = ('comment_author','doctor','net_like','date_time',) # bu da kolon ve satir olarak orda cok guzel gosteriyor
    search_fields = ("comment_author__startswith",)    
    
class CommentAnswerAdmin(admin.ModelAdmin):
    list_filter = ('date_time',)
    list_display = ('answer_author','comment','date_time',)
    search_fields = ("answer_author__startswith",)

    
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('doctor_name','depart')
    search_fields = ("doctor_name__startswith",)

class ReportCommentAdmin(admin.ModelAdmin):
    list_filter = ('date_time',)
    list_display = ('report_author','comment','date_time',)
    search_fields = ("report_author__startswith",)


admin.site.register(Uni)
admin.site.register(Faculty)
admin.site.register(Depart)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(CommentAnswer, CommentAnswerAdmin)
admin.site.register(ReportComment, ReportCommentAdmin)

