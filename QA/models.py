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

from django.db.models.signals import post_migrate
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import models as auth_models
from django.contrib.auth.models import Permission

# custom user related permissions
def add_user_permissions(sender, **kwargs):
    ct = ContentType.objects.get(app_label='auth', model='user')
    perm, created = Permission.objects.get_or_create(codename='can_verify', name='Can Verify Posts', content_type=ct)
post_migrate.connect(add_user_permissions, sender=auth_models)