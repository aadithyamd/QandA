from django.shortcuts import render
from .forms import add_Question_Form, add_Answer_Form#, RegistrationForm
from .models import Question, Answer
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response

def home(request):
	title = "Welcome"
	form = add_Question_Form(request.POST)
	context ={  
	"template_title":title,
	"form":form,
	#'user': request.user
	}
	#if "submit" in request.POST:
	if form.is_valid() and form.clean_text() != "":
		ques = Question(question_text=form.clean_text())
		ques.save()
	return render(request,"home.html",context)
