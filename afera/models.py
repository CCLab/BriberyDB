from django.db import models

# Create your models here.

class Type (models.Model):

  name = models.CharField(max_length=128)
  
  def __unicode__ (self):
    return self.name
  

class Scandal (models.Model):

  type = models.ForeignKey(Type)
  subtype = models.ForeignKey(Type)
  consequence = models.CharField (max_length=128)
  description = models.TextField ()
  background = models.TextField  ()
  
  def __unicode__ (self):
    return unicode(Title.models.filter(scandal__exact=self)[0])
  

class Title (models.Model):

  scandal = models.ForeignKey (Scandal)
  title = models.CharField (max_length=128)
  
  def __unicode__ (self):
    return self.title
    
class Tag (models.Model):

  tag      = models.CharField (max_length=128)
  scandals = models.ManyToManyField (Scandal)
  
  def __unicode__ (self):
    return self.tag


class Event (models.Model):

  scandal          = models.ForeignKey (Scandal)
  type             = models.ForeignKey (EventType)
  title            = models.CharField (max_length=128)
  date             = models.DateField (auto_add=False)
  publication_date = models.DateField ()
  description      = models.TextField ()
