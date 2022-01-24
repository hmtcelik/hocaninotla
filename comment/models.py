from django.db import models


class Uni(models.Model):
    uni_name = models.CharField(max_length=50)

    def __str__(self):
        return self.uni_name

class Faculty(models.Model):
    uni = models.ForeignKey(Uni, on_delete=models.CASCADE)
    faculty_name = models.CharField(max_length=50)
    uni_shortcut = models.CharField(max_length=10)
    
    def __str__(self):
        return self.uni_shortcut + '-' + self.faculty_name