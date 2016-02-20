from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Question(models.Model):
	question_text = models.CharField(max_length=120, blank=True, null=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	def __unicode__(self): 
		return self.question_text

class Answer(models.Model):
	# content = models.EmailField()
	answer_text = models.CharField(max_length=200, blank=True, null=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	question = models.ForeignKey(Question)
	author = models.ForeignKey(User)
	upvotes = models.IntegerField(default=0)
	def __unicode__(self): 
		return self.answer_text

class Upvote(models.Model):
	upvoted_user = models.ForeignKey(User, default=1)
	answer = models.ForeignKey(Answer, default=1)
	# def __unicode__(self): 
	# 	return self.answer