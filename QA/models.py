from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Question(models.Model):
	question_text = models.CharField(max_length=120, blank=False,null=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	category1 = models.CharField(max_length=120, blank=True,default="")
	category2 = models.CharField(max_length=120, blank=True,null=True)
	category3 = models.CharField(max_length=120, blank=True,null=True)
	category4 = models.CharField(max_length=120, blank=True,null=True)
	def __unicode__(self): 
		return self.question_text

class Answer(models.Model):
	answer_text = models.CharField(max_length=200, blank=False,null=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	question = models.ForeignKey(Question)
	author = models.ForeignKey(User)
	upvotes = models.IntegerField(default=0)
	faculty_upvote = models.IntegerField(default=0)
	verify = models.BooleanField(default=False)
	def __unicode__(self): 
		return self.answer_text

class Upvote(models.Model):
	upvoted_user = models.ForeignKey(User, default=1)
	answer = models.ForeignKey(Answer, default=1)

class Categories(models.Model):
	categories = models.CharField(max_length=120, blank=False)