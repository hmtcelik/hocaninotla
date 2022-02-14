from django.views import generic
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse



from .forms import NewUserForm, RateForm
from .models import Uni , Faculty, Depart, Doctor, Comment


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

class CommentCreate(generic.FormView):
    template_name = 'comment_add.html'
    form_class = RateForm

    def get_success_url(self):
        return reverse('comment:comment', kwargs={'pk': self.kwargs.get('doctor_id') })

    def form_valid(self, form):
        form.instance.doctor_id = self.kwargs.get('doctor_id')
        form.save()
        
        return super().form_valid(form)


    '''def form_valid(self, form):
        doctor_id = self.kwargs['doctor_id']
        doctor = Doctor.objects.get(pk=doctor_id)
       ''' 
        
        


'''def createcomment(request):
    if request.method == "POST":
        form = RateForm(request.POST)
        if form.is_valid():
            obj = form.save()
            return redirect("comment:comment")
    form = RateForm()
    return render (request=request, template_name="comment_add.html", context={"rate_form":form})
'''

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