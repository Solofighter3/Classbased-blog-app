from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from .helpers import generateslug,choicess
from django.contrib.auth import get_user_model
# Create your models here.


class category(models.Model):
    cases = models.CharField(max_length=15,default='superhero')
    def __str__(self) -> str:
        return self.cases


class Blogs(models.Model):
    categorys=models.CharField(max_length=15,default='superhero',choices=choicess())
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    title=models.CharField(max_length=100)
    content=RichTextField(blank=True)
    slug=models.SlugField(max_length=1000,null=True,blank=True)
    image=models.ImageField(upload_to="blogapps/files")
    created_first=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
       self.slug = generateslug(self.title)
       super(Blogs, self).save(*args, **kwargs)

    



class Feedback(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    email=models.EmailField(unique=True)
    content=models.TextField()


class PublishingUser(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name
    
class Comment(models.Model):
    CommentPost = models.ForeignKey(Blogs , on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model() , on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self' , null=True , blank=True , on_delete=models.CASCADE , related_name='replies')
# ForeignKey called parent, which establishes a many-to-one relationship with itself (self)
#  because a comment can have many replies, but a reply can have only one parent.
    class Meta:
        ordering=['-date_posted']

    def __str__(self):
        return str(self.author) + ' comment ' + str(self.content)

    @property
    def children(self):
        return Comment.objects.filter(parent=self).reverse()
#children filters all the replies of the comments
    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False
#is_parent categorizes whether a comment is parent or reply of comment.