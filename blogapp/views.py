from django.views.generic import TemplateView,View
from app.forms import SignUpForm
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login


class SignupPageView(View):
    template_name = 'signup.html'
    form_class =SignUpForm
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})
        
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  
            # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(
                username=form.cleaned_data['username'],
                password=raw_password,
            )
            login(request, user) 
            return redirect('login')
       
        return render(request, self.template_name, context={'form': form})