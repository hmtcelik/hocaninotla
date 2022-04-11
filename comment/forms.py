from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe #for example; using <strong> on labels 
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError  

from django.contrib.auth import forms as auth_forms #django password forgetting things forms

from .models import  Comment , RATE_CHOICES, CommentAnswer, ReportComment, GRADE_CHOICES, ONLINE_CLASS_CHOICES, ATTANDANCE_CHOICES, TAKE_AGAIN_CHOICES, BannedEmails
from .models import Requests, DoctorRequests

# Create your forms here.
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class':'ud-formm-group',}),label= mark_safe('<strong>Kullanıcı Adı</strong>'))
    password = forms.CharField(strip=False,widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class':'ud-formm-group'}),label=mark_safe('<strong>Şifre</strong>'))

        
class PasswordsResetForm(auth_forms.PasswordResetForm):
    email = forms.EmailField(
        required=True,
        label=mark_safe('<strong>Email</strong>'),
        widget=forms.TextInput(attrs={'class':'ud-formm-group'}),
        )

class PasswordsConfirmForm(auth_forms.SetPasswordForm):
    new_password1 = forms.CharField(
        label= mark_safe('<strong>Yeni Şifre</strong>'),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'ud-formm-group'}),
        strip=False,
        help_text= mark_safe("<div style='padding:5px 5px; margin-top:-5px;'>En az 8 karakter içermelidir<br>Sadece sayılardan oluşmamalıdır</div><br>"),
    )
    new_password2 = forms.CharField(
        label= mark_safe('<strong>Tekrar Yeni Şifre</strong>'),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'ud-formm-group'}),
    )
    

class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(
        max_length=100,
        label=mark_safe('<strong>Eski Şifre</strong>'),
        widget=forms.PasswordInput(attrs={'autocomplete': 'off', 'class':'ud-formm-group'}),
        )
    new_password1 = forms.CharField(
        max_length=100,        
        label= mark_safe('<strong>Yeni Şifre</strong>'),
        widget=forms.PasswordInput(attrs={'autocomplete': 'off','class':'ud-formm-group'}),
        help_text= mark_safe("<div style='padding:5px 5px; margin-top:-5px;'>En az 8 karakter içermelidir<br>Sadece sayılardan oluşmamalıdır</div><br>"),        
    )
    new_password2 = forms.CharField(
        max_length=100,
        label= mark_safe('<strong>Tekrar Yeni Şifre</strong>'),
        widget=forms.PasswordInput(attrs={'autocomplete': 'off','class':'ud-formm-group'}),
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

class NewUserForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label=mark_safe('<strong>Email</strong>'),
        widget=forms.TextInput(attrs={'class':'ud-formm-group'}),
        help_text= mark_safe("<div style='padding:5px 5px; margin-top:-5px;'>Yalnızca üniversite e-postanız ile kayıt olabilirsiniz</div><br>"),
        )
    password1 = forms.CharField(
        label= mark_safe('<strong>Şifre</strong>'),
        max_length=100,        
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'ud-formm-group'}),
        help_text= mark_safe("<div style='padding:5px 5px; margin-top:-5px;'>En az 8 karakter içermelidir<br>Sadece sayılardan oluşmamalıdır</div><br>"),
    )
    password2 = forms.CharField(
        max_length=100,        
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
            'username': ""
        }

    def clean_username(self):
        super(NewUserForm, self).clean()
        username = self.cleaned_data['username']
        if User.objects.exclude().filter(username=username).exists():
            raise forms.ValidationError(mark_safe("<span style='color:red;margin-bottom:15px;'>Bu kullanici adi zaten kullaniliyor</span>"))
        if ' ' in username:
            raise forms.ValidationError(mark_safe("<span style='color:red;margin-bottom:15px;'>Boşluk içermemelidir.( _ kullanabilirsiniz)</span>"))
        
        return username

    def clean_password2(self): 
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError(mark_safe("<span style='color:red;margin-bottom:15px;'>Şifreler birbirleriyle uyuşmuyor</span>"))  
        
        return password2
    
    def clean_email(self):  
        email = self.cleaned_data['email']
        new = User.objects.filter(email=email)  
        if 'edu.tr' not in email:
            raise ValidationError(mark_safe("<span style='color:red;margin-bottom:15px;'>Lütfen geçerli bir e-posta giriniz</span>"))  
        if new.count():  
            raise ValidationError(mark_safe("<span style='color:red;margin-bottom:15px;'>Bu e-posta zaten kullaniliyor</span>"))  
        banned = BannedEmails.objects.filter(email=email)
        if banned.count():
            raise ValidationError(mark_safe("<span style='color:red;margin-bottom:15px;'>Bu e-posta adresi zaten kullaniliyor</span>"))  
    
        return email
    
    def save(self, commit=True):
            user = super(NewUserForm, self).save(commit=False)
            user.email = self.cleaned_data['email']
            if commit:
                user.save()
            return user    

    field_order = ['username', 'email', 'password1', 'password2',]

class RateForm(forms.ModelForm): #comment create

    class Meta:
        model = Comment
        exclude = ['comment_author', 'likes', 'total_likes', 'total_answers', 'date_time', 'net_like','comment_author_id']        
        fields = ('rate','comment_body', 'take_again','attandance','online_class','grade','anonymous')
        labels = {
            "comment_body": mark_safe("<strong>Yorum</strong>"),
            "rate": mark_safe("<strong>Verdiğim Not</strong>"),
            "take_again": mark_safe("<strong>Tekrar Alır mıydın</strong>"),
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
    
class RequestsForm(forms.ModelForm):
    class Meta:
        model = Requests
        exclude = ['request_author',]
        fields = ('request_body',)
        labels = {
            "request_body": mark_safe("<strong>İstek ve Önerim</strong>"),
        }
        widgets = {
            'request_body': forms.Textarea(attrs={'class':'ud-form-group comment-box','placeholder': ("bişeyler yaz")}),       
        }
        
    def save(self, commit=True):
        request = super(RequestsForm, self)
        if commit:
            request.save()
        return request

class DoctorRequestForm(forms.ModelForm):
    class Meta:
        model = DoctorRequests
        exclude = ['request_author',]
        fields = ('doctor_name','uni_name','faculty_name','depart_name','doctor_lecture')
        labels = {
            "doctor_name": mark_safe("<strong>Adı ve Soyadı</strong>"),
            "uni_name": mark_safe("<strong>Üniversitesi</strong>"),
            "faculty_name": mark_safe("<strong>Fakültesi</strong>"),
            "depart_name": mark_safe("<strong>Departmanı</strong>"),
            "doctor_lecture": mark_safe("<strong>Alanı(Ders)</strong>"),
        }
        widgets = {
            'uni_name': forms.TextInput(attrs={'class':'ud-form-group comment-box',}),
            'faculty_name': forms.TextInput(attrs={'class':'ud-form-group comment-box',}),    
            'depart_name': forms.TextInput(attrs={'class':'ud-form-group comment-box',}),    
            'doctor_name': forms.TextInput(attrs={'class':'ud-form-group comment-box',}),    
            'doctor_lecture': forms.TextInput(attrs={'class':'ud-form-group comment-box',}),
        }
        
    def save(self, commit=True):
        doc_request = super(DoctorRequestForm, self)
        if commit:
            doc_request.save()
        return doc_request