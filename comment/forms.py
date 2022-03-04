from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe #for like using <strong> on labels 

from .models import  Comment , RATE_CHOICES, CommentAnswer, ReportComment, GRADE_CHOICES, ONLINE_CLASS_CHOICES, ATTANDANCE_CHOICES, TAKE_AGAIN_CHOICES


# Create your forms here.

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        labels = {
            "username": "Kullanici Adi",
            "email": "Mail",
            "password1": "Parola",
            "password2": "Tekrar Parola",
        }
    def save(self, commit=True):
            user = super(NewUserForm, self).save(commit=False)
            user.email = self.cleaned_data['email']
            if commit:
                user.save()
            return user    


class RateForm(forms.ModelForm): #comment create

    class Meta:
        model = Comment
        exclude = ['comment_author', 'likes', 'total_likes', 'total_answers', 'date_time', 'net_like']        
        fields = ('rate','comment_body', 'take_again','attandance','online_class','grade','anonymous')
        labels = {
            "comment_body": mark_safe("<strong>Yorum</strong>"),
            "rate": mark_safe("<strong>Verdiğim Not</strong>"),
            "take_again": mark_safe("<strong>Tekrar Alır mısın</strong>"),
            "attandance": mark_safe("<strong>Devamlılık</strong>"),
            "online_class": mark_safe("<strong>Eğitim Şekli</strong>"),
            "grade": mark_safe("<strong>Harf Notum</strong>"),
            "anonymous":mark_safe("<strong>İsmim Gözükmesin</strong>"),
        }
        widgets = {
            'rate': forms.Select(attrs={'class':'ud-form-group'}),
            'comment_body': forms.Textarea(attrs={'class':'ud-form-group comment-box','placeholder': ("bişeyler yaz")}),
            'take_again': forms.Select(attrs={'class':'ud-form-group'}),
            'attandance': forms.Select(attrs={'class':'ud-form-group'}),
            'online_class': forms.Select(attrs={'class':'ud-form-group'}),
            'grade': forms.Select(attrs={'class':'ud-form-group'}),
            'anonymous': forms.CheckboxInput(attrs={'class':'ud-form-group annon'}),            
        }
        
    def save(self, commit=True):
        obj = super(RateForm, self)
        if commit:
            obj.save()
        return obj

class CommentAnswerForm(forms.ModelForm):
    
    class Meta:
        model = CommentAnswer
        exclude = ['answer_author']
        fields = ('answer_body',)
        labels = {
            "answer_body": mark_safe("<strong>Yanıt</strong>"),
        }
        widgets = {
            'answer_body': forms.Textarea(attrs={'class':'ud-form-group comment-box','placeholder': ("bişeyler yaz")}),       
        }
        
    def save(self, commit=True):
        answer = super(CommentAnswerForm, self)
        if commit:
            answer.save()
        return answer
    
class ReportForm(forms.ModelForm):
    class Meta:
        model = ReportComment
        exclude = ['report_author',]
        fields = ('report_body',)
        labels = {
            "report_body": mark_safe("<strong>Şikayetim</strong>"),
        }
        widgets = {
            'report_body': forms.Textarea(attrs={'class':'ud-form-group comment-box','placeholder': ("bişeyler yaz")}),       
        }
        
    def save(self, commit=True):
        report = super(ReportForm, self)
        if commit:
            report.save()
        return report