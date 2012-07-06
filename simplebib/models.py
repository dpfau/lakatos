from django.db import models

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

 	def full_title(self):
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
		if len(authorQuery) == 0:
	 		ref = 'Anonymous'
		elif len(authorQuery) == 1:
			ref = authorQuery[0].surname
		elif len(authorQuery) == 2:
			ref = authorQuery[0].surname + ' and ' + authorQuery[1].surname
		else:
			ref = authorQuery[0].surname + ' et al.'
		if self.pub_date is not None:
			ref += ' (' + str(self.pub_date.year) + ')'
		return ref

class Thread(models.Model):
	title = models.CharField(max_length=200)
 	papers = models.ManyToManyField(Paper, through='Node')
 	def __unicode__(self):
 		return self.title

class Node(models.Model):
 	paper = models.ForeignKey(Paper)
 	thread = models.ForeignKey(Thread)
 	abbrev = models.CharField(max_length=60)
 	children = models.ManyToManyField("self", through='Edge', symmetrical=False)
 	def __unicode__(self):
 		if self.abbrev is not None:
	 		return thread.__unicode__() + ': ' + self.abbrev
	 	else:
	 		return thread.__unicode__() + ': ' + paper.__unicode__()
 	# A thought: as defined, this allows us to draw and edge between papers in different threads.  Is that right?

class Edge(models.Model):
 	parent = models.ForeignKey(Node, related_name='out_links')
 	child = models.ForeignKey(Node, related_name='in_links')
 	comment = models.CharField(max_length=200)
 	def __unicode__(self):
 		return self.parent.__unicode__() + ' -> ' + self.child.__unicode__()