from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class Questions(models.Model):
	"""Table for Options"""
	qns = models.TextField()
	ansId = models.IntegerField()
	day = models.IntegerField()
	selected_ans = models.CharField(max_length = 50, default = 'select')
	def __unicode__(self):
		return "qnId = %s qns = %s ans = %s"%(self.id, self.qns, self.ansId)

class Options(models.Model):
	"""Table for Options"""
	option = models.CharField(max_length = 100)
	qn = models.ForeignKey(Questions)
	def __unicode__(self):
		return "optId = %s opt = %s qnId = %s"%(self.id, self.option, self.qn_id)

class User(models.Model):
	"""Table for user"""		
	email = models.EmailField(max_length = 50)
	name = models.CharField(max_length = 50)
	user_id = models.CharField(max_length= 200)
	image_url = models.URLField(max_length = 200)
	score = models.IntegerField()
	totalTime = models.IntegerField()
	today_score = models.IntegerField()
	start_time = models.IntegerField()
	next_answered_qn = models.IntegerField()
	today_total_time = models.IntegerField()
	
	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ('score', 'totalTime')	
