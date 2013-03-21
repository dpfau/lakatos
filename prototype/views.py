from prototype.models import Thread, Paper, Node, Edge
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from lakatos.mendeley_client import MendeleyClient

def index(request):
	""" Display a list of threads """
	thread_list = Thread.objects.all()
	return render_to_response('prototype/index.html', 
		{'thread_list': thread_list}, 
		context_instance=RequestContext(request))

def view_thread(request, thread_title):
	""" Show all papers within a thread, along with the other papers to which they are linked, possibly in other threads """
	try:
		t = Thread.objects.get(title=thread_title)
	except Thread.DoesNotExist:
		return render_to_response('prototype/detail.html', {'title': thread_title}, context_instance=RequestContext(request))
	return render_to_response('prototype/detail.html', {'thread': t}, context_instance=RequestContext(request))

def make_thread(request):
	""" Create a new thread """
	thread_list = Thread.objects.all()
	new_thread_name = request.POST['new_thread_name'].replace(' ', '_')
	if len(new_thread_name) is 0:
	 	return render_to_response('prototype/index.html', 
	 		{'thread_list': thread_list, 'thread_exists': 'No name provided for thread'}, 
	 		context_instance=RequestContext(request))
	else:
	 	if len(thread_list.filter(title=new_thread_name)) is 0:
	 		Thread.objects.create(title=new_thread_name)
	 		return HttpResponseRedirect(reverse('prototype.views.view_thread', args=(new_thread_name,)))
	 	else:
	 		return render_to_response('prototype/index.html', 
	 			{'thread_list': thread_list, 'thread_exists': 'Thread with that name exists'}, 
	 			context_instance=RequestContext(request))

def search(request, thread_title=None):
	""" Pass a search query to the Mendeley API and display top results """
	if request.method == 'POST':
		query = request.POST['query']
		mendeley = MendeleyClient('03257b25c6866c0cfc0953f87b774f6904f975d88', '79f8032c78ccdac6fe31d0bd399f41e2')
		try:
			mendeley.load_keys()
		except IOError:
			mendeley.get_required_keys()
			mendeley.save_keys()
		result = mendeley.search(query, items=10)
		documents = []
		for doc in result['documents']:
			paper = Paper.import_mendeley_paper(doc)
			if paper is not None:
				documents.append(Paper.import_mendeley_paper(doc))
		return render_to_response('prototype/search.html', {'query': query, 'documents': documents, 'thread': thread_title}, context_instance=RequestContext(request))
	else:
		return render_to_response('prototype/search.html', {'thread': thread_title})

def add(request, thread_title=None):
	""" Add a given paper as a node to a thread """
	if thread_title == None:
		return HttpResponseRedirect(reverse('prototype.views.index'))
	else:
		if request.method == 'POST':
			Node.objects.create(paper=Paper.objects.get(uuid=request.POST['uuid']), thread=Thread.objects.get(title=thread_title))
		return HttpResponseRedirect(reverse('prototype.views.view_thread', args=(thread_title,)))

def choose_link(request, node_id):
	return render_to_response('prototype/link.html', {'in_link': node_id, 'threads': Thread.objects.all()}, context_instance=RequestContext(request))

def make_link(request):
	if request.method == 'POST':
		p = Node.objects.get(pk=request.POST['in_link'])
		c = Node.objects.get(pk=request.POST['out_link'])
		edgeQuery = Edge.objects.filter(parent=p, child=c)
		if edgeQuery:
			edgeQuery[0].comment = request.POST['comment'] # If the edge already exists, change the comment
		else:
			Edge.objects.create(parent=p, child=c, comment=request.POST['comment'])
		return HttpResponseRedirect(reverse('prototype.views.view_thread', args=(p.thread.title,)))
	else:
		return HttpResponseRedirect(reverse('prototype.views.index'))

def clear_edge(request):
	if request.method == 'POST':
		e = Edge.objects.get(pk=request.POST['edge'])
		thread_title = e.parent.thread.title
		e.delete()
		return HttpResponseRedirect(reverse('prototype.views.view_thread', args=(thread_title,)))
	else:
		return HttpResponseRedirect(reverse('prototype.views.index'))

def clear_node(request):
	pass

def clear_thread(request):
	pass

def paper(request, paper_id):
	pass

def author(request, author_name):
	pass