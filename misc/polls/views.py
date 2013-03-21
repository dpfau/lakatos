from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from polls.models import Poll, Choice

def votes(request, poll_id):
	p = get_object_or_404(Poll, pk=poll_id)
	try:
		selected_choices = p.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render_to_response('polls/details.html', {
			'poll': p,
			'error_message': "You didn't select a chocie.",
		}, context_instance=RequestContext(request))
	else:
		selected_choices.votes += 1
		selected_choices.save()
		return HttpResponseRedirect(reverse('poll_results', args=(p.id,)))