from read_api import settings
from tastypie.resources import Resource
from tastypie.authorization import Authorization
from tastypie.fields import DictField
from pymongo import Connection
from copy import copy


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

    def dehydrate(self, bundle):
        return bundle.data['tweet']

    def alter_list_data_to_serialize(self, request, data_dict):
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                # Get rid of the "meta".
                del(data_dict['meta'])
                data_dict['tweets'] = copy(data_dict['objects'])
                del(data_dict['objects'])

        return data_dict

    def _connection(self):
        return Connection(host=settings.MONGO_DATABASES['default']['HOST'])

    def _collection(self):
        db = settings.MONGO_DATABASES['default']['DATABASE']
        collection = settings.MONGO_DATABASES['default']['COLLECTION']
        connection = self._connection()
        return connection[db][collection]

    def get_resource_uri(self, bundle_or_obj):
        kwargs = {
            'resource_name': self._meta.resource_name,
        }

        return self._build_reverse_url("api_dispatch_detail", kwargs=kwargs)

    def custom_get_object_list(self, request, **kwargs):
        collection = self._collection()
        query = collection.find(spec={'feelings': kwargs['filters']['feeling']},
                                limit=50,
                                sort={'created_at': -1})
        results = []
        for result in query:
            new_obj = TweetObject(result)
            results.append(new_obj)

        return results

    def get_object_list(self, request):
        collection = self._collection()
        query = collection.find(limit=50, sort=[('created_at', -1)])
        results = []
        for result in query:
            new_obj = TweetObject(result)
            results.append(new_obj)

        return results

    def obj_get_list(self, request=None, **kwargs):
        filters = {}
        if hasattr(request, 'GET'):
            # Grab a mutable copy.
            filters = request.GET.copy()
        # Update with the provided kwargs.
        filters.update(kwargs)
        if filters.get('feeling'):
            return self.custom_get_object_list(request, filters=filters)
        else:
            return self.get_object_list(request)

    def obj_get(self, request=None, **kwargs):
        return self.get_object_list(request)
