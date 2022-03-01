from django.shortcuts import render

def my_404(request, exception):
    return render(request,'404/404.html')

def my_500(request):
    return render(request,'404/500.html')