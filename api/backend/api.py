from tastypie.resources import ModelResource
from backend.models import Feelings, Tweets, Users


class FeelingsResource(ModelResource):
    class Meta:
        queryset = Feelings.objects.all()

class UsersResource(ModelResource):
    class Meta:
        queryset = Users.objects.all()

class TweetsResource(ModelResource):
    class Meta:
        queryset = Tweets.objects.all()
