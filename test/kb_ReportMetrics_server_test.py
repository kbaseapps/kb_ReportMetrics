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
	"""
	for testing to kb_Metrics service
	cls.met_client = kb_Metrics(url='https://ci.kbase.us/dynserv/a57e748e729233bd03ae77686925a541f40a7376.kb-Metrics', service_ver='beta')
	cls.ret_metrics = cls.met_client.get_app_metrics({
                 'user_ids': ['qzhang'],
                 'epoch_range': (1420083768000,1435677602000)
        })
	"""

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        if hasattr(self.__class__, 'wsName'):
            return self.__class__.wsName
        suffix = int(time.time() * 1000)
        wsName = "test_kb_ReportMetrics_" + str(suffix)
        ret = self.getWsClient().create_workspace({'workspace': wsName})  # noqa
        self.__class__.wsName = wsName
        return wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    # Uncomment to skip this test
    @unittest.skip("skipped test_run_count_ncbi_genomes")
    def test_run_count_ncbi_genomes(self):
        # First set input parameters
        m_params = {
            'workspace_name': self.getWsName(),
            'genome_source': 'refseq',
            'genome_domain': 'fungi',#'archaea',#'bacteria','plant','fungi'
            'refseq_category': 'reference', #'reference','representative','na',
            'create_report': 1
        }
        # Second, call your implementation
        ret = self.getImpl().count_ncbi_genomes(self.getContext(), m_params)


    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    # Uncomment to skip this test
    @unittest.skip("skipped test_run_count_genome_features")
    def test_run_count_genome_features_from_files(self):
        # First set input parameters
        m_params =     {
            'workspace_name': self.getWsName(),
            'genome_file_urls': ['ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/009/605/GCF_000009605.1_ASM960v1/GCF_000009605.1_ASM960v1_genomic.gbff.gz','ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/008/725/GCF_000008725.1_ASM872v1/GCF_000008725.1_ASM872v1_genomic.gbff.gz','ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/009/605/GCF_000009605.1_ASM960v1/GCF_000009605.1_ASM960v1_genomic.gbff.gz'],
            'create_report': 1
        }
        # Second, call your implementation
        ret = self.getImpl().count_genome_features_from_files(self.getContext(), m_params)


    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    # Uncomment to skip this test
    @unittest.skip("skipped test_run_count_ncbi_genome_features")
    def test_run_count_ncbi_genome_features(self):
        # First set input parameters
        m_params =     {
            'workspace_name': self.getWsName(),
            'genome_file_urls': [],
            'genome_source': 'refseq',
            'genome_domain': 'bacteria',#'archaea',#'bacteria','plant','fungi'
            'refseq_category': 'reference',#'representative','na',
            'create_report': 1
        }
        # Second, call your implementation
        ret = self.getImpl().count_ncbi_genome_features(self.getContext(), m_params)


    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    # Uncomment to skip this test
    @unittest.skip("skipped test_run_count_ensemblgenome_features")
    def test_run_count_ensemblgenome_features(self):
        # First set input parameters
        m_params =     {
            'workspace_name': self.getWsName(),
            'genome_file_urls': ['ftp.ensemblgenomes.org/pub/release-37/plants/genbank/corchorus_capsularis/Corchorus_capsularis.CCACVL1_1.0.37.nonchromosomal.dat.gz'],
            'create_report': 0
        }
        # Second, call your implementation
        ret = self.getImpl().count_genome_features_from_files(self.getContext(), m_params)


    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    # Uncomment to skip this test
    @unittest.skip("skipped test_run_eummy_test")
    def test_run_dummy_test(self):
        m_params = {
            'stats_name': 'app_stats',#'user_job_states',
            'user_ids':['qzhang'],#'user_ids': [],
            'epoch_range':(1420083768000,1435677602000),#(datetime.datetime(2015, 1, 1), datetime.datetime(2015,6,30)
            'workspace_name': self.getWsName(),
            'create_report': 0
        }
        # Second, call your implementation
        ret = self.getImpl().dummy_test0(self.getContext(), m_params)
        print(ret[0])

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    # Uncomment to skip this test
    #@unittest.skip("skipped test_run_report_metrics")
    def test_run_report_metrics(self):
        m_params = {
            'stats_name': 'user_ws',#user_details','app_stats''exec_stats','exec_aggr_table','exec_stats','exec_aggr_stats','user_job_states'
            'user_ids':[],#['qzhang'],#'user_ids': [],
            'epoch_range':(1420083768000,1435677602000),#(datetime.datetime(2015, 1, 1), datetime.datetime(2015,6,30)
            #'epoch_range':(1420083768000,1451606549000)#(datetime.datetime(2015, 1, 1), datetime.datetime(2016,1,1)
            'workspace_name': self.getWsName(),
            'create_report':1 
        }
        # Second, call your implementation
        ret = self.getImpl().report_metrics(self.getContext(), m_params)
        print(pformat(ret[0]))

