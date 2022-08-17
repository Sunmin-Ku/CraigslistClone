from django.db import models

# Create your models here.
class Search(models.Model):
    search = models.CharField(max_length=500) # just take input for 500 char lengths
    created = models.DateTimeField(auto_now=True)
    # search database ---> create search and created

    def __str__(self):
        return '{}'.format(self.search) # instead of search object, appear as what I search

    class Meta:
        verbose_name_plural = 'Searches'