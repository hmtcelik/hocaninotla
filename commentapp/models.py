from django.db import models

# Create your models here.

class University(models.Model):
    uni_name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.uni_name
    
class Faculty(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    faculty_name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.faculty_name 
    
class Departmant(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    departmant_name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.departmant_name
    
class Doctor(models.Model):
    departmant = models.ForeignKey(Departmant, on_delete=models.CASCADE)
    doctor_name = models.CharField(max_length=50)
    doctor_image = models.FileField(blank=True)
    about = models.TextField(max_length=500)
    
    def __str__(self):
        return self.doctor_name
    
class Comment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    comment_author = models.CharField(max_length=50)
    comment_title = models.CharField(max_length=50)
    comment = models.TextField(max_length=500)
    
    def __str__(self):
        return self.doctor.doctor_name + '-' + self.comment_author





    
    
