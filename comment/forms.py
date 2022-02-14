from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import  Comment , RATE_CHOICES


# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user


class RateForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('comment_author', 'comment_body', 'rate')
        
    def save(self, commit=True):
        obj = super(RateForm, self)
        if commit:
            obj.save()
        return obj