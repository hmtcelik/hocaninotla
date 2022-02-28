from django.views import generic
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.db.models import Avg, Count
from django.template import RequestContext


from sinkaf import Sinkaf #kufur engelleyici


from .forms import NewUserForm, RateForm, CommentAnswerForm
from .models import Uni , Faculty, Depart, Doctor, Comment, CommentAnswer
from django.contrib.auth.models import User


# Searchbar func.
def searchbar(request):
    if request.method == "GET":
        search = request.GET.get('search')
        post = Uni.objects.all().filter(uni_name__contains=search)
        post2 = Doctor.objects.all().filter(doctor_name__contains=search)
        context = {'post': post, 'post2' : post2,}
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
    
     
class CommentView(generic.DetailView):
    model = Doctor
    template_name = 'comment.html'

    #(CALISMIYOR)re-comment counter for javascript slider (bunu yapiyom cunki tum yanitlari goster mallik yapmasin eger yorum varsa yapsin diye)
    comments = Comment.objects.all().count()
    i = 1
    for i in range(comments):
        ct = CommentAnswer.objects.filter(comment=i).count()

    
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
            av_rates = round(av_rates, 2)
        else:
            av_rates = 'No Rate'
        #-----------------------------------------------

        all_comments = Comment.objects.filter(doctor=doctor).count #number of all comments
        
        #------ is like/dislike is liked/disliked? for canceling like/dislike  --------
        
        arg = {'av_rates': av_rates,
               'rates1': noRate1,
               'rates2': noRate2,
               'rates3': noRate3,
               'rates4': noRate4,
               'rates5': noRate5,
               'ct_recomments': self.ct,
               'all_comments': all_comments,
               }
        
        context.update(arg)
        return context

#comment like button
def likeview(request, doctor_id, comment_id):
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
    return HttpResponseRedirect(reverse('comment:comment', args=[str(doctor_id)]))
    
#comment dislike button
def dislikeview(request, doctor_id, comment_id):
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
        doctor_id = self.kwargs.get('doctor_id')
        if self.snf.tahmin([form.cleaned_data['comment_body']]):
            messages.error(self.request,"Yorumunuzda uygunsuz ifadeler bulunuyor.")
            return HttpResponseRedirect(reverse('comment:createcomment', args=[str(doctor_id)]))

        form.save()
        return super().form_valid(form)
    

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
            messages.error(self.request,"Yorumunuzda uygunsuz ifadeler bulunuyor.")
            return HttpResponseRedirect(reverse('comment:commentanswer', args=[str(doctor_id),str(comment_id)]))
        
        form.save()
        
        comment = get_object_or_404(Comment, id=self.kwargs.get('comment_id'))
        comment.total_answers += 1 # number of total answers
        comment.save()
        
        return super().form_valid(form)

    
    
#Register----->
def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			messages.success(request, "Basariyla Kayit Olundu." )
			return redirect("comment:login")
		else:
				messages.error(request,"Bir Seyler Ters Gitti, Lutfen Tekrar Deneyiniz.")
	form = NewUserForm()
	return render (request=request, template_name="registration/register.html", context={"register_form":form})


#Login----->
def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("comment:home")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="registration/login.html", context={"login_form":form})


#Logout----->
def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("comment:home")