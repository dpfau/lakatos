from prototype.models import Thread
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

def index(request):
	thread_list = Thread.objects.all()
	return render_to_response('prototype/index.html', 
		{'thread_list': thread_list}, 
		context_instance=RequestContext(request))

def detail(request, thread_title):
	try:
		t = Thread.objects.get(title=thread_title)
	except Thread.DoesNotExist:
		return render_to_response('prototype/detail.html')
	return render_to_response('prototype/detail.html', {'thread': t})

def create(request):
	thread_list = Thread.objects.all()
	new_thread_name = request.POST['new_thread_name'].replace(' ', '_')
	if len(new_thread_name) is 0:
	 	return render_to_response('prototype/index.html', 
	 		{'thread_list': thread_list, 'thread_exists': 'No name provided for thread'}, 
	 		context_instance=RequestContext(request))
	else:
	 	if len(thread_list.filter(title=new_thread_name)) is 0:
	 		t = Thread(title=new_thread_name)
	 		t.save()
	 		return HttpResponseRedirect(reverse('prototype.views.detail', args=(new_thread_name,)))
	 	else:
	 		return render_to_response('prototype/index.html', 
	 			{'thread_list': thread_list, 'thread_exists': 'Thread with that name exists'}, 
	 			context_instance=RequestContext(request))
	# return render_to_response('prototype/create.html', {'new_thread_name': new_thread_name}, context_instance=RequestContext(request))