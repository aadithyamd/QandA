from django import forms
from .models import Question, Answer
import re
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class add_Question_Form(forms.ModelForm): # just a regular form

	class Meta:
		model = Question
		fields = ['question_text']
	def clean_text(self):
		return self.cleaned_data.get('question_text')
		
class add_Answer_Form(forms.ModelForm):
	class Meta:
		model = Answer
		fields = ['answer_text']
	def clean_text(self):
		return self.cleaned_data.get('answer_text')