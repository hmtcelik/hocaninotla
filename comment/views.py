from django.views import generic
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.db.models import Avg #for avarage of rates
from django.template import RequestContext




from .forms import NewUserForm, RateForm, CommentAnswerForm
from .models import Uni , Faculty, Depart, Doctor, Comment, CommentAnswer
from django.contrib.auth.models import User


#like button
def likeview(request, doctor_id, comment_id):
    comment = get_object_or_404(Comment, id=request.POST.get('comment_id'))
    user = request.user
    comment.likes.add(user)
    comment.save()
    print(doctor_id)
    print(comment_id)
    return HttpResponseRedirect(reverse('comment:comment', args=[str(doctor_id)]))
    
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

    #counting how many rates for each rate
    rates1 = Comment.objects.filter(rate=1.0).count()
    rates2 = Comment.objects.filter(rate=2.0).count()
    rates3 = Comment.objects.filter(rate=3.0).count()
    rates4 = Comment.objects.filter(rate=4.0).count()
    rates5 = Comment.objects.filter(rate=5.0).count()
    
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
        
        stuff = get_object_or_404(Comment, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        arg = {'av_rates': av_rates,
               'rates1': self.rates1,
               'rates2': self.rates2,
               'rates3': self.rates3,
               'rates4': self.rates4,
               'rates5': self.rates5,
               'ct_recomments': self.ct,
               'total_likes': total_likes,
               }
        
        context.update(arg)
        return context
    

class CommentCreate(generic.FormView):
    template_name = 'comment_add.html'
    form_class = RateForm

    def get_success_url(self):
        return reverse('comment:comment', kwargs={'pk': self.kwargs.get('doctor_id') })

    def form_valid(self, form):
        form.save(commit=False)        
        form.instance.doctor_id = self.kwargs.get('doctor_id')
        form.instance.comment_author = self.request.user
        form.save()
        
        return super().form_valid(form)

class CommentAnswerView(generic.FormView):
    template_name = 'comment_answering.html'
    form_class = CommentAnswerForm

    def get_success_url(self):
        return reverse('comment:comment', kwargs={'pk': self.kwargs.get('doctor_id') })
    
    def form_valid(self, form):
        form.save(commit=False)
        form.instance.comment_id = self.kwargs.get('comment_id')
        form.instance.answer_author = self.request.user
        form.save()
        
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