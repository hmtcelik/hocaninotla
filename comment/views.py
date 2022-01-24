from django.views import generic
from .models import Uni

class UniView(generic.ListView):
    template_name = 'uni.html'
    context_object_name = 'all_unis'
    
    def get_queryset(self):
        return Uni.objects.all()
    
    
class FacultyView(generic.DetailView):
    model = Uni
    template_name = 'faculty.html'
    
     