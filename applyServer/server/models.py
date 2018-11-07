from django.db import models

# Create your models here.
class Students(models.Model):
    name = models.CharField(max_length = 20)
    stu_id = models.CharField(max_length = 20)
    sex = models.CharField(max_length = 1)
    tel = models.CharField(max_length = 20)
    QQ = models.CharField(max_length = 20)
    email = models.CharField(max_length = 30)
    academy = models.CharField(max_length = 40)
    isAdjust = models.CharField(max_length = 1)
    asp = models.CharField(max_length = 40)
    resume = models.TextField()
    characterStage = models.CharField(max_length = 20)
    character = models.TextField()

class Asp(models.Model):
    name = models.CharField(max_length = 20)
    stu_id = models.CharField(max_length = 20)
    tel = models.CharField(max_length = 20)
    BU = models.CharField(max_length = 20)
    order = models.CharField(max_length = 20)
    isAdjust = models.CharField(max_length = 1)
    audition1 = models.TextField(null=True)
    scale1 = models.FloatField(null=True)
    audition2 = models.TextField(null=True)
    scale2 = models.FloatField(null=True)
    audition3 = models.TextField(null=True)
    scale3 = models.FloatField(null=True)
    applyStatus = models.IntegerField()

class BUInformation(models.Model):
    BU = models.CharField(max_length = 20)
    stage = models.CharField(max_length = 1)

class Admins(models.Model):
    BU = models.CharField(max_length = 20)
    tel = models.CharField(max_length = 20)
    name = models.CharField(max_length = 20)
    passWord = models.CharField(max_length = 50)

class Queue(models.Model):
    BU = models.CharField(max_length = 20)
    queue = models.TextField()

        
