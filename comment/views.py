from django.views import generic
from .models import Uni , Faculty, Depart, Doctor
from django.shortcuts import render


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
    