from tastypie.resources import ModelResource
from backend.models import States, Feelings, Tweets, Users
from tastypie import fields

class StatesResource(ModelResource):
    class Meta:
        queryset = States.objects.all()
        include_resource_uri = False

class FeelingsResource(ModelResource):
    class Meta:
        queryset = Feelings.objects.all()
        include_resource_uri = False

class SimpleFeelingsResource(ModelResource):
    class Meta:
        queryset = Feelings.objects.all()
        include_resource_uri = False
    def dehydrate(self, bundle):
        return bundle.data['id']

class UsersResource(ModelResource):
    class Meta:
        queryset = Users.objects.all()
        include_resource_uri = False

class TweetsResource(ModelResource):
    sentimento = fields.ForeignKey(SimpleFeelingsResource, 'sentimento', full=True)
    class Meta:
        queryset = Tweets.objects.all()
        include_resource_uri = False
