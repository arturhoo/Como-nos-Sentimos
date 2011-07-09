from tastypie.resources import ModelResource
from backend.models import Feelings, Tweets, Users


class FeelingsResource(ModelResource):
    class Meta:
        queryset = Feelings.objects.all()
