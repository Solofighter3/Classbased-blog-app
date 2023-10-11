from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.views.generic import TemplateView,CreateView,ListView,DetailView,UpdateView,DeleteView
from .models import Blogs,Feedback,Comment
from .forms import addblogform,feedbackform,CommentForm
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
class index(ListView):
    template_name="index.html"
    model=Blogs
    context_object_name="blogs"

    def get_queryset(self,*args,**kwargs):
        return Blogs.objects.order_by("created_first")
    

class feedbacks(CreateView):
   model = Feedback
   form_class=feedbackform
   template_name="feedback.html"
   success_url="/"
   def form_valid(self, form: BaseModelForm) -> HttpResponse:
       form.instance.user=self.request.user
       messages.success(self.request, "Feedback was sent")
       return super().form_valid(form)

class createblog(CreateView):
    template_name="addblog.html"
    model=Blogs
    form_class=addblogform
    success_url="/apps/"
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
       form.instance.user=self.request.user
       return super().form_valid(form)

class updateview(UpdateView):
    template_name="addblog.html"
    model=Blogs
    form_class=addblogform
    success_url="/apps/"
    def form_valid(self,form):
        pk = self.kwargs.get('pk')
        blog=get_object_or_404(Blogs,pk=pk)
        if self.request.user!=blog.user:
            return HttpResponse('not allowded')
        else:
            return super().form_valid(form)
        




class deleteview(DeleteView):
    model=Blogs
    success_url="/apps/"
    context_object_name="blog"
    template_name="delete.html"
    def form_valid(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        blog=get_object_or_404(Blogs,pk=pk)
        if self.request.user==blog.user:
            # Perform the delete operation
            return super().delete(request, *args, **kwargs)
        else:
            # Handle the condition when it is not met
            # For example, you can redirect to an error page
            return HttpResponse('not allowed')



class detailview(DetailView):
    template_name="blogde.html"
    model=Blogs
    context_object_name="blog"#By default django gonna name the  object book
    def get_context_data(self, **kwargs):
        data=super().get_context_data(**kwargs)
        connected_comments = Comment.objects.filter(CommentPost=self.get_object())
        number_of_comments = connected_comments.count()
        data["title"]=Blogs.objects.filter(slug=self.kwargs.get(id,0))
        data['comments'] = connected_comments
        data['no_of_comments'] = number_of_comments
        data['comment_form'] = CommentForm()

        return data
    def post(self , request , *args , **kwargs):
        if self.request.method == 'POST':
            print('-------------------------------------------------------------------------------Reached here')
            comment_form = CommentForm(self.request.POST) 
            if comment_form.is_valid():
                content = comment_form.cleaned_data['content']
                try:
                    parent = comment_form.cleaned_data['parent']
                except:
                    parent=None

            

            new_comment = Comment(content=content , author = self.request.user , CommentPost=self.get_object() , parent=parent)
            new_comment.save()
            return redirect(self.request.path_info)
    

class Yourblogs(ListView):
    template_name="yourblog.html"
    model=Blogs
    context_object_name="blogs"

    def get_queryset(self,*args,**kwargs):
        return Blogs.objects.filter(user=self.request.user).order_by("created_first")