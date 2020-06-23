import datetime
import requests
import logging
import http.client
from json.decoder import JSONDecodeError
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


if settings.DEBUG:
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    http.client.HTTPConnection.debuglevel = 1


class Algorithm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    filename = models.CharField(max_length=255)
    text = models.TextField()
    metrics = models.CharField(max_length=100, default="")
    status = models.CharField(max_length=100, default="")
    run_id = models.CharField(max_length=100, default="")
    mdate = models.DateTimeField("Modify Date", auto_now=True)
    cdate = models.DateTimeField("Create Date", default=datetime.datetime.now)


class AlgoSym(requests.Session):

    def prepare(self):
        self.headers.update({
            "accept": "application/json",
        })

    @staticmethod
    def __json(resp):
        _json = None
        if resp.status_code == 200:
            try:
                _json = resp.json()
            except JSONDecodeError:
                pass
        else:
            _json = {"error": resp.text, "code": resp.status_code}
        return _json

    def run(self, user, algorithm):
        self.prepare()
        data = {
            "userId": user.email,
            "userAlgoName": algorithm.filename,
        }
        files = {"code": (algorithm.filename, algorithm.text)}
        resp = self.post(settings.ALGOSYM_URL + "/algoCode",
                         auth=settings.ALGOSYM_AUTH, data=data, files=files)

        return self.__json(resp)

    def status(self, user, algorithm):
        self.prepare()
        resp = self.get(settings.ALGOSYM_URL + "/algoStatus/" + algorithm.run_id,
                        auth=settings.ALGOSYM_AUTH)

        return self.__json(resp)

