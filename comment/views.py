from django.views import generic
from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import PasswordChangeView

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.db.models import Avg, Count
from django.template import RequestContext
import re

from django.contrib.auth import views as auth_views #django password forgetting things views
from django.contrib.auth import forms as auth_forms #django password forgetting things forms

# password resetting (forget password
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

from django.core.exceptions import PermissionDenied #for raise 404 errror on 'pagenotfound_view'

from sinkaf import Sinkaf #kufur engelleyici

from . import forms as my_forms # all my forms using with; my_forms.ExampleForm

from .forms import NewUserForm, RateForm, CommentAnswerForm, ReportForm, LoginForm, PasswordChangingForm, PasswordsResetForm
from .models import Uni , Faculty, Depart, Doctor, Comment, CommentAnswer, ReportComment
from django.contrib.auth.models import User


# Searchbar func.
def searchbar(request):
    if request.method == "GET":
        search = request.GET.get('search')
        if not search or search == "":
            return HttpResponseRedirect(reverse('comment:home'))
        else:                
            post2 = Doctor.objects.all().filter(doctor_name__contains=search)
            all_results = post2.count()
            context = {'post2' : post2, 'all_results':all_results}
            return render(request, 'searchbar.html', context)

class HomeView(generic.TemplateView):
    template_name = 'index.html'

class UniView(generic.ListView):
    template_name = 'uni.html'
    context_object_name = 'all_unis'
    
    def get_queryset(self):
        return Uni.objects.all()
    
    
class FacultyView(generic.DetailView):
    model = Uni
    template_name = 'faculty.html'
    
     
class DepartView(generic.DetailView):
    model = Faculty
    template_name = 'depart.html'
    
    
class DoctorView(generic.DetailView):
    model = Depart
    template_name = 'doctor.html'
    
class AddDoctorView(generic.TemplateView):
    template_name = 'adddoctor.html'
    
class AccountView(generic.TemplateView):
    template_name = 'account/account_index.html'

    
class ContactView(generic.TemplateView):
    template_name = 'contact.html'

class MyCommentsView(generic.TemplateView):
    template_name = 'account/mycomments.html'
    
    def get_context_data(self, **kwargs):
        context = super(MyCommentsView, self).get_context_data(**kwargs)
        
        user_id = self.request.user.id
        
        comments = Comment.objects.all().filter(comment_author_id=user_id)
        
        all_results = comments.count()
        
        arg = {
            'comments':comments,
            'all_results':all_results,    
        }
          
        context.update(arg)
        return context
    

    
class CommentView(generic.DetailView):
    model = Doctor
    template_name = 'comment.html'

    def get_context_data(self, **kwargs): #burda degiskeni context dataya atip gidip templatesde direk ismiyle kullanabiliyoz
        context = super(CommentView, self).get_context_data(**kwargs)

        #------ avarage rates of doctors -----------------
        doctor = get_object_or_404(Doctor, id=self.kwargs['pk'])
        #no = numberof
        noAllRates = Comment.objects.filter(doctor = doctor).count()
        noRate1 = Comment.objects.filter(doctor = doctor, rate=1.0).count()
        noRate2 = Comment.objects.filter(doctor = doctor, rate=2.0).count()
        noRate3 = Comment.objects.filter(doctor = doctor, rate=3.0).count()
        noRate4 = Comment.objects.filter(doctor = doctor, rate=4.0).count()
        noRate5 = Comment.objects.filter(doctor = doctor, rate=5.0).count()
        
        if noAllRates != 0:
            av_rates = ((noRate1 * 1) + (noRate2 * 2) + (noRate3 * 3) + (noRate4 * 4) + (noRate5 * 5)) / noAllRates
            av_rates = round(av_rates, 1)
        else:
            av_rates = 0.0
            
        doctor.doctor_av_rate = av_rates
        
        #-----------------------------------------------


        all_comments = Comment.objects.filter(doctor=doctor).count() #number of all comments
        
        doctor.doctor_total_rate = noAllRates

        # START FOR DOCTOR RATE SCORECARDS EACH VOTE -------------------------------------------
        colorwidth_rate1 = 0 
        colorwidth_rate2 = 0
        colorwidth_rate3 = 0
        colorwidth_rate4 = 0
        colorwidth_rate5 = 0

        rate_list = [noRate1,noRate2,noRate3,noRate4,noRate5]
        
        max_rate = max(rate_list)


        if max_rate != 0:
            each_vote = 100/max_rate # this is for each vote equal how much power
            colorwidth_rate1 = noRate1 * each_vote
            colorwidth_rate2 = noRate2 * each_vote
            colorwidth_rate3 = noRate3 * each_vote
            colorwidth_rate4 = noRate4 * each_vote
            colorwidth_rate5 = noRate5 * each_vote                

        if max_rate == 1:
            each_vote = 50
            colorwidth_rate1 = noRate1 * each_vote
            colorwidth_rate2 = noRate2 * each_vote
            colorwidth_rate3 = noRate3 * each_vote
            colorwidth_rate4 = noRate4 * each_vote
            colorwidth_rate5 = noRate5 * each_vote                  

        if noRate1 == noRate2:
            if noRate1 == noRate3:
                if noRate1 == noRate4:                     
                    if noRate1 == noRate5:
                        colorwidth_rate1 = 50
                        colorwidth_rate2 = 50
                        colorwidth_rate3 = 50
                        colorwidth_rate4 = 50
                        colorwidth_rate5 = 50
        
        if noRate1 == 0:
            colorwidth_rate1 = 0
        if noRate2 == 0:
            colorwidth_rate2 = 0
        if noRate3 == 0:
            colorwidth_rate3 = 0
        if noRate4 == 0:
            colorwidth_rate4 = 0
        if noRate5 == 0:
            colorwidth_rate5 = 0
        #-------------------------------------------------------------------------------

        # ---------- if user did comment this doctor, not allowed second comment -------------------------
        user_id = self.request.user.id
        user_comment_id = 0
        already_rated = 0
        
        if user_id != None:
            comments_of_this_user = Comment.objects.filter(doctor=doctor, comment_author_id=user_id) #also this doctor
            if comments_of_this_user:
                already_rated = 1
            else:
                already_rated = 0
            

            check_comment = Comment.objects.filter(doctor=doctor, comment_author_id=user_id)
            if check_comment:
                comment = get_object_or_404(Comment, doctor=doctor, comment_author_id=user_id)
                user_comment_id = comment.id

        
        #----------------------------------------------------------------------------

        arg = {'av_rates': av_rates,
               'rates1': noRate1,
               'rates2': noRate2,
               'rates3': noRate3,
               'rates4': noRate4,
               'rates5': noRate5,
               'all_comments': all_comments,
               'colorwidth_rate1': colorwidth_rate1,
               'colorwidth_rate2': colorwidth_rate2,
               'colorwidth_rate3': colorwidth_rate3,
               'colorwidth_rate4': colorwidth_rate4,
               'colorwidth_rate5': colorwidth_rate5,
               'already_rated' : already_rated,
               'user_comment_id':user_comment_id,
               'user_id': user_id,
               }
        doctor.save()
        context.update(arg)
        return context

#comment like button
def likeview(request, doctor_id, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=request.POST.get('comment_id'))
        user = request.user
        okay = 0
        disliked = 0
        
        for i in comment.likes.all():  #check if user like this post ? (if is , like will delete at line 117)
            if i == user:
                okay = True
                break

        if okay:   
            comment.likes.remove(user)
        else:
            comment.likes.add(user)
            for a in comment.dislikes.all(): #check all dislikes for if the user liked the comment, will delete his dislike
                if a == user:
                    disliked = True
                    break
            if disliked:
                comment.dislikes.remove(user)

        comment.net_like = (comment.likes.count()) - (comment.dislikes.count())
        comment.total_likes = comment.likes.count()
        comment.total_dislikes = comment.dislikes.count()    
        comment.save()

        data = {
            'likes': comment.total_likes
        }
        return JsonResponse(data, safe=False)
        
    return HttpResponseRedirect(reverse('comment:comment', args=[str(doctor_id)]))
    
#comment dislike button
def dislikeview(request, doctor_id, comment_id):
    if request.method == 'POST':    
        comment = get_object_or_404(Comment, id=request.POST.get('comment_id'))
        user = request.user
        okay = 0
        liked = 0
        
        for i in comment.dislikes.all(): #check if user dislike this post ? (if is , dislike will delete at line 135)
            if i == user:
                okay = 1
                break
        if okay == 1:
            comment.dislikes.remove(user)
        else:
            comment.dislikes.add(user)
            for a in comment.likes.all(): #check all likes for when the user press dislike button , the site will delete the like if he is liked
                if a == user:
                    liked = 1
                    break
            if liked == 1:
                comment.likes.remove(user)
        
        comment.net_like = (comment.likes.count()) - (comment.dislikes.count())
        comment.total_likes = comment.likes.count()
        comment.total_dislikes = comment.dislikes.count()
        comment.save()
    
        data = {
            'dislikes': comment.total_dislikes
        }
        return JsonResponse(data, safe=False)
    
    return HttpResponseRedirect(reverse('comment:comment', args=[str(doctor_id)]))

class CommentCreate(generic.FormView):
    template_name = 'comment_add.html'
    form_class = RateForm
    snf = Sinkaf() #kufur engelliyici
    
    def get_success_url(self):
        return reverse('comment:comment', kwargs={'pk': self.kwargs.get('doctor_id') })

    def form_valid(self, form):
        form.save(commit=False)        
        form.instance.doctor_id = self.kwargs.get('doctor_id')
        form.instance.comment_author = self.request.user
        form.instance.comment_author_id = self.request.user.id
        doctor_id = self.kwargs.get('doctor_id')
    
        user_id = self.request.user.id
        
        doctor = get_object_or_404(Doctor, id=self.kwargs['doctor_id'])
        comments_of_this_user = Comment.objects.filter(doctor=doctor, comment_author_id=user_id) #also this doctor
        if comments_of_this_user:
            messages.error(self.request,"Zaten Not Vermissin, Tekrar Veremezsin!.")
            return HttpResponseRedirect(reverse('comment:createcomment', args=[str(doctor_id)]))
        
        if self.snf.tahmin([form.cleaned_data['comment_body']]):
            messages.error(self.request,"Yorumunda uygunsuz ifadeler bulunuyor.")
            return HttpResponseRedirect(reverse('comment:createcomment', args=[str(doctor_id)]))
            
        form.save()
        messages.success(self.request, "Yorumun Basariyla Kaydedildi." )
        
        return super().form_valid(form)

def commentdeleteview(request, doctor_id, comment_id):
    if request.method == 'POST':

        doctor = get_object_or_404(Doctor, id=doctor_id)
        user_id = request.user.id

        try:
            the_comment = Comment.objects.get(doctor=doctor_id, comment_author_id=user_id)            
        except Comment.DoesNotExist:
            the_comment = None
            
        if the_comment != None:
            the_comment.delete()
                            
            messages.success(request, "Yorumun Basariyla Silindi.")

    next = request.POST.get('next', '/')

        
    return HttpResponseRedirect(next)


    
def commenteditview(request, doctor_id, comment_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    user_id = request.user.id
    try:
        the_comment = Comment.objects.get(doctor=doctor_id, comment_author_id=user_id)
    except Comment.DoesNotExist:
        the_comment = None
    
    if the_comment != None:        
        update_form = RateForm(instance=the_comment)
  
        snf = Sinkaf() #kufur hakaret engelliyor
        
        if request.method == 'POST':
            update_form = RateForm(request.POST, instance=the_comment)
            if update_form.is_valid():
                if snf.tahmin([update_form.cleaned_data['comment_body']]):
                    messages.error(request,"Yorumunda uygunsuz ifadeler bulunuyor.")
                    return HttpResponseRedirect(reverse('comment:editcomment', args=[str(doctor_id),str(comment_id)]))
                
                update_form.save(commit=False)
                update_form.doctor_id = doctor_id
                update_form.comment_author = request.user
                update_form.comment_author_id = request.user.id

                update_form.save()
                messages.success(request, "Yorumun Basariyla Kaydedildi.")
            return HttpResponseRedirect(reverse('comment:comment', args=[str(doctor_id)]))
    
    else:
        return HttpResponseRedirect(reverse('comment:comment', args=[str(doctor_id)]))
        
            
    return render(request=request, template_name="comment_edit.html", context={"edit_form":update_form})
        

class CommentAnswerView(generic.FormView):
    template_name = 'comment_answering.html'
    form_class = CommentAnswerForm
    snf = Sinkaf() #kufur hakaret engelliyor

    def get_success_url(self):
        return reverse('comment:comment', kwargs={'pk': self.kwargs.get('doctor_id') })

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.comment_id = self.kwargs.get('comment_id')
        form.instance.answer_author = self.request.user       
        doctor_id = self.kwargs.get('doctor_id')
        comment_id = self.kwargs.get('comment_id')         
        if self.snf.tahmin([form.cleaned_data['answer_body']]):
            messages.error(self.request,"Yanitinizda uygunsuz ifadeler bulunuyor.")
            return HttpResponseRedirect(reverse('comment:commentanswer', args=[str(doctor_id),str(comment_id)]))

        form.save()
        messages.success(self.request, "Yanitiniz Basariyla Kaydedildi." )

        comment = get_object_or_404(Comment, id=self.kwargs.get('comment_id'))
        comment_answers = CommentAnswer.objects.filter(comment=comment_id)
        comment.total_answers = comment_answers.count() #number of total answers
        comment.save()
        
        return super().form_valid(form)

class ReportCommentView(generic.FormView):    
    template_name = 'comment_reporting.html'
    form_class = ReportForm
    snf = Sinkaf()
    
    def get_success_url(self):
        return reverse('comment:comment', kwargs={'pk': self.kwargs.get('doctor_id') })
        
    def form_valid(self, form):
        form.save(commit=False)
        form.instance.comment_id = self.kwargs.get('comment_id')
        form.instance.report_author = self.request.user
        doctor_id = self.kwargs.get('doctor_id')
        comment_id = self.kwargs.get('comment_id')   
        if self.snf.tahmin([form.cleaned_data['report_body']]):
            messages.error(self.request,"Sikayetinizde uygunsuz ifadeler bulunuyor.")
            return HttpResponseRedirect(reverse('comment:reportcomment', args=[str(doctor_id),str(comment_id)]))
        
        form.save()
        messages.success(self.request, "Sikayetiniz Bize Ulasmistir." )
        return super().form_valid(form)
    

#Login----->
def login_request(request):
	if request.method == "POST":
		form = LoginForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f" Hoşgeldin {username}.")
				return redirect("comment:home")
			else:
				messages.error(request,"Kullanıcı adı veya şifre yanlış")
		else:
			messages.error(request,"Kullanıcı adı veya şifre yanlış")
	form = LoginForm()
	return render(request=request, template_name="registration/login.html", context={"login_form":form})


#Logout----->
def logout_request(request):
	logout(request) 
	return redirect("comment:home")

#Register----->
def register_request(request):
    if request.method == "POST":
        snf = Sinkaf() #kufur hakaret engelliyor      
        form = NewUserForm(request.POST)
        if form.is_valid():
            if snf.tahmin([form.cleaned_data['username']]):
                messages.error(request,"Isminizde uygunsuz ifadeler var")
                return redirect("comment:register")
            user = form.save()
            messages.success(request, "Basariyla Kayit Olundu." )
            return redirect("comment:login")
    else:
        form = NewUserForm()
    return render (request=request, template_name="registration/register.html", context={"register_form":form})


class PasswordsChangeView(PasswordChangeView):
    form_class= PasswordChangingForm
    template_name='registration/changepassword.html'
    success_url= reverse_lazy('comment:changedpassword')

def passwordsuccesview(request):
    return render(request, template_name="registration/succes_changedpassword.html",context={})


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordsResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:    
                    subject = "Parola Sifirlama Istegi"
                    email_template_name = "registration/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain':'127.0.0.1:8000',
                        'site_name': 'Hocani Notla',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }   
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect ("comment:password_reset_done")     
            else:
                messages.error(request,"Bu E-posta ile ilişkin kullanıcı bulunamadı")

    password_reset_form = PasswordsResetForm()
    return render(request=request, template_name="registration/password_reset.html", context={"password_reset_form":password_reset_form})


class My_PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name='registration/password_reset_done.html'
    success_url = reverse_lazy('comment:password_reset_confirm')
    
class My_PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    form_class = my_forms.PasswordsConfirmForm
    template_name='registration/password_reset_confirm.html'
    success_url = reverse_lazy('comment:password_reset_complete')

class My_PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name='registration/password_reset_complete.html'
    success_url = reverse_lazy('comment:login')
    
class RequestFormView(generic.FormView):    
    template_name = 'requestform.html'
    form_class = my_forms.RequestsForm
    snf = Sinkaf()
    
    def get_success_url(self):
        return reverse_lazy('comment:home')
        
    def form_valid(self, form):
        form.save(commit=False)

        form.instance.request_author = self.request.user
   
        if self.snf.tahmin([form.cleaned_data['request_body']]):
            messages.error(self.request,"Sikayetinizde uygunsuz ifadeler bulunuyor.")
            return HttpResponseRedirect(reverse('comment:requestform',))
        
        form.save()
        messages.success(self.request, "Form Bize Ulasmistir." )
        return super().form_valid(form)