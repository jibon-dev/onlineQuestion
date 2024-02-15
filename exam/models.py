from django.db import models
from accounts.models import User

# Create your models here.
class Question(models.Model):
    question = models.TextField()
    option_one = models.CharField(max_length=100)
    option_two = models.CharField(max_length=100)
    option_three = models.CharField(max_length=100)
    option_four = models.CharField(max_length=100)
    correct_answer = models.CharField(max_length=100)
    duration = models.IntegerField()

    def __str__(self):
        return self.question


class Clock(models.Model):
    time = models.IntegerField()
    flag = models.BooleanField(default=False)


class Solution(models.Model):
    number = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True) 
    questions = models.CharField(max_length=400, blank=True)
    solution = models.CharField(max_length=400, blank=True)
    
    class Meta:
        unique_together = (('number',),)

    def __str__(self):
        return self.user.email


        