from tastypie.resources import ModelResource
from backend.models import States, Feelings, Tweets, Users
from tastypie import fields

class StatesResource(ModelResource):
    class Meta:
        queryset = States.objects.all()

class FeelingsResource(ModelResource):
    class Meta:
        queryset = Feelings.objects.all()

class UsersResource(ModelResource):
    state = fields.ForeignKey(StatesResource, 'state')
    class Meta:
        queryset = Users.objects.all()

class TweetsResource(ModelResource):
    class Meta:
        queryset = Tweets.objects.all()
