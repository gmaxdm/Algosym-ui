import datetime
import requests
import logging
import http.client
from json.decoder import JSONDecodeError
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
http.client.HTTPConnection.debuglevel = 1


class Algorithm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    filename = models.CharField(max_length=255)
    text = models.TextField()
    metrics = models.CharField(max_length=100)
    mdate = models.DateTimeField("Modify Date", auto_now=True)
    cdate = models.DateTimeField("Create Date", default=datetime.datetime.now)


class AlgoSym(requests.Session):

    def run(self, user, algorithm):
        self.headers.update({
            "accept": "application/json",
            "Content-Type": "multipart/form-data",
        })
        data = {
            "userId": settings.ALGOSYM_AUTH[0],
            "userAlgoName": algorithm.filename,
        }
        files = {"file": (algorithm.filename, algorithm.text)}
        resp = self.post(settings.ALGOSYM_URL + "/algoCode",
                         auth=settings.ALGOSYM_AUTH, data=data, files=files)
        logger.debug(resp)
        logger.debug(resp.headers)
        try:
            _json = resp.json()
        except JSONDecodeError:
            _json = None
        return _json

