import math
from time import time
from django.db import models
from django.contrib.auth.models import User
 
class Quiz(models.Model):
    title = models.CharField(max_length=40,null=True)
    description = models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return self.title

    def n_questions(self):
        return len(self.question_set.all())

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete= models.CASCADE)
    question = models.CharField(max_length=200,null=True)
    op1 = models.CharField(max_length=200,null=True)
    op2 = models.CharField(max_length=200,null=True)
    op3 = models.CharField(max_length=200,null=True)
    op4 = models.CharField(max_length=200,null=True)
    ans = models.IntegerField()
    
    def __str__(self):
        return self.question


class Attempt(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete= models.CASCADE)
    name = models.CharField(max_length= 20, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null= True)
    current_question = models.IntegerField()

    def n_points(self):
        points = 0
        for answer in self.answer_set.all():
            if (answer.answer == answer.question.ans):
                points += 1
        return points

    def total_time(self):
        try:
            return self.end_time - self.start_time
        except:
            return None

    def total_time_string(self):
        time_passed = self.end_time - self.start_time
        seconds = time_passed.seconds
        minutes = seconds//60
        seconds = seconds%60
        return "{:02d}:{:02d}.{:.4}".format(minutes, seconds, str(time_passed.microseconds))

    def __str__(self):
        return str(self.quiz) + " | " + self.name + " | "

class Answer(models.Model):
    attempt = models.ForeignKey(Attempt, on_delete= models.CASCADE)
    question = models.ForeignKey(Question, on_delete= models.CASCADE)
    answer = models.IntegerField() 
