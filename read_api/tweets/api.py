from tastypie.resources import Resource
from tastypie.authorization import Authorization
from tastypie.fields import DictField, CharField
from tastypie.bundle import Bundle
from pymongo import Connection


class TweetObject(object):
    def __init__(self, tweet):
        self.tweet = tweet


class TweetsResource(Resource):
    tweet = DictField(attribute='tweet')

    class Meta:
        resource_name = 'tweets'
        object_class = TweetObject
        authorization = Authorization()
        include_resource_uri = False
        limit = 30
        max_limit = None

    def _connection(self):
            return Connection()

    def _collection(self):
            connection = self._connection()
            return connection.cns.tweets

    def get_resource_uri(self, bundle_or_obj):
        kwargs = {
            'resource_name': self._meta.resource_name,
        }

        return self._build_reverse_url("api_dispatch_detail", kwargs=kwargs)

    def get_object_list(self, request):
        collection = self._collection()
        query = collection.find()
        results = []
        for result in query:
            new_obj = TweetObject(result)
            results.append(new_obj)

        return results

    def obj_get_list(self, request=None, **kwargs):
        # Filtering disabled for brevity...
        return self.get_object_list(request)

    def obj_get(self, request=None, **kwargs):
        return self.get_object_list(request)
