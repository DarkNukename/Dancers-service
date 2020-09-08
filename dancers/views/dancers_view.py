import logging
from .base_view import BaseView
from ..models import Dancers, Couples
import json

log = logging.getLogger('dancers_log')
couples_log = logging.getLogger('couples_log')


class DancersView(BaseView):

    @BaseView.authorization(('admin', 'anonymous'))
    def get(self, request, client, client_id):
        params = request.GET
        response = list(Dancers.objects.filter(**params).values())
        stat = BaseView.send_stat_log(request, client, client_id)
        if not stat:
            BaseView.log(log, request, client, client_id)
        return {'status': 'Success', 'data': response, 'code': 200}

    @BaseView.authorization(('admin',))
    def post(self, request, client, client_id):
        data = json.loads(request.body.decode('utf-8'))
        response = Dancers.objects.create(**data).pk
        stat = BaseView.send_stat_log(request, client, client_id)
        if not stat:
            BaseView.log(log, request, client, client_id)
        return {'status': 'Success', 'data': response, 'code': 200}

class DancerView(BaseView):

    @BaseView.authorization(('admin', 'anonymous'))
    def get(self, request, uuid, client, client_id):
        response = list(Dancers.objects.filter(pk=uuid).values())
        if not response:
            return {'status': 'Failed', 'message': 'Object does not exist', 'code': 404}
        stat = BaseView.send_stat_log(request, client, client_id)
        if not stat:
            BaseView.log(log, request, client, client_id)
        return {'status': 'Success', 'data': response, 'code': 200}

    @BaseView.authorization(('admin', 'anonymous'))
    def patch(self, request, uuid, client, client_id):
        data = json.loads(request.body.decode('utf-8'))
        Dancers.objects.filter(pk=uuid).update(**data)
        response = list(Dancers.objects.filter(pk=uuid).values())
        stat = BaseView.send_stat_log(request, client, client_id)
        if not stat:
            BaseView.log(log, request, client, client_id)
        return {'status': 'Success', 'data': response, 'code': 200}

    @BaseView.authorization(('admin',))
    def delete(self, request, uuid, client, client_id):
        dancer = Dancers.objects.filter(pk=uuid)
        if dancer[0].couple_uuid:
            couple = Couples.objects.filter(pk=dancer[0].couple_uuid)
            Dancers.objects.filter(pk=couple[0].male).update(couple_uuid="")
            Dancers.objects.filter(pk=couple[0].female).update(couple_uuid="")
            couple.delete()
            BaseView.log(couples_log, request, client, client_id)
        dancer.delete()
        # stat = BaseView.send_stat_log(request, client, client_id)
        # if not stat:
        BaseView.log(log, request, client, client_id)
        return {'status': 'Success', 'code': 200}