from django.db import models
from datetime import date

class Author(models.Model):
	forename = models.CharField(max_length=200)
	surname = models.CharField(max_length=200)
	def __unicode__(self):
		return self.forename + ' ' + self.surname

class Paper(models.Model):
	title = models.CharField(max_length=1000)	
	uuid = models.CharField(max_length=200, primary_key=True)
	authors = models.ManyToManyField(Author)
	pub_date = models.DateField()
	same = models.ForeignKey('Paper', blank=True, null=True, default='', related_name='copies') # Identifier if paper is a copy of another, set in method "merge"

	@staticmethod
	def import_mendeley_paper(document):
		paperQuery = Paper.objects.filter(uuid=document['uuid'])
		if not paperQuery:
			if document['title'] is None or document['year'] is None:
				return None
			p = Paper.objects.create(uuid=document['uuid'], title=document['title'], pub_date=date(document['year'], 1, 1))
			if document['authors'] is not None:
				for author in document['authors']:
					authorQuery = Author.objects.filter(forename=author['forename'], surname=author['surname'])
					if authorQuery:
						p.authors.add(authorQuery[0])
					else:
						a = Author.objects.create(forename=author['forename'], surname=author['surname'])
						p.authors.add(a)
			return p
		else:
			return paperQuery[0]

	def merge(self, p):
 		p.same = self
 		p.save()
 		for q in p.copies.all():
 			q.same = self
 			q.save()

 	def full_title(self):
 		authorQuery = self.authors.all()
 		if not authorQuery:
 			ref = 'Anonymous'
 		else: 
 			ref = ', '.join([author.__unicode__() for author in self.authors.all()])
 		if self.pub_date is not None:
	 		ref += ' (' + str(self.pub_date.year) + '). ' 
	 	else:
	 		ref += '.'
	 	if self.title is not None:
	 		ref += ' ' + self.title + '.'
	 	else:
	 		ref += ' Untitled.'
	 	return ref

	def __unicode__(self):
		authorQuery = self.authors.all()
		if not authorQuery:
	 		ref = 'Anonymous'
		elif len(authorQuery) is 1:
			ref = authorQuery[0].surname
		elif len(authorQuery) is 2:
			ref = authorQuery[0].surname + ' and ' + authorQuery[1].surname
		else:
			ref = authorQuery[0].surname + ' et al.'
		if self.pub_date is not None:
			ref += ' (' + str(self.pub_date.year) + ')'
		return ref

class Thread(models.Model):
	title = models.CharField(max_length=200, primary_key=True)
 	papers = models.ManyToManyField(Paper, through='Node')
 	def __unicode__(self):
 		return self.title.replace('_', ' ')

class Node(models.Model):
 	paper = models.ForeignKey(Paper)
 	thread = models.ForeignKey(Thread)
 	abbrev = models.CharField(max_length=60)
 	children = models.ManyToManyField("self", through='Edge', symmetrical=False)
 	def __unicode__(self):
 		if self.abbrev is None or len(self.abbrev) is 0:
 	 		return self.thread.__unicode__() + ': ' + self.paper.__unicode__()
	 	else:
	 		return self.thread.__unicode__() + ': ' + self.abbrev
 	# A thought: as defined, this allows us to draw and edge between papers in different threads.  Is that right?

class Edge(models.Model):
 	parent = models.ForeignKey(Node, related_name='out_links')
 	child = models.ForeignKey(Node, related_name='in_links')
 	comment = models.CharField(max_length=200)
 	def __unicode__(self):
 		return self.parent.__unicode__() + ' -> ' + self.child.__unicode__()