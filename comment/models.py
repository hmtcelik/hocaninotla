from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg #for avarage of rates



class Uni(models.Model):
    uni_name = models.CharField(max_length=50)
    uni_img = models.ImageField(upload_to ='uploads/', blank=True, null=True)

    def __str__(self):
        return self.uni_name

class Faculty(models.Model):
    uni = models.ForeignKey(Uni, on_delete=models.CASCADE)
    faculty_name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.uni.uni_name + '-' + self.faculty_name
    
class Depart(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    depart_name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.faculty.uni.uni_name + '-' + self.depart_name

class Doctor(models.Model):
    depart = models.ForeignKey(Depart, on_delete=models.CASCADE)
    doctor_name = models.CharField(max_length=50)
    doctor_bio = models.TextField(max_length=1000)
    doctor_pp = models.ImageField(upload_to ='uploads/', blank=True, null=True)
    
    def __str__(self):
        return self.depart.faculty.uni.uni_name + '-' + self.doctor_name


RATE_CHOICES = [
    (1.0, '1 - cok kotu'),
    (2.0, '2 - kotu'),
    (3.0, '3 - orta'),
    (4.0, '4 - iyi'),
    (5.0, '5 - cok iyi'),
]
    
    
class Comment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    comment_author = models.CharField(max_length=150)
    comment_body = models.TextField(max_length=1000)
    rate = models.FloatField(choices=RATE_CHOICES, null=True)
    anonymous = models.BooleanField(default=False, blank=True)
    #hide areas -->
    date_time = models.DateTimeField(auto_now_add=True, blank=True)
    likes = models.ManyToManyField(User, related_name='comments_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='comments_dislikes', blank=True)
    total_likes = models.IntegerField(default=0, blank=True)
    total_dislikes = models.IntegerField(default=0, blank=True)
    total_answers = models.IntegerField(default=0, blank=True) # this is number of commentanswers (re-comments)
    
    def __str__(self):
        return self.comment_author+' ---> '+ self.doctor.doctor_name  + '//' + self.doctor.depart.faculty.uni.uni_name

class CommentAnswer(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    answer_author = models.CharField(max_length=150)
    answer_body = models.TextField(max_length=1000)
    date_time = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return 'Yanit: ' + self.answer_author+' ---> '+ self.comment.comment_author + ' // ' + self.comment.doctor.doctor_name + '-' + self.comment.doctor.depart.faculty.uni.uni_name
