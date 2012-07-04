from django.db import models

class Author(models.Model):
	forename = models.CharField(max_length=200)
	surname = models.CharField(max_length=200)
	def __unicode__(self):
		self.forename + ' ' + self.surname

class Paper(models.Model):
 	title = models.CharField(max_length=1000)
	uuid = models.CharField(max_length=200, primary_key=True)
 	authors = models.ManyToManyField(Author)
 	pub_date = models.DateField()
 	def __unicode__(self):
 		ref = ''
 		for author in self.authors:
 			ref += author + ', '
 		ref = ref[:-2]
 		ref += ' (' + pub_date.year + '). ' + self.title + '.'

class Thread(models.Model):
 	papers = models.ManyToManyField(Paper, through='Node')

class Node(models.Model):
 	paper = models.ForeignKey(Paper)
 	thread = models.ForeignKey(Thread)
 	abbrev = models.CharField(max_length=60)
 	children = models.ManyToManyField("self", through='Edge', symmetrical=False) 
 	# A thought: as defined, this allows us to draw and edge between papers in different threads.  Is that right?

class Edge(models.Model):
 	parent = models.ForeignKey(Node, related_name='out_links')
 	child = models.ForeignKey(Node, related_name='in_links')
 	comment = models.CharField(max_length=200)