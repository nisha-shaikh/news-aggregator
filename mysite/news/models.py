from django.db import models

# Create your models here.
class SearchRequests(models.Model):
    query = models.CharField(max_length=250, primary_key=True)
    dateAdded = models.DateField()

class SearchResults(models.Model):
    headline = models.TextField()
    link = models.URLField()
    source = models.CharField(max_length=50)
    request = models.ManyToManyField(SearchRequests)