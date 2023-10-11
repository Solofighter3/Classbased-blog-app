from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Blogs,Feedback,category
from froala_editor.widgets import FroalaEditor
from .helpers import choicess
from django.db.migrations.state import get_related_models_tuples
from .models import Comment
from django.utils.translation import gettext_lazy as _

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        

        fields = ['content','parent']
        
        labels = {
            'content': _(''),
        }
        
        widgets = {
            'content' : forms.TextInput(attrs={"class": "block w-full text-gray-900 border border-gray-300 rounded-lg bg-gray-50 sm:text-md focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"}),
            
            }        
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username',"email",'password1','password2', )

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    
class feedbackform(forms.ModelForm):
   class Meta:
       model=Feedback
       fields=('user','email','content')
       exclude = ['user']

class addblogform(forms.ModelForm):
   data=choicess()
   print(data)
   categorys=forms.ChoiceField(widget=forms.Select(attrs={"class":" btn-secondary btn-lg dropdown-toggle bg-green-600"}),choices=data)
   class Meta:
      model=Blogs
      fields=("title","content","image","categorys")
      content = forms.CharField(widget=FroalaEditor)
      
