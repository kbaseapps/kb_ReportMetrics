# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
import requests

from os import environ
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from pprint import pprint, pformat  # noqa: F401

#from biokbase.catalog.Client import Catalog
from biokbase.workspace.client import Workspace as workspaceService
from kb_ReportMetrics.kb_ReportMetricsImpl import kb_ReportMetrics
from kb_ReportMetrics.kb_ReportMetricsServer import MethodContext
from kb_ReportMetrics.authclient import KBaseAuth as _KBaseAuth
from kb_Metrics.kb_MetricsClient import kb_Metrics

class kb_ReportMetricsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('kb_ReportMetrics'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'kb_ReportMetrics',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(cls.wsURL)
        cls.serviceImpl = kb_ReportMetrics(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']
	cls.srv_wiz_url = cls.cfg['srv-wiz-url']


    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def getContext(self):
        return self.__class__.ctx

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    # Uncomment to skip this test
    #for testing to kb_Metrics service
    #@unittest.skip("skipped test_sscce")
    def test_sscce(self):
	met_client = kb_Metrics(url='https://ci.kbase.us/dynserv/a57e748e729233bd03ae77686925a541f40a7376.kb-Metrics', token=environ.get('KB_AUTH_TOKEN', None),service_ver='beta')
	ret_metrics = met_client.get_app_metrics({})

