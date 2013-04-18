from django.db import models
from datetime import datetime

class User(models.Model):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)
     
    def __unicode__(self):
        return u'%s %s %s' % (self.username, self.email, self.password) 

class Poll(models.Model):
    user = models.ForeignKey(User)
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return u'question:%s pub_date:%s' % (self.question, self.pub_date) 
    
class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(max_length=200)
    image_url = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __unicode__(self):
        return u'choice_text:%s image_url:%s' % (self.choice_text, self.image_url)


