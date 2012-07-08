from prototype.models import Thread
from django.template import RequestContext
from django.shortcuts import render_to_response
#from django.http import Http404

def index(request):
	thread_list = Thread.objects.all()
	return render_to_response('prototype/index.html', {'thread_list': thread_list}, context_instance=RequestContext(request))

def detail(request, thread_title):
	try:
		t = Thread.objects.get(title=thread_title)
	except Thread.DoesNotExist:
		return render_to_response('prototype/detail.html')
	return render_to_response('prototype/detail.html', {'thread': t})

def create(request):
	t = Thread(title=request.POST['new_thread_name'].replace(' ','_'))
	t.save()