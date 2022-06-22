import datetime

from django.db import models


class MainImage(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='main_image/')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    name = models.CharField(max_length=50)
    family_name = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    image = models.ImageField(upload_to='teacher/')
    birth_day = models.DateField(default=datetime.date.today)
    tell = models.CharField(max_length=25)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(max_length=500)
    image = models.ImageField(upload_to='course/')
    teachers = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class LearningMaterial(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    image = models.ImageField(upload_to='learning_material/')
    viewed = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Message(models.Model):
    name = models.CharField(max_length=70)
    email = models.EmailField(max_length=100)
    tell = models.CharField(max_length=25)
    adress = models.CharField(max_length=200)
    user = models.TextField(max_length=300)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class WhoWeAre(models.Model):
    text = models.TextField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)

class New(models.Model):
    name = models.CharField(max_length=60)
    text = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='new/')
    views = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Comment(models.Model):
    news_id = models.ForeignKey(New, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    user = models.TextField(max_length=300)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.news_id.name

class BolimQoshish(models.Model):
    bolim_nomi = models.CharField(max_length=255)
    url_manzil = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.bolim_nomi
