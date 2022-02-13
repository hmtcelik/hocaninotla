from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Comment , RATE_CHOICES


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
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'materialize-texarea'}), required=False)
    rate = forms.ChoiceField(choices=RATE_CHOICES, widget=forms.Select(), required=True)
    
    class Meta:
        model = Comment
        fields = ('comment_author','comment_body','rate')