# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Access(models.Model):
    id = models.BigIntegerField(primary_key=True)
    class Meta:
        db_table = u'access'

class Feelings(models.Model):
    id = models.IntegerField(primary_key=True)
    feeling = models.CharField(unique=True, max_length=60, blank=True)
    re = models.CharField(max_length=180, blank=True)
    rgb = models.TextField(blank=True)
    def __unicode__(self):
        return self.feeling
    class Meta:
        db_table = u'feelings'

class Locations(models.Model):
    text = models.CharField(max_length=150, primary_key=True)
    structured = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = u'locations'

class States(models.Model):
    state = models.CharField(max_length=6, primary_key=True)
    state_long = models.CharField(unique=True, max_length=90, blank=True)
    rgb = models.CharField(unique=True, max_length=135, blank=True)
    class Meta:
        db_table = u'states'

class Tweets(models.Model):
    id = models.BigIntegerField(primary_key=True)
    from_user = models.CharField(max_length=60, blank=True)
    text = models.TextField(blank=True)
    sentimento = models.ForeignKey(Feelings, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(blank=True)
    class Meta:
        db_table = u'tweets'

class Users(models.Model):
    screen_name = models.CharField(max_length=60, primary_key=True)
    name = models.TextField(blank=True)
    location = models.TextField(blank=True)
    description = models.TextField(blank=True)
    city = models.TextField(blank=True)
    state = models.ForeignKey(States, null=True, db_column='state', blank=True)
    location_status = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'users'

