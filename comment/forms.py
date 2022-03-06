from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe #for like using <strong> on labels 

from .models import  Comment , RATE_CHOICES, CommentAnswer, ReportComment, GRADE_CHOICES, ONLINE_CLASS_CHOICES, ATTANDANCE_CHOICES, TAKE_AGAIN_CHOICES


# Create your forms here.
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class':'ud-formm-group',}),label= mark_safe('<strong>Kullanıcı Adı</strong>'))
    password = forms.CharField(strip=False,widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class':'ud-formm-group'}),label=mark_safe('<strong>Şifre</strong>'))


class NewUserForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label=mark_safe('<strong>Email</strong>'),
        widget=forms.TextInput(attrs={'class':'ud-formm-group'}),
        )
    password1 = forms.CharField(
        label= mark_safe('<strong>Şifre</strong>'),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'ud-formm-group'}),
        help_text= mark_safe("<div style='padding:5px 5px; margin-top:-5px;'>En az 8 karakter içermelidir<br>Sadece sayılardan oluşmamalıdır</div><br>"),
    )
    password2 = forms.CharField(
        label= mark_safe('<strong>Şifre Tekrar</strong>'),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'ud-formm-group'}),
        strip=False,
    )
    
    class Meta:
        model = User
        fields = ("username",)
        labels = {
            "username": mark_safe('<strong>Kullanıcı Adı</strong>'),
        }
        widgets={
            'username': forms.TextInput(attrs={'class':'ud-formm-group',}),
            }
        help_texts={
            'username': ''
        }
    def save(self, commit=True):
            user = super(NewUserForm, self).save(commit=False)
            user.email = self.cleaned_data['email']
            print(user)
            if commit:
                user.save()
            return user    

    field_order = ['username', 'email', 'password1', 'password2',]

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
    
