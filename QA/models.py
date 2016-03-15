from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User,UserManager
# Create your models here.
class Categories(models.Model):
	categories = models.CharField(max_length=120, blank=False,null=False)
	def __unicode__(self): 
		return self.categories

class Customuser(User):
	category = models.CharField(max_length=300, blank=True,null=True)
	categories = models.ManyToManyField(Categories,related_name='intrested_in')
	DEPARTMENT = (
	('CS', 'Computer Science'),
	('EC', 'Electronics & Communication'),
	('EE', 'Electrical & Electronics'),
	('EB', 'Electronics & Biomedical'),
	)

	department = models.CharField(max_length=2, choices=DEPARTMENT)
	def __str__(self):
		return self.username

class Question(models.Model):
	question_text = models.TextField(blank=False,null=True)
	follow = models.IntegerField(default=0)
	author = models.ForeignKey(Customuser)
	upload = models.FileField(upload_to='uploads/%Y/%m/%d/',blank=True,null=True) #if null is true then NULL is set if no value
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)# but in forms, set blank=True,form can be left. 
	updated = models.DateTimeField(auto_now_add=False, auto_now=True) 
	category1 = models.ForeignKey(Categories,blank=True,null=True,related_name='category1')
	category2 = models.ForeignKey(Categories,blank=True,null=True,related_name='category2')
	category3 = models.ForeignKey(Categories,blank=True,null=True,related_name='category3')
	category4 = models.ForeignKey(Categories,blank=True,null=True,related_name='category4')

	class Meta:
		ordering = ['follow','-timestamp']
		
	def __unicode__(self): 
		return self.question_text

class Answer(models.Model):
	answer_text = models.TextField(blank=False,null=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	question = models.ForeignKey(Question)
	author = models.ForeignKey(Customuser)
	upvotes = models.IntegerField(default=0)
	faculty_upvote = models.IntegerField(default=0)
	verify = models.BooleanField(default=False)
	def __unicode__(self): 
		return self.answer_text

class Upvote(models.Model):
	upvoted_user = models.ForeignKey(User)
	answer = models.ForeignKey(Answer)
	question = models.ForeignKey(Question,default=1)

