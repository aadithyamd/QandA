from django import forms
from .models import Question, Answer, Categories, Customuser
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class add_Question_Form(forms.ModelForm): # just a regular form
    question_text = forms.CharField(label=_("question_text"),
        widget=forms.Textarea({'cols': '40', 'rows': '5'}))
    
    class Meta:
        model = Question
        fields = ['question_text',  'upload', 
        'category1','category2',
        'category3','category4']

    def clean_text(self):
        if question_text == "":
            raise forms.ValidationError(
                "Need a question",)
        else:
            return True
    
    def save(self,commit=True):
        question = super(add_Question_Form, self).save(commit=False)
        question.question_text = self.cleaned_data["question_text"]
        if commit:
            question.save()
        return question
		
class add_Answer_Form(forms.ModelForm):
	class Meta:
		model = Answer
		fields = ['answer_text']
	def clean_text(self):
		return self.cleaned_data.get('answer_text')

class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as before, for verification."))

    # User's username field and our own 2 fields pass1 and pass2 are used. Later
    # we shall set the User's password by user.set_password.

    class Meta:
        model = Customuser
        fields = ("username","email","first_name","department")


    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        self.instance.username = self.cleaned_data.get('username')
        # To remove invalid passwords like short words, number only cases 
        auth.password_validation.validate_password(self.cleaned_data.get('password2'), self.instance)
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password2"])
        if commit:
            user.save()
        return user


class AuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    username = forms.CharField( max_length=254,
                                widget=forms.TextInput( attrs={'autofocus': ''}),
    )
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': _("Please enter a correct username and password. "
                           "Note that both fields may be case-sensitive."),
        'inactive': _("This account is inactive."),
    }

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = auth.authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    )
            else:
                return self.cleaned_data
class UserForm(forms.ModelForm):
    class Meta:
        model = Customuser
        fields = ('categories',)

class CustomuserAdminForm(forms.ModelForm):

    class Meta:
        model = Customuser
        fields = ("username","email","first_name","last_name",
                'department','groups','is_active','is_staff','is_superuser')
#       fields = ['username','password','verify,'first_name','last_name','email','batch',]

################### Django classes ##########################



