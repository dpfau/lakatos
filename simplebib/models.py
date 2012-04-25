from django.db import models

class Paper(models.Model):
	title = models.CharField(max_length=1000)
	uuid = models.CharField(max_length=200)
	authors = models.ManyToManyField(Author)
	pub_date = models.DateField()

class Author(models.Model):
	forename = models.CharField(max_length=200)
	surname = models.CharField(max_length=200)