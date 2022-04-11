from urllib import request
from wsgiref.util import request_uri
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg #for avarage of rates



class Uni(models.Model):
    uni_name = models.CharField(max_length=150)
    uni_img = models.ImageField(upload_to ='uploads/', blank=True, null=True)

    def __str__(self):
        return self.uni_name

class Faculty(models.Model):
    uni = models.ForeignKey(Uni, on_delete=models.CASCADE)
    faculty_name = models.CharField(max_length=150)
    
    def __str__(self):
        return self.uni.uni_name + '-' + self.faculty_name
    
class Depart(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    depart_name = models.CharField(max_length=150)
    
    def __str__(self):
        return self.faculty.uni.uni_name + '-' + self.depart_name

class Doctor(models.Model):
    depart = models.ForeignKey(Depart, on_delete=models.CASCADE)
    doctor_name = models.CharField(max_length=150)
    doctor_lecture = models.CharField(max_length=150) 
    doctor_link = models.URLField(max_length=200, blank=True, default="#")
    doctor_av_rate = models.FloatField(default=0.0, blank=True) 
    doctor_total_rate = models.IntegerField(default=0, blank=True)
    
    def __str__(self):
        return self.depart.faculty.uni.uni_name + '-' + self.doctor_name


RATE_CHOICES = [
    (5.0, '5 - çok iyi'),
    (4.0, '4 - iyi'),
    (3.0, '3 - orta'),
    (2.0, '2 - kötü'),
    (1.0, '1 - çok kötü'),
]

GRADE_CHOICES = (
    ('Henüz Bilmiyorum','Henüz Bilmiyorum'),
    ('AA','AA'),
    ('BA','BA'),
    ('BB','BB'),
    ('CB','CB'),
    ('CC','CC'),
    ('DC','DC'),
    ('DD','DD'),
    ('FF','FF'),        
)

TAKE_AGAIN_CHOICES = (
    ('Evet','Evet'),
    ('Hayır','Hayır'),
    ('Emin Değilim','Emin Değilim'),
)

ATTANDANCE_CHOICES = (
    ('Zorunlu','Zorunlu'),
    ('Zorunlu Değil','Zorunlu Değil'),
)

ONLINE_CLASS_CHOICES = (
    ('Yüzyüze Eğitim','Yüzyüze Eğitim'),
    ('Online Eğitim','Online Eğitim'),
    ('Hibrit Eğitim','Hibrit Eğitim'),
)

class Comment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    comment_author = models.CharField(max_length=150)
    comment_author_id = models.IntegerField()
    comment_author_email = models.CharField(max_length=150)
    rate = models.FloatField(choices=RATE_CHOICES, null=True)
    comment_body = models.TextField(max_length=1000, blank=True)
    take_again = models.CharField(max_length=20, choices=TAKE_AGAIN_CHOICES, null=True, blank=True)
    attandance = models.CharField(max_length=20, choices=ATTANDANCE_CHOICES, null=True, blank=True)
    online_class = models.CharField(max_length=20, choices=ONLINE_CLASS_CHOICES, null=True, blank=True)
    grade = models.CharField(max_length=20, choices=GRADE_CHOICES, null=True, blank=True)
    anonymous = models.BooleanField(default=False, blank=True)
    #hide areas -->
    date_time = models.DateTimeField(auto_now_add=True, blank=True)
    likes = models.ManyToManyField(User, related_name='comments_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='comments_dislikes', blank=True)
    total_likes = models.IntegerField(default=0, blank=True)
    total_dislikes = models.IntegerField(default=0, blank=True)
    net_like = models.IntegerField(default=0, blank=True)
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

class ReportComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    report_author = models.CharField(max_length=150)
    report_body = models.TextField(max_length=1000, blank=True)
    date_time = models.DateTimeField(auto_now_add=True, blank=True)
    
    def __str__(self):
        return 'Report:' + self.report_author + ' ---> ' + self.comment.comment_author + ' // ' + self.comment.doctor.doctor_name + '-' + self.comment.doctor.depart.faculty.uni.uni_name
    
    
class BannedEmails(models.Model):
    email = models.CharField(max_length=150)
    date_time = models.DateTimeField(auto_now_add=True, blank=True)
    
    def __str__(self):
        return self.email

class Requests(models.Model):
    request_author = models.CharField(max_length=150)
    request_body = models.TextField(max_length=1000)
    date_time = models.DateTimeField(auto_now_add = True, blank=True)
    
    def __str__(self):
        return self.request_author
    
class DoctorRequests(models.Model):
    request_author = models.CharField(max_length=150)
    doctor_name = models.CharField(max_length=150)
    uni_name = models.CharField(max_length=150)
    faculty_name = models.CharField(max_length=150)
    depart_name = models.CharField(max_length=150)
    doctor_lecture = models.CharField(max_length=150) 

    def __str__(self):
        return self.request_author