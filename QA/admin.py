from django.contrib import admin
from .models import Question, Answer, Upvote
from .forms import add_Question_Form, add_Answer_Form

class QuestionAdmin(admin.ModelAdmin):
	list_display = ["__unicode__","timestamp"]
	#form = add_Question
	class Meta:
		model = add_Question_Form
class AnswerAdmin(admin.ModelAdmin):
	list_display = ["__unicode__","question","timestamp"]
	#form = add_Question
	class Meta:
		model = add_Answer_Form
	def save_model(self, request, obj, form, change):
		obj.user = request.user
		obj.save()
class UpvoteAdmin(admin.ModelAdmin):
	list_display = ["answer","upvoted_user"]

admin.site.register(Question,QuestionAdmin)
admin.site.register(Answer,AnswerAdmin)
admin.site.register(Upvote,UpvoteAdmin)