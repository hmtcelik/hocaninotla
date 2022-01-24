from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import University, Faculty, Departmant, Doctor, Comment

# Create your views here.

class IndexView(TemplateView):
    template_name = "index.html"
     
class UniView(ListView):
    model = University
    template_name = 'universty.html'
    context_object_name = 'all_universities'
    uni_name = University.uni_name
    
class FacultyView(ListView):
    model = Faculty
    template_name = 'faculty.html'
    context_object_name = 'all_faculties'
    
class DepartmantView(ListView):
    model = Departmant
    template_name = 'departmant.html'
    context_object_name = 'all_departmants'

class DoctorView(ListView):
    model = Doctor()
    template_name = 'doctor.html'
    context_object_name = 'all_doctors'
    
class CommentView(ListView):
    model = Faculty
    template_name = 'comment.html'
    context_object_name = 'all_comments'
    
    