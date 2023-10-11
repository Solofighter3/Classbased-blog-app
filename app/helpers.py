from django.utils.text import slugify
import random
import string
from django.shortcuts import render
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf.pisa import pisaDocument
import uuid
from django.conf import settings
def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def generateslug(text):
    new_slug=slugify(text)
    from .models import Blogs
    if Blogs.objects.filter(slug=new_slug).first():
        new_slug=slugify(text+get_random_string(5))
    return new_slug

def choicess():
    
    from .models import category
    l1=[i for i in category.objects.all()]
    l2=[]
    for i in category.objects.all():
       l2.append(i.cases)
    data=list(zip(l2,l2))
    return data