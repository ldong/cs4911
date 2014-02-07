from django.shortcuts import render
from django.template import loader, Context
from django.http import HttpResponse
from WebPortal.models import HumorContent 

def archive(request):
    humorContents = HumorContent.objects.all() 
    t = loader.get_template("archive.html")
    c = Context({ 'humorContents' : humorContents })
    return HttpResponse(t.render(c))
