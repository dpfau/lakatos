from django.db import models

class Paper(models.Model):
	title = models.CharField(max_length=1000)
	uuid = models.CharField(max_length=200)
	authors = models.ManyToManyField(Author)
	pub_date = models.DateField()

class Author(models.Model):
	forename = models.CharField(max_length=200)
	surname = models.CharField(max_length=200)

class Thread(models.Model):
	pass

class PaperInThread(models.Model):
	paper = models.ForeignKey(Paper)
	thread = models.ForeignKey(Thread)
	abbrev = models.CharField(max_length=60)
	edge = models.ManyToManyField("self",through=EdgeInThread,symmetrical=False)

class EdgeInThread(models.Model):
	pass