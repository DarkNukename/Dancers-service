import logging
from .base_view import BaseView
from ..models import Couples, Dancers
import json

log = logging.getLogger('couples_log')


class CouplesView(BaseView):

    @BaseView.authorization(('admin', 'anonymous'))
    def get(self, request, client, client_id):
        params = request.GET
        response = list(Couples.objects.filter(**params).values())
        BaseView.log(log, request, client, client_id)
        return {'status': 'Success', 'data': response, 'code': 200}

    @BaseView.authorization(('admin', 'anonymous'))
    def post(self, request, client, client_id):
        data = json.loads(request.body.decode('utf-8'))
        response = Couples.objects.create(**data).pk

        for key, value in data.items():
            Dancers.objects.filter(pk=value).update(couple_uuid=response)

        BaseView.log(log, request, client, client_id)
        return {'status': 'Success', 'data': response, 'code': 200}

class CoupleView(BaseView):

    @BaseView.authorization(('admin', 'anonymous'))
    def get(self, request, uuid, client, client_id):
        response = list(Couples.objects.filter(pk=uuid).values())
        if not response:
            return {'status': 'Failed', 'message': 'Object does not exist', 'code': 404}
        BaseView.log(log, request, client, client_id)
        return {'status': 'Success', 'data': response, 'code': 200}


    @BaseView.authorization(('admin', 'anonymous'))
    def delete(self, request, uuid, client, client_id):
        entry = Couples.objects.filter(pk=uuid)
        Dancers.objects.filter(pk=entry[0].male).update(couple_uuid=None)
        Dancers.objects.filter(pk=entry[0].female).update(couple_uuid=None)
        entry.delete()
        BaseView.log(log, request, client, client_id)
        return {'status': 'Success', 'code': 200}