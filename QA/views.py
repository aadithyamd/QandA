from django.shortcuts import render
from .forms import add_Question_Form, add_Answer_Form, UserCreationForm, AuthenticationForm# RegistrationForm
from .models import Question, Answer, Upvote
from django.views.decorators.csrf import csrf_protect
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

def home(request):
	location = "/"
	form = AuthenticationForm(request.POST)
	context ={  
	"form":form,
	"next": location
	}

	if form.is_valid() and form.clean() != "":
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		user = auth.authenticate(username=username, password=password)
		if user is not None and user.is_active:
			auth.login(request, user)
			return HttpResponseRedirect("/write")
	return render(request,"home.html",context)


def register_view(request):
	if request.method == 'POST':
		form = UserCreationForm(data=request.POST)
		if form.is_valid():
			# permission = Permission.objects.get(name='Can view poll')
			# user.user_permissions.add(permission)
			user = form.save()
			return HttpResponseRedirect('/')
	else:
		form = UserCreationForm()
	context = { "form":form, }
	return render(request,"register.html",context)


def logout_view(request):
	auth.logout(request)
	# Redirect to a success page.
	return HttpResponseRedirect("/")
	
@login_required
def listquestions(request):
	title = "Put your question here"
	if request.method == 'POST':
		form = add_Question_Form(data=request.POST)
		if form.is_valid():
			form.save(commit=True)
			return HttpResponseRedirect('/write')
	else:
		form = add_Question_Form()
	qlist = Question.objects.all()
	context = {
	"template_title":title,
	"list":qlist,
	"form":form,
	}
	return render(request,"write.html",context)

@login_required
def detail(request, question_id):
	answer = Answer.objects.filter(question = question_id)
	ques = Question.objects.get(pk=question_id) 
	question = Question.objects.filter(pk=question_id) #list obtained for iteration in template
	current_users_upvoted_content = Upvote.objects.filter(upvoted_user=request.user)
	current_users_upvoted_answers = []
	for i in current_users_upvoted_content:
		current_users_upvoted_answers.append(i.answer)
	title = "Question is "
	author = request.user
	form = add_Answer_Form(request.POST)
	# upvote submission
	if request.method == 'POST' and request.POST.get("submit","") == "": ############
		answer_id = request.POST.get("answer_id","")
		answer = Answer.objects.get(pk=answer_id)
		User = request.user
		if Upvote.objects.filter(upvoted_user=User,answer=answer).exists():
			print "already exists"
		else:
			vote = Upvote(upvoted_user=User,answer=answer)
			answer.upvotes+=1
			answer.save()
			vote.save()
		return HttpResponseRedirect('/write/%s' % str(question_id))
		# answer submission
	if request.method == 'POST' and request.POST.get("submit","") != "":
		form = add_Answer_Form(data=request.POST)
		if form.is_valid():
			ans = Answer(answer_text=form.clean_text(),question=ques,author=author)
			ans.save()
			return HttpResponseRedirect('/write/%s' % str(question_id))
	else:
		form = add_Answer_Form()
		return render(request, 'detail.html', {"template_title":title,"answer":answer,
			'form':form,'question': question,'check_upvoted_already': current_users_upvoted_answers })

# def vote(request, answer_id):
# 	print answer_id
