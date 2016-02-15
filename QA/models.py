from __future__ import unicode_literals
from django.db import models

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
	def __unicode__(self): 
		return self.answer_text
