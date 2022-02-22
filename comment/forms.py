from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import  Comment , RATE_CHOICES, CommentAnswer


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


class RateForm(forms.ModelForm): #comment create


    class Meta:
        model = Comment
        exclude = ['comment_author', 'likes', 'total_likes', 'total_answers', 'date_time']        
        fields = ('comment_body', 'rate', 'anonymous')
        
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
        
    def save(self, commit=True):
        answer = super(CommentAnswerForm, self)
        if commit:
            answer.save()
        return answer