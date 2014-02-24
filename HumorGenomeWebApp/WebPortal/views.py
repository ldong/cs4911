from django.shortcuts import render
from django.template import loader, Context
from django.http import HttpResponse
from django.utils import simplejson
from WebPortal.models import HumorContent 

def archive(request):
    humorContents = HumorContent.objects.order_by('id');
    mostRecent = humorContents[len(humorContents) - 1];
    t = loader.get_template("archive.html")
    c = Context({ 'humorContent' : mostRecent })
    return HttpResponse(t.render(c))

def getNextHumor(request):
	if(request.GET.get('id')):
		humorContents = HumorContent.objects.order_by('id');
		idNumber = int(request.GET.get('id'));
		nextId = ((idNumber) % len(humorContents));
		desiredHumor = humorContents[nextId];
		result = {}
		result.update({'id': desiredHumor.id})
		result.update({'url': desiredHumor.url})
		result.update({'title': desiredHumor.title});
		#result.update({'created': desiredHumor.created});
		return HttpResponse(simplejson.dumps(result), content_type='application/json');
	return HttpResponse("BAD");

def getPrevHumor(request):
	if(request.GET.get('id')):
		humorContents = HumorContent.objects.order_by('id');
		idNumber = int(request.GET.get('id')) - 2;
		prevId = ((idNumber) % len(humorContents));
		desiredHumor = humorContents[prevId];
		result = {}
		result.update({'id': desiredHumor.id})
		result.update({'url': desiredHumor.url})
		result.update({'title': desiredHumor.title});
		#result.update({'created': desiredHumor.created});
		return HttpResponse(simplejson.dumps(result), content_type='application/json');
	return HttpResponse("BAD");
