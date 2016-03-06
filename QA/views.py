from django.shortcuts import render
from .forms import add_Question_Form, add_Answer_Form, UserCreationForm, AuthenticationForm# RegistrationForm
from .models import Question, Answer, Upvote, Categories
from django.views.decorators.csrf import csrf_protect
from django.contrib import auth
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

@login_required 
def home(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect("/write")
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
	category_object = []
	if request.method == 'POST':
		print request.POST
		if request.POST.get("submit","") == "Create Category":
			category = request.POST.get("newcategory","")
			if not Categories.objects.filter(categories = category).exists():
				Categories(categories = category).save()
			else:
				category = 0
			return HttpResponse({category}, content_type ="application/text")

		form = add_Question_Form(data=request.POST)
		questionform = form.save(commit=False)
		category1 = request.POST.get("category1","") ## Dangerous
		category2 = request.POST.get("category2","")
		category3 = request.POST.get("category3","")
		category4 = request.POST.get("category4","")
		for i in {category1,category2,category3,category4}:
			if Categories.objects.filter(categories = i).exists():
				category_object.append(Categories.objects.get(categories = i))
			if not Categories.objects.filter(categories = i).exists():
				C = Categories(categories = i).save()
				category_object.append(C)
		if form.is_valid():
			category_object.append(None)
			category_object.append(None)
			category_object.append(None)
			category_object.append(None)
			print category_object
			questionform.category1 = category_object[0]
			questionform.category2 = category_object[1]
			questionform.category3 = category_object[2]
			questionform.category4 = category_object[3]
			questionform.category5 = category_object[4]
			questionform.save()
			return HttpResponseRedirect('/write')
	else:
		c = list(Categories.objects.all().values_list('categories', flat=True).order_by('categories'))  
		form = add_Question_Form()
	qlist = Question.objects.all()
	context = {
	"list":qlist,
	"form":form,
	"categorylist":c
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
	print request.POST
	# upvote submission
	if request.method == 'POST' and (request.POST.get("submit","") == "upvote" or request.POST.get("submit","") == "upvoted"): 
		form = add_Answer_Form(request.POST)
		answer_id = request.POST.get("answer_id","")
		answer = Answer.objects.get(pk=answer_id)
		User = request.user
		if Upvote.objects.filter(upvoted_user=User,answer=answer).exists():
			up = Upvote.objects.get(upvoted_user=User,answer=answer)
			up.delete()
			answer.upvotes-=1
			if request.user.is_staff:
				answer.faculty_upvote-=1
			answer.save()
		else:
			vote = Upvote(upvoted_user=User,answer=answer)
			answer.upvotes+=1
			if request.user.is_staff:
				answer.faculty_upvote+=1
			answer.save()
			vote.save()
		return HttpResponseRedirect('/write/%s' % str(question_id))
	if request.method == 'POST' and request.POST.get("submit","") == "delete":
		answer_id = request.POST.get("answer_id","")
		print answer_id
		answer = Answer.objects.get(pk=answer_id)
		answer.delete()
		return HttpResponseRedirect('/write/%s' % str(question_id))

	if request.method == 'POST' and request.POST.get("submit","") == "Add Answer":
		form = add_Answer_Form(data=request.POST)
		if form.is_valid():
			ans = Answer(answer_text=form.clean_text(),question=ques,author=author)
			ans.save()
			return HttpResponseRedirect('/write/%s' % str(question_id))

	elif request.method == 'POST' and (request.POST.get("submit","") == "verify" or request.POST.get("submit","") == "verified") :
		if request.user.is_authenticated() and request.user.is_staff:
			answer_id = request.POST.get("answer_id","")
			ans = Answer.objects.get(pk=answer_id)
			if ans.verify == False:
				ans.verify = True
			else:
				ans.verify = False
			ans.save()
			form = add_Answer_Form()
			return render(request, 'staff_detail.html', {"template_title":title,"answer":answer,
			'form':form,'question': question,'check_upvoted_already': current_users_upvoted_answers })

	elif request.user.is_authenticated():
		if request.user.is_staff:
			form = add_Answer_Form()
			return render(request, 'staff_detail.html', {"template_title":title,"answer":answer,
			'form':form,'question': question,'check_upvoted_already': current_users_upvoted_answers })

	form = add_Answer_Form()
	return render(request, 'detail.html', {"template_title":title,"answer":answer,
			'form':form,'question': question,'check_upvoted_already': current_users_upvoted_answers })

def read(request):
	question_id = 2
	answer_id = 2
	answer = Answer.objects.get(pk = answer_id)
	#ques = answer.question
	#question = Question.objects.filter(pk=question_id)
	return render(request,'read.html',{"answer":answer})