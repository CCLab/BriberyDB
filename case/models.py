from django.db import models

# Create your models here.

class Type (models.Model):

  name = models.CharField(max_length=128)
  

class Scandal (models.Model):

  type = models.ForeignKey(Type)
  subtype = models.ForeignKey(Type)
  consequence = models.CharField(max_length=128)
  description = models.TextField()
  

class Title (models.Model):

  scandal = models.ForeignKey (Scandal)
  
class Tag (models.Model):

  tag      = models.CharField (max_length=128)
  scandals = models.ManyToManyField (Scandal)

class Event (models.Model):

  scandal = models.ForeignKey (Scandal)
