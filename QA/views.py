from django.shortcuts import render
from .forms import add_Question_Form, add_Answer_Form, UserCreationForm, AuthenticationForm,UserForm# RegistrationForm
from .models import Question, Answer, Upvote, Categories, Customuser
from django.views.decorators.csrf import csrf_protect
from django.contrib import auth
from django.http import HttpResponseRedirect, HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
import ast
from datetime import timedelta
from django.utils.timezone import now
from django.db.models import Q
@login_required 
def home(request):
	if request.user.is_authenticated():
		if len(Customuser.objects.filter(username=request.user.username))==1:
			Cuser = Customuser.objects.get(username=request.user.username)
			Cuser.last_login = now()
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
		if user is not None :
			if user.is_superuser:
				return render(request,"home.html",context)
			elif user.is_active:
				auth.login(request, user)
				return HttpResponseRedirect("/write")
	return render(request,"home.html",context)


def register_view(request):
	if request.method == 'POST':
		form = UserCreationForm(data=request.POST)
		print request.POST
		print request.POST.get("categories","")
		if form.is_valid():
			# permission = Permission.objects.get(name='Can view poll')
			# user.user_permissions.add(permission)
			user = form.save(commit=False)
			user.save()
			return HttpResponseRedirect('/')
	else:
		form = UserCreationForm()
	context = { "form":form, }
	return render(request,"register.html",context)

@login_required
def logout_view(request):
	if request.user.is_superuser:
		return HttpResponseRedirect('/accounts/login')
	Cuser = Customuser.objects.get(username=request.user.username)
	Cuser.last_login = now()
	auth.logout(request)
	# Redirect to a success page.
	return HttpResponseRedirect("/")
	
@login_required
def listquestions(request):
	if request.user.is_superuser:
		return HttpResponseRedirect('/accounts/login')
	category_object = []
	if request.method == 'POST':
		print request.POST
		if request.POST.get("submit","") == "Create Category":
			category = request.POST.get("newcategory","")
			if not Categories.objects.filter(categories = category).exists():
				Categories(categories = category).save()
				category = Categories.objects.get(categories = category)
				return JsonResponse({"category":category.categories,"cid":category.pk}, content_type ="application/json")
			else:
				category = 0
				return HttpResponse({category}, content_type ="application/text")
		form = add_Question_Form(request.POST,request.FILES,)
		# new_file = UploadFile(file = request.FILES['file'])
		# new_file.save()
		# print form.is_valid()
		#if form.is_valid():
		#	questionform = questionform.save(commit=False)
		category1 = request.POST.get("category1","") ## Dangerous
		category2 = request.POST.get("category2","")
		category3 = request.POST.get("category3","")
		category4 = request.POST.get("category4","")
		for i in {category1,category2,category3,category4}:
			if Categories.objects.filter(categories = i).exists():
				category_object.append(Categories.objects.get(categories = i))
			else:
				C = Categories(categories = i).save()
				category_object.append(C)
		category_object.append(None)
		category_object.append(None)
		category_object.append(None)
		category_object.append(None)
		category_object.append(None)
		#print category_object
		form.category1 = category_object[0]
		form.category2 = category_object[1]
		form.category3 = category_object[2]
		form.category4 = category_object[3]
		form.category5 = category_object[4]
		print "the form validity",form.is_valid
		if form.is_valid():
			f = form.save(commit=False)
			f.author=Customuser.objects.get(username=request.user.username)
			f.save()
		return HttpResponseRedirect('/write')
	else:
		form = add_Question_Form()
	qlist = Question.objects.all()
	c = Categories.objects.all()  #change
	context = {
		"list":qlist,
		"form":form,
		"categorylist":c
	}
	return render(request,"write.html",context)

@login_required
def detail(request, question_id):
	if request.user.is_superuser:
		return HttpResponseRedirect('/accounts/login')

	answer = Answer.objects.filter(question = question_id)
	ques = Question.objects.get(pk=question_id) 
	question = Question.objects.filter(pk=question_id) #list obtained for iteration in template
	current_users_upvoted_content = Upvote.objects.filter(upvoted_user=request.user)
	current_users_upvoted_answers = []
	for i in current_users_upvoted_content:
		current_users_upvoted_answers.append(i.answer)
	title = "Question is "
	author = Customuser.objects.get(username=request.user.username)
	#print request.POST
	# upvote submission
	if request.method == 'POST' and (request.POST.get("submit","") == "upvote" or request.POST.get("submit","") == "upvoted"): 
		#form = add_Answer_Form(request.POST)
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
			vote = Upvote(upvoted_user=User,answer=answer,question=answer.question)
			answer.upvotes+=1
			if request.user.is_staff:
				answer.faculty_upvote+=1
			answer.save()
			vote.save()
		return HttpResponseRedirect('/write/%s' % str(question_id))

	if request.user.is_authenticated:
	#  Code to delete answer on clicking delete button

		if request.method == 'POST' and request.POST.get("submit","") == "delete":
			answer_id = request.POST.get("answer_id","")
			print answer_id
			answer = Answer.objects.get(pk=answer_id)
			if request.user.is_staff or request.user.username==answer.author.username: 
				answer.delete()
			return HttpResponseRedirect('/write/%s' % str(question_id))

	#  Code to delete Question on clicking delete button

		if request.method == 'POST' and request.POST.get("submit","") == "Delete Question":
			
			question_id = request.POST.get("question_id","")
			print question_id
			question = Question.objects.get(pk=question_id)
			if request.user.is_staff or request.user.username==question.author.username:
				question.delete()
			return HttpResponseRedirect('/write/')

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

	if request.user.is_authenticated():
		if request.user.is_staff:
			form = add_Answer_Form()
			return render(request, 'staff_detail.html', {"template_title":title,"answer":answer,
			'form':form,'question': question,'check_upvoted_already': current_users_upvoted_answers })

	form = add_Answer_Form()
	return render(request, 'detail.html', {"template_title":title,"answer":answer,
			'form':form,'question': question,'check_upvoted_already': current_users_upvoted_answers })

@login_required
def read(request):
	if request.user.is_superuser:
		return HttpResponseRedirect('/accounts/login')
	question_id = 2
	answer_id = 2
	answer = Answer.objects.get(pk = answer_id)
	current_users_upvoted_content = Upvote.objects.filter(upvoted_user=request.user)
	current_users_upvoted_answers = []
	for i in current_users_upvoted_content:
		current_users_upvoted_answers.append(i.answer)
	Cuser = Customuser.objects.get(username=request.user.username)
	print Cuser
	c=Categories.objects.all()
	if request.method == 'POST' and (request.POST.get("submit","") == "upvote" or request.POST.get("submit","") == "upvoted"): 
		answer_id = request.POST.get("answer_id","")
		answer = Answer.objects.get(pk=answer_id)
		if Upvote.objects.filter(upvoted_user=Cuser,answer=answer).exists():
			up = Upvote.objects.get(upvoted_user=Cuser,answer=answer)
			up.delete()
			answer.upvotes-=1
			if request.user.is_staff:
				answer.faculty_upvote-=1
			answer.save()
		else:
			vote = Upvote(upvoted_user=Cuser,answer=answer,question=answer.question)
			answer.upvotes+=1
			if request.user.is_staff:
				answer.faculty_upvote+=1
			answer.save()
			vote.save()
		return HttpResponseRedirect('/read')
	#print Cuser.category
	if request.POST:
		print request.POST					
		if Cuser.category is None:
			a = []
			a.append(int(request.POST.get("category","")))
		else:
			a = ast.literal_eval(Cuser.category)
			b = []
			b.append(int(request.POST.get("category","")))
			a= list(set(a)|set(b))
			#resultList=[1,2,5,7,9]
			#a = a + list(d)
		Cuser.category = str(a)
		Cuser.save()


	if Cuser.category != None:
		categorylistofuser = ast.literal_eval(Cuser.category)
	else :
		categorylistofuser = []
	Qobjects = []
	for i in categorylistofuser:
		Qobjects += (Question.objects.filter(Q(Q(category1=i) |Q(category2=i)|Q(category3=i)|Q(category4=i))))
	#print Qobjects
	Aobjects = []
	for i in Qobjects:
		Aobjects += Answer.objects.filter(question=i)
	#print Aobjects
	LatestAobjects = []
	onesecond = timedelta(seconds=1)
	for i in Aobjects:
		if (i.timestamp-Cuser.last_login) > onesecond:
			LatestAobjects.append(i)
	LatestAobjects = list(set(LatestAobjects))
	

	#Latest Questions
	print "Latest Questions"
	LatestQobjects = []
	for i in Qobjects:
		if (i.timestamp-Cuser.last_login) > onesecond:
			LatestQobjects.append(i)
	LatestQobjects = list(set(LatestQobjects))
	

	print "Latest new Answers in upvoted answer's question"
	# User upvoted an answer that belonged to another category. New answer to that questions are shown
	Uobjects = Upvote.objects.filter(upvoted_user=Cuser)
	QofUobjects = []
	AofUobjects = []
	for i in Uobjects:
		QofUobjects.append(i.question)
		AofUobjects.append(i.answer)
	print QofUobjects
	othersAofUobjects = []
	otherAofUobjects  = []
	for i in QofUobjects:
		otherAofUobjects += Answer.objects.filter(question=i)
	for i in otherAofUobjects:
		if i not in AofUobjects:
			 othersAofUobjects.append(i)
	print othersAofUobjects
	LatestothersAofUobjects = []
	onesecond = timedelta(seconds=1)
	for i in othersAofUobjects:
		if (i.timestamp-Cuser.last_login) > onesecond:
			LatestothersAofUobjects.append(i)
	LatestothersAofUobjects = list(set(LatestothersAofUobjects))

	print "listing all answers by upvote order"
	JustAobjects = Answer.objects.all().order_by('-upvotes')
	#ques = answer.question
	#question = Question.objects.filter(pk=question_id)
	return render(request,'read.html',{"check_upvoted_already":current_users_upvoted_answers,"LatestAobjectslist":LatestAobjects,"LatestQobjectslist":LatestQobjects,
		"LatestothersAofUobjectslist":LatestothersAofUobjects,"categorylist":c,"JustAobjectslist":JustAobjects})