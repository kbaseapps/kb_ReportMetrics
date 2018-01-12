import time
import datetime
import dateutil.parser
import pytz
import json
import os
import re
import copy
import uuid
import shutil
import sys
from pprint import pprint, pformat
from urllib2 import Request, urlopen
from urllib2 import URLError, HTTPError
import urllib
import errno

from Bio import Entrez, SeqIO
from numpy import median, mean, max

from Workspace.WorkspaceClient import Workspace as Workspace
from Catalog.CatalogClient import Catalog
from NarrativeJobService.NarrativeJobServiceClient import NarrativeJobService
from UserAndJobState.UserAndJobStateClient import UserAndJobState
from UserProfile.UserProfileClient import UserProfile
from kb_Metrics.kb_MetricsClient import kb_Metrics


def log(message, prefix_newline=False):
    """Logging function, provides a hook to suppress or redirect log messages."""
    print(('\n' if prefix_newline else '') + '{0:.2f}'.format(time.time()) + ': ' + str(message))


def _mkdir_p(path):
    """
    _mkdir_p: make directory for given path
    """
    if not path:
        return
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def ceildiv(a, b):
    """
    celldiv: get the ceiling division of two integers, by reversing the floor division
    """
    return -(-a // b)

def _datetime_from_utc(date_utc_str):
    try:#for u'2017-08-27T17:29:37+0000'
        dt = datetime.datetime.strptime(date_utc_str,'%Y-%m-%dT%H:%M:%S+0000')
    except ValueError as v_er:#for ISO-formatted date & time, e.g., u'2015-02-15T22:31:47.763Z'
        dt = datetime.datetime.strptime(date_utc_str,'%Y-%m-%dT%H:%M:%S.%fZ')
    return dt

def _timestamp_from_utc(date_utc_str):
    dt = _datetime_from_utc(date_utc_str)
    return int(time.mktime(dt.timetuple())*1000) #in microseconds

def _convert_to_datetime(dt):
    new_dt = dt
    if (not isinstance(dt, datetime.date) and not isinstance(dt, datetime.datetime)):
        if isinstance(dt, int):
            new_dt = datetime.datetime.utcfromtimestamp(dt / 1000)
        else:
            new_dt = _datetime_from_utc(dt)
    return new_dt

def _unix_time_millis_from_datetime(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    return int((dt - epoch).total_seconds()*1000)


class UJS_CAT_NJS_DataUtils:

    def __init__(self, workspace_url, job_service_url, srv_wiz_url,
		njsw_url, auth_service_url, kbase_endpoint, provenance, token):
        self.workspace_url = workspace_url
        self.job_service_url = job_service_url
        self.njsw_url = njsw_url
        self.auth_service_url = auth_service_url
	self.srv_wiz_url = srv_wiz_url
	self.catalog_url = kbase_endpoint + '/catalog'
	self.user_profile_url = kbase_endpoint + '/user_profile/rpc'
        self.provenance = provenance

        #initialize service clients
        self.ws_client = Workspace(self.workspace_url)
        self.cat_client = Catalog(self.catalog_url, auth_svc=self.auth_service_url)
        self.njs_client = NarrativeJobService(self.njsw_url, auth_svc=self.auth_service_url)
        self.ujs_client = UserAndJobState(self.job_service_url, auth_svc=self.auth_service_url)
        self.uprf_client = UserProfile(self.user_profile_url, auth_svc=self.auth_service_url)
        #self.met_client = kb_Metrics(self.srv_wiz_url, token=token, auth_svc=self.auth_service_url)
	self.met_url = 'https://ci.kbase.us/dynserv/a57e748e729233bd03ae77686925a541f40a7376.kb-Metrics'
        self.met_client = kb_Metrics(url=self.met_url, auth_svc=self.auth_service_url, token=token)


    def get_app_metrics(self, input_params):
        """
        get_app_metrics: call the dynamic service kb_Metrics to retrieve app metrics
        and return the following data structure, e.g.,
	[{
	u'app_id': u'kb_ReportMetrics/count_genome_features_from_files',
	u'authparam': u'27951',
	u'authstrat': u'kbaseworkspace',
	u'client_groups': [u'njs'],
	u'complete': True,
	u'created': 1515173864675,
	u'creation_time': 1515173864675,
	u'desc': u'Execution engine job for kb_ReportMetrics.count_genome_features_from_files',
	u'error': False,
	u'errormsg': None,
	u'estcompl': None,
	u'exec_start_time': 1515173873601,
	u'finish_time': 1515173991461,
	u'job_id': u'5a4fb7e8e4b0c23d90df55bf',
	u'job_input': {
		u'app_id': u'kb_ReportMetrics/count_genome_features_from_files',
		u'meta': {u'cell_id': u'6620f8a8-e464-491a-973e-d717cde08847',
			u'run_id': u'705ca618-1432-4a37-b43b-5c4d736fbdfb',
			u'tag': u'beta',
			u'token_id': u'3608feea-7b98-4ad9-8430-472bc67e6c74'},
		u'method': u'kb_ReportMetrics.count_genome_features_from_files',
		u'params': [{u'create_report': 1,
			u'genome_file_urls': [u'ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/009/605/GCF_000009605.1_ASM960v1/GCF_000009605.1_ASM960v1_genomic.gbff.gz',
				u'ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/008/725/GCF_000008725.1_ASM872v1/GCF_000008725.1_ASM872v1_genomic.gbff.gz',
			u'ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/009/605/GCF_000009605.1_ASM960v1/GCF_000009605.1_ASM960v1_genomic.gbff.gz'],
			u'workspace_name': u'qzhang:narrative_1515016322184'}],
		u'requested_release': None,
		u'service_ver': u'931c6e7a90a9cf99c8c480edeb3ea461ea0a2f60',
		u'wsid': 27951},
	u'job_output': {
		u'id': u'18552903324',
		u'result': [{u'report_name': u'kb_Metrics_report_26006057-d85a-4317-a1d6-bba0f7bd291a',
			u'report_ref': u'27951/79/1'}],
		u'version': u'1.1'},
	u'job_state': u'completed',
	u'maxprog': None,
	u'meta': [{u'k': u'cell_id',
		u'v': u'6620f8a8-e464-491a-973e-d717cde08847'},
		{u'k': u'run_id', u'v': u'705ca618-1432-4a37-b43b-5c4d736fbdfb'},
		{u'k': u'tag', u'v': u'beta'},
		{u'k': u'token_id',
		u'v': u'3608feea-7b98-4ad9-8430-472bc67e6c74'}],
	u'method': u'kb_ReportMetrics.count_genome_features_from_files',
	u'modification_time': 1515173991461,
	u'prog': 0,
	u'progtype': u'none',
	u'results': {u'shocknodes': None,
			u'shockurl': None,
			u'workspaceids': None,
			u'workspaceurl': None},
	u'run_time': 117860,
	u'service': u'qzhang',
	u'started': 1515173873601,
	u'status': u'done',
	u'time_info': [1515173864675, 1515173991461, None],
	u'updated': 1515173991461,
	u'user': u'qzhang',
	u'wsid': u'27951'},
	...
	]
        """
        #log("Fetching the metrics data")
        ret_metrics = []
        params = self.process_met_parameters(input_params)
        user_ids = params['user_ids']
        time_start = params['minTime']
        time_end = params['maxTime']
        try:
            ret_metrics = self.met_client.get_app_metrics({})
                #'user_ids': user_ids,
                #'epoch_range': (time_start, time_end)
            #})
        except Exception as e_met: #RuntimeError
            log('kb_Metrics.get_app_metrics raised error:')
            log(e_met)
            return []
	else: #no exception raised, process the data returned from the service call
		log(pformat(ret_metrics[0]))
		return ret_metrics

    def generate_app_metrics_from_ujs(self, input_params):#, token):
        """
        generate_app_metrics: get app job state data with structure as the following example:
        [
         {'app_id': u'kb_Metrics/refseq_genome_counts',
          'canceled': 0,
          'creation_time': 1510159439977,
          'error': 0,
          'exec_start_time': 1510159441720,
          'finish_time': 1510159449612,
          'finished': 1,
          'job_desc': u'Execution engine job for kb_Metrics.refseq_genome_counts',
          'job_id': u'5a03344fe4b088e4b0e0e370',
          'job_state': u'completed',
          'method': u'refseq_genome_counts',
          'module': u'kb_Metrics',
          'result': [{u'report_name': u'kb_Metrics_report_f97f0567-fee5-48ea-8fc5-1f5e361ee2bd',
                      u'report_ref': u'25735/121/1'}],
          'run_time': '0:00:08',
          'stage': u'complete',
          'status': u'done',
          'time_info': [u'2017-11-08T16:44:01+0000',
                        u'2017-11-08T16:44:09+0000',
                        None],
          'user_id': u'qzhang',
          'wsid': 25735},
         {'app_id': u'RAST_SDK/annotate_contigset',
          'canceled': 0,
          'creation_time': 1485974151389,
          'error': 0,
          'exec_start_time': 1485974156377,
          'finish_time': 1485974703341,
          'finished': 1,
          'job_desc': u'Execution engine job for RAST_SDK.annotate_genome',
          'job_id': u'58922a87e4b0c1af1bf0981b',
          'job_state': u'completed',
          'method': u'annotate_genome',
          'module': u'RAST_SDK',
          'result': [{u'id': u'Pantoea.ananatis_contigs_beta_out',
                      u'report_name': u'Pantoea.ananatis_contigs_beta_out.report',
                      u'report_ref': u'19268/62/1',
                      u'workspace': u'qzhang:narrative_1485914570215',
                      u'ws_report_id': u'Pantoea.ananatis_contigs_beta_out.report'}],
          'run_time': '0:09:07',
          'stage': u'complete',
          'status': u'done',
          'time_info': [u'2017-02-01T18:35:56+0000',
                        u'2017-02-01T18:45:03+0000',
                        None],
          'user_id': u'qzhang',
          'wsid': 19268},
          ......
        ]
        """
        params = self.process_app_parameters(input_params)
        user_ids = params['user_ids']
        time_start = params['time_start']
        time_end = params['time_end']
        job_stage = params['job_stage']

        ws_owners, ws_ids = self.get_user_workspaces(user_ids, time_start, time_end, 0, 0)
        ujs_ret = self.get_user_and_job_states(ws_ids)
        total_ujs_count = len(ujs_ret)
        #log("Before time_stage filter:{}".format(total_ujs_count))

        jt_filtered_ujs = self.filterUJS_by_time_stage(ujs_ret, job_stage, time_start, time_end)
        period_ujs_count = len(jt_filtered_ujs)
        jt_filtered_ujs = self.convert_time_info(jt_filtered_ujs)
        #log("After time_stage filter:{}".format(period_ujs_count))
        #user_grouped_ujs = self.group_by_user(jt_filtered_ujs, user_ids)
        return {'job_states':jt_filtered_ujs}


    def get_user_workspaces(self, user_ids, st_time, ed_time, showDeleted=0, showOnlyDeleted=0):
        """
        get_user_workspaces: given the user ids, get a list of data structure as the example below:
        typedef tuple<ws_id id,
              ws_name workspace,
              username owner,
              timestamp moddate,
              int max_objid,
              permission user_permission,
              permission globalread,
              lock_status lockstat,
              usermeta metadata> workspace_info;

        ws_info = self.ws_client.list_workspace_info({'owners':user_ids,
                        'showDeleted': showDeleted,
                        'showOnlyDeleted': showOnlyDeleted,
                        'perm':'r',
                        'excludeGlobal': 1,
                        'after': '2017-04-03T08:56:32Z',
                        'before': '2017-11-03T08:56:32Z'
                })

        return a list of ws_owners and ws_ids
        """
        #log("Fetching workspace ids for {} users:\n{}".format('the' if user_ids else 'all', user_ids if user_ids else ''))
        #ws_info = self.ws_client.list_workspace_info({})
        ws_info = self.ws_client.list_workspace_info({'owners':user_ids,
                        'showDeleted': showDeleted,
                        'showOnlyDeleted': showOnlyDeleted,
                        'perm':'r',
                        'after': st_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                        'before': ed_time.strftime("%Y-%m-%dT%H:%M:%SZ")
                })

        #log(pformat(ws_info))
        ws_ids = [ws[0] for ws in ws_info]
        ws_owners = [ws[2] for ws in ws_info]

        return (ws_owners, ws_ids)

    def get_user_and_job_states(self, ws_ids):
        """
        get_user_and_job_states: Get the user and job info for the given workspaces
        """
        #log("Fetching the job data...for these workspaces:\n{}".format(pformat(ws_ids)))

        wsj_states = []
        clnt_groups = self.get_client_groups_from_cat()
        counter = 0
        while counter < len(ws_ids) // 10:
            j_states = []
            wid_slice = ws_ids[counter * 10 : (counter + 1) * 10]
            wsj_states += self.retrieve_user_job_states(wid_slice, clnt_groups)
            counter += 1

        wsj_states += self.retrieve_user_job_states(ws_ids[counter * 10: ], clnt_groups)
        #log(pformat(wsj_states[0]))

        return wsj_states


    def retrieve_user_job_states(self, wid_p, c_groups):
        """
        call ujs_client.list_jobs2() that returns an array of job_info2:
        typedef tuple<job_id job, user_info users, service_name service,
                job_stage stage, job_status status, time_info times,
                progress_info progress, boolean complete, boolean error,
                auth_info auth, usermeta meta, job_description desc, Results res>
                job_info2;

        retrieve_user_job_states: returns an array of required data items about user_and_job states
        """
        #log("Fetching the ujs data for workspace(s) {}...".format(pformat(wid_p)))
        ret_ujs = []
        try:
            nar_jobs = self.ujs_client.list_jobs2({
                'filter': 'S',#all jobs are returned
                'authstrat': 'kbaseworkspace',
                'authparams': wid_p
            })
        except Exception as e_ujs: #RuntimeError as e_ujs:
            log('UJS list_jobs2 raised error:\n')
            log(pformat(e_ujs))
            return []
        else:#no exception raised
            if (nar_jobs and len(nar_jobs) > 0):
                #******The ujs_client.list_jobs2({...}) returns a 13 member tuple:*****#
                job_ids = [j[0] for j in nar_jobs]#[u'59f36d00e4b0fb0c767100cc',...]
                job_user_info = [j[1] for j in nar_jobs]#[[u'qzhang', None],[u'qzhang', u'qzhang'],...]
                job_owners = [j[2] for j in nar_jobs]#[u'qzhang',u'qzhang',...]
                job_stages = [j[3] for j in nar_jobs]#One of 'created', 'started', 'complete', 'canceled' or 'error'
                job_status = [j[4] for j in nar_jobs]##[u'done','running','canceled by user','......',...]
                job_time_info = [j[5] for j in nar_jobs]#tuple<timestamp started, timestamp last_update,timestamp est_complete>[[u'2017-10-27T17:29:37+0000', u'2017-10-27T17:29:42+0000', None],...]
                job_progress_info = [j[6] for j in nar_jobs]#tuple<total_progress prog, max_progress max, progress_type ptype>
                job_complete = [j[7] for j in nar_jobs]#[1,1,...,0,..]
                job_error = [j[8] for j in nar_jobs]#[1,0,...,0,..]
                job_auth_info = [j[9] for j in nar_jobs]#[[u'kbaseworkspace', u'25735'],...]
                job_meta = [j[10] for j in nar_jobs]#[{u'cell_id': u'828d2e3c-5c5d-4c4c-9de8-4aacb875c074',u'run_id': u'a05df5b3-2d3e-4e4a-9a32-173acaa9bd0c',u'tag': u'beta',u'token_id': u'2dea84eb-8f40-4516-b18e-f284cc6bb107'},...]
                job_desc = [j[11] for j in nar_jobs]#[u'Execution engine job for kb_Metrics.count_ncbi_genome_features',...]
                job_res = [j[12] for j in nar_jobs]#[{},None,...]

                ret_ujs = self.retrieve_ujs_via_njs(c_groups, job_ids, job_owners,
                                job_stages, job_status, job_time_info, job_error, job_desc)

        return ret_ujs

    def retrieve_ujs_via_njs(self, c_groups, job_ids, job_owners, job_stages,
                        job_status, job_time_info,job_error, job_desc):
        ujs_ret = []
        try:
            #log("Calling njs.check_jobs for {} jobs".format(len(job_ids)))
            job_info = self.njs_client.check_jobs({
                        'job_ids': job_ids, 'with_job_params': 1
                })
        except Exception as e_njs: #RuntimeError as e_njs:
            log('NJS check_jobs raised error:\n')
            log(pformat(e_njs))
            return []
        else:#no exception raised
            job_states = job_info.get('job_states', {})
            job_params = job_info.get('job_params', {})
            job_errors = job_info.get('check_error', {})

            # Retrieve the interested data from job_states to assemble an array of job states
            #for j_id, j_owner in zip(job_ids, job_owners):
            for j_idx, jb_id in enumerate(job_ids):
                jbs = job_states.get(job_ids[j_idx], {})
                jbp = job_params.get(job_ids[j_idx], {})
                u_j_s = {}
                u_j_s['job_id'] = job_ids[j_idx]
                u_j_s['user_id'] = job_owners[j_idx]
                u_j_s['status'] = job_status[j_idx]
                u_j_s['stage'] = job_stages[j_idx]
                u_j_s['time_info'] = job_time_info[j_idx]
                u_j_s['error'] = job_error[j_idx]
                u_j_s['job_desc'] = job_desc[j_idx]

                if jbs:
                    try:
                        u_j_s['app_id'] = jbp['app_id']
                        for clnt in c_groups:
                            if u_j_s['app_id'] == clnt['app_id']:
                                u_j_s['client_groups'] = clnt['client_groups']
                                break
                        u_j_s['wsid'] = jbp['wsid']
                        u_j_s['module'], u_j_s['method'] = jbp['method'].split('.')
                        u_j_s['job_state'] = jbs['job_state']
                        if jbs['job_state'] == 'suspend':
                            u_j_s['error'] = jbs['error']
                        elif (jbs['job_state'] == 'completed' and 'result' in u_j_s):
                            u_j_s['result'] = jbs['result']

                        u_j_s['finished'] = jbs['finished']
                        u_j_s['canceled'] = jbs['canceled']
                        u_j_s['creation_time'] = jbs['creation_time']
                        if 'exec_start_time' in jbs:
                            u_j_s['exec_start_time'] = jbs['exec_start_time']
                        elif u_j_s['stage'] == 'started':
                            u_j_s['exec_start_time'] = u_j_s['time_info'][1]
                        if 'finish_time' in jbs:
                            u_j_s['finish_time'] = jbs['finish_time']
                        elif (u_j_s['stage'] == 'completed' or u_j_s['stage'] == 'complete'):
                            u_j_s['finish_time'] = u_j_s['time_info'][1]
                    except KeyError as e_key:
                        log("KeyError for " + pformat(e_key))
                    else:
                        pass
                else:
                    #log("No job state info is returned by njs for job with id {}".format(job_ids[j_idx]))
                    #log("\nBut maybe ujs has returned something for job with id {}".format(job_ids[j_idx]))
                    #log(pformat(job_stages[j_idx]))
                    u_j_s['creation_time'] = _timestamp_from_utc(u_j_s['time_info'][0])
                    if (u_j_s['stage'] == 'started' and u_j_s['status'] == 'running'):
                        u_j_s['exec_start_time'] = _timestamp_from_utc(u_j_s['time_info'][1])
                    elif (u_j_s['stage'] == 'completed' or u_j_s['stage'] == 'complete'
                            or u_j_s['job_state'] == 'completed' or u_j_s['status'] == 'done'):
                        u_j_s['finish_time'] = _timestamp_from_utc(u_j_s['time_info'][1])
                    #get some info from the client groups
                    for clnt in c_groups:
                        if clnt['function_name'] in u_j_s['job_desc']:
                            u_j_s['app_id'] = clnt['app_id']
                            u_j_s['client_groups'] = clnt['client_groups']
                            u_j_s['module'] = clnt['module_name']
                            u_j_s['method'] = clnt['function_name']
                            break
                    #log("*******From ujs result directly*******:\n")
                    #log(pformat(u_j_s))

                if ('exec_start_time' in u_j_s and u_j_s['stage'] == 'started'
                        and u_j_s['status'] == 'running'):
                    delta = (datetime.datetime.utcnow() -
                            datetime.datetime.fromtimestamp(u_j_s['exec_start_time']/1000))
                    delta = delta - datetime.timedelta(microseconds=delta.microseconds)
                    u_j_s['running_time'] = str(delta) #delta.total_seconds()
                elif ('finish_time' in u_j_s and 'exec_start_time' in u_j_s
                        and u_j_s['status'] == 'done'):
                    delta = (datetime.datetime.fromtimestamp(u_j_s['finish_time']/1000) -
                            datetime.datetime.fromtimestamp(u_j_s['exec_start_time']/1000))
                    delta = delta - datetime.timedelta(microseconds=delta.microseconds)
                    u_j_s['run_time'] = str(delta) #delta.total_seconds()
                elif (u_j_s['stage'] == 'created' and 'creation_time' in u_j_s
                        and u_j_s['status'] not in ['done','running','canceled by user','error']
                        and job_error[j_idx] == {}):
                    delta = (datetime.datetime.utcnow() - datetime.datetime.fromtimestamp(
                                    u_j_s['creation_time']/1000))
                    delta = delta - datetime.timedelta(microseconds=delta.microseconds)
                    u_j_s['queued_time'] = str(delta) #delta.total_seconds()
                    u_j_s['status'] = 'queued'
                else:
                    u_j_s['status'] = 'not created'

                ujs_ret.append(u_j_s)

        #log("Job count={}".format(len(ujs_ret)))
        return ujs_ret

    def get_exec_stats_from_cat(self):
        """
        get_exec_stats_from_cat: Get stats on completed jobs
        return an array of the following structure (example with data):
        {
             u'app_id': u'describe_rnaseq_experiment',
             u'app_module_name': u'KBaseRNASeq',
             u'creation_time': 1456863947.568,
             u'exec_start_time': 1456863953.739,
             u'finish_time': 1456863955.138,
             u'func_module_name': u'KBaseRNASeq',
             u'func_name': u'SetupRNASeqAnalysis',
             u'git_commit_hash': u'5de844e7303a8a30a94d4ca40f2b341439b8bb3c',
             u'is_error': True,
             u'user_id': u'srividya22'
        }
        """
        try: #log("Fetching the exec stats data from Catalog API...")
            raw_stats = self.cat_client.get_exec_raw_stats({})
        except Exception as e_raw: #RuntimeError:
            log('kb_Metrics.get_exec_stats_from_cat raised error:')
            log(pformat(e_raw))
            return []
	else:
	    # Calculate queued_time and run_time (in seconds)
	    for elem in raw_stats:
		tc = elem['creation_time']
		ts = elem['exec_start_time']
		tf = elem['finish_time']
		elem['queued_time'] = ts - tc
		elem['run_time'] = tf - ts

            log(pformat(raw_stats[0]))
	    return raw_stats


    def get_client_groups_from_cat(self):
        """
        get_client_groups_from_cat: Get the client_groups data from Catalog API
        return an array of the following structure (example with data):
        {
            u'app_id': u'assemblyrast/run_arast',
            u'client_groups': [u'bigmemlong'],
            u'function_name': u'run_arast',
            u'module_name': u'AssemblyRAST'},
        }
        """
        # Pull the data
        client_groups = self.cat_client.get_client_groups({})

        #log("\nClient group example:\n{}".format(pformat(client_groups[0])))

        return client_groups


    def get_exec_aggrTable_from_cat(self):
        """
        get_exec_stats_from_cat: Get stats on completed jobs
        return an array of the following structure (example with data):
        {
             u'app': u'kb_uploadmethods/import_sra_as_reads_from_web',
             u'func': u'import_sra_from_web',
             u'func_mod': u'kb_uploadmethods',
             u'n': 5,
             u'user': u'umaganapathyswork'
        }
        """
        try:#log("Fetching the exec_aggr table data from Catalog API...")
            aggr_tab = self.cat_client.get_exec_aggr_table({})
        except Exception as e_aggr: #RuntimeError:
            log('kb_Metrics.get_exec_aggrTable_from_cat raised error:')
            log(pformat(e_aggr))
            return []
	else:
	    log(pformat(aggr_tab[0]))
	    return aggr_tab


    def get_exec_aggrStats_from_cat(self):
        """
        get_exec_aggr_from_cat: Get stats on aggregated execution results of KBase apps
        return an array of the following structure (example with data):
        {
             u'full_app_id': u'KBaseRNASeq/describe_rnaseq_experiment',
             u'module_name': u'KBaseRNASeq',
             u'number_of_calls': 689,
             u'number_of_errors': 117,
             u'time_range': u'*',
             u'total_exec_time': 10.807103612158034,
             u'total_queue_time': 127.90380222181479,
             u'type': u'a'
        }
        """
        # Pull the data
        try:#log("Fetching the exec_aggr stats data from Catalog API...")
            aggr_stats = self.cat_client.get_exec_aggr_stats({})
        except Exception as e_aggr: #RuntimeError:
            log('kb_Metrics.get_exec_aggrStats_from_cat raised error:')
            log(pformat(e_aggr))
            return []
	else:
	    # Convert time from seconds to hours
	    for kb_mod in aggr_stats:
		te = kb_mod['total_exec_time']
		tq = kb_mod['total_queue_time']
		kb_mod['total_exec_time'] = te/3600
		kb_mod['total_queue_time'] = tq/3600
	    log(pformat(aggr_stats[0]))
	    return aggr_stats


    def get_module_stats_from_cat(self):
        """
        get_module_stats_from_cat: Get stats on Modules
        """
        # Pull the data
        log("Fetching the module stats data from Catalog API...")
        now = time.time()
        kb_modules = dict()
        for kb_module in self.cat_client.list_basic_module_info({'include_unreleased':True}):
            name = kb_module['module_name']
            v = self.cat_client.get_module_info({'module_name':name})['beta']
            vers = self.cat_client.list_released_module_versions({'module_name':name})
            s = 'b'
            if len(vers)>0:
                v = vers[0]
                s = 'r'
            if v is None:
                continue
            ct = len(v['narrative_methods'])
            days = (v['timestamp']/1000)/3600/24
            #print '%-40s %3d %3d' %(kb_module['module_name'],days,ct)
            kb_modules['%s:%d:%s' %(name,ct,s)] = days
        #log(pformat(kb_modules))

        # Generate time based summaries
        sorted_x = sorted(kb_modules, key=lambda i: int(kb_modules[i]))
        mods = dict()
        apps = dict()
        rmods = dict()
        rapps = dict()
        for bucket in range(184,300):
            mods[bucket] = 0
            apps[bucket] = 0
            rmods[bucket] = 0
            rapps[bucket] = 0
        for m in sorted_x:
            (name,ct,s) = m.split(':')
            d = kb_modules[m]
            bucket = int(d/91.25)
            if bucket not in mods:
                mods[bucket] = 0
                apps[bucket] = 0
                rmods[bucket] = 0
                rapps[bucket] = 0
            mods[bucket] += 1
            apps[bucket] += int(ct)
            if s == 'r':
                rmods[bucket] += 1
                rapps[bucket] += int(ct)
            #print '%-40s %3d %3d' %(name,int(ct),kb_modules[m])

        # Modules by Quarter
        tmods = 0
        tapps = 0
        trmods = 0
        trapps = 0
        Q = 1
        Y =16
        labels = dict()
        bucket = 184
        for year in range(16,21):
            for quarter in range(1,5):
                labels[bucket] = 'Q%d-%2d' % (quarter,year)
                bucket += 1
        for b in range(184,191):
            tmods += mods[b]
            tapps += apps[b]
            trmods += rmods[b]
            trapps += rapps[b]
            print '%5s %3d %3d       %3d %3d   %3d %3d' %(labels[b],tmods, tapps,trmods,trapps,tmods-trmods,tapps-trapps)

        return kb_modules


    def group_by_user(self, job_sts, user_ids):
        grouped_ujs = []
        if user_ids == []:
            return {'user_id': 'all_users', 'job_states': job_sts}

        for uid in user_ids:
            ujs_by_user = []
            for ujs_i in job_sts:
                if uid == ujs_i['user_id']:
                    ujs_by_user.append(ujs_i)
            if len(ujs_by_user) > 0:
                grouped_ujs.append({'user_id': uid, 'job_states': ujs_by_user})

        return grouped_ujs


    def filterUJS_by_time_stage(self, job_sts, j_stage, j_start_time, j_end_time):
        filtered_ujs = []
        for ujs_i in job_sts:
            if isinstance(ujs_i['creation_time'], int):
                cr_time = datetime.datetime.utcfromtimestamp(ujs_i['creation_time'] / 1000)
            else:
                cr_time = _datetime_from_utc(ujs_i['creation_time'])
            #log("Comparing {} between {} and {}".format(str(cr_time), str(j_start_time), str(j_end_time)))
            if (cr_time <= j_end_time and cr_time >= j_start_time):
                if (j_stage == 'all' or j_stage == ujs_i['stage']):
                    filtered_ujs.append(ujs_i)

        return filtered_ujs


    def convert_time_info(self, ujs_arr):
        #convert time_info from [utc_string, utc_string, utc_string] to [epoch_timestamp*3]
        for u_j_s in ujs_arr:
            if u_j_s['time_info']:
                #log("Before {}".format(pformat(u_j_s['time_info'])))
                u_j_s['time_info'] = [_timestamp_from_utc(t_j) if t_j else None for t_j in u_j_s['time_info']]
                #log("After {}".format(pformat(u_j_s['time_info'])))
        return ujs_arr

    def init_clients_withToken(self, token):
        token = token if token else os.environ['KB_AUTH_TOKEN']
        self.ws_client = Workspace(self.workspace_url, token=token)
        self.cat_client = Catalog(self.catalog_url, auth_svc=self.auth_service_url, token=token)
        self.njs_client = NarrativeJobService(self.njsw_url, auth_svc=self.auth_service_url, token=token)
        self.ujs_client = UserAndJobState(self.job_service_url, auth_svc=self.auth_service_url, token=token)
        self.uprf_client = UserProfile(self.user_profile_url, auth_svc=self.auth_service_url, token=token)

    def process_app_parameters(self, params):
        if params.get('user_ids', None) is None:
            params['user_ids'] = []
        else:
            if not isinstance(params['user_ids'], list):
                raise ValueError('Variable user_ids' + ' must be a list.')

        if not params.get('time_range', None) is None:
            time_start, time_end = params['time_range']
            params['time_start'] = _convert_to_datetime(time_start)
            params['time_end'] = _convert_to_datetime(time_end)
        else: #set the most recent 48 hours range
            params['time_end'] = datetime.datetime.utcnow()
            params['time_start'] = params['time_end'] - datetime.timedelta(hours=48)

        if params.get('job_stage', None) is None:
            params['job_stage'] = 'all'
        if params['job_stage'] == 'completed':
            params['job_stage'] = 'complete'

        return params


    def process_user_parameters(self, params):
        if params.get('filter_str', None) is None:
            params['filter_str'] = ''
        else:
            if not isinstance(params['filter_str'], str):
                raise ValueError('Variable filter_str' + ' must be a string.')

        if not params.get('time_range', None) is None:
            time_start, time_end = params['time_range']
            params['time_start'] = _convert_to_datetime(time_start)
            params['time_end'] = _convert_to_datetime(time_end)
        else: #set the most recent quarter (90 days)
            params['time_end'] = datetime.datetime.utcnow()
            params['time_start'] = params['time_end'] - datetime.timedelta(days=90)

        return params


    def generate_user_metrics(self, input_params):#, token):
        """
        generate_user_metrics: get user data with structure as the following example:
        [
         {'creation_time': '2017-09-04 15:46:56.387000',
          'user_data': {u'department': u'Biotechnology and food science',
                        u'organization': u'NTNU'},
          'user_name': {u'realname': u'Vetle Simensen', u'username': u'vetle'}},
         {'creation_time': '2017-09-06 21:45:43.251000',
          'user_data': {u'department': u'Department of Medicine',
                        u'organization': u'University of Chicago'},
          'user_name': {u'realname': u'\xd6zcan Esen', u'username': u'ozcan'}},
         {'creation_time': '2017-08-30 21:47:51.711000',
          'user_data': {u'department': u'Plant and Microbial Biology',
                        u'organization': u'University of California-Berkeley'},
          'user_name': {u'realname': u'Daniel Westcott', u'username': u'westcott'}},
         ......
        ]
        """
        params = self.process_user_parameters(input_params)
        user_filter = params['filter_str']
        time_start = params['time_start']
        time_end = params['time_end']

        kb_users = self.get_user_names(user_filter)

        user_names = []
        real_names = []
        for u in kb_users:
            user_names.append(u['username'])
            real_names.append(u['realname'])

        kb_uprof = self.get_user_profiles(user_names)
        total_user_count = len(kb_uprof)
        log("Before time range filter:{}".format(total_user_count))

        if (time_start is not None or time_end is not None):
            kb_uprof = self.filterUPROF_by_time_stage(kb_uprof, time_start, time_end)
        period_user_count = len(kb_uprof)
        log("After time range filter:{}".format(period_user_count))

        return {'user_metrics': kb_uprof}


    def get_user_names(self, filter_str):
        """
        get_user_names: given a filter string, get a list of User of structure as below:
        typedef structure {
                username username;
                realname realname;
                string thumbnail;
        } User;
        """
        log("Fetching user name details for {} users\n{}".format(
                'the' if filter_str else 'all', 'with id containing ' + filter_str if filter_str else ''))
        user_names = self.uprf_client.filter_users({'filter': filter_str})
        #log(pformat(user_names))
        return user_names


    def get_user_profiles(self, user_ids):
        """
        get_user_profiles: given the user ids, get a list of UserProfile of structure as below:
        typedef structure {
                username username;
                realname realname;
                string thumbnail;
        } User;
        typedef structure {
                User user;
                UnspecifiedObject profile;
        } UserProfile;
        example returned data:
        [
                {u'profile': {u'metadata': {u'created': u'2017-11-28T02:52:28.492Z',
                                            u'createdBy': u'userprofile_ui_service'},
                              u'preferences': {},
                              u'synced': {u'gravatarHash': u'81793127ae5301c545a054846941c061'},
                              u'userdata': {u'department': u'Physics',
                                            u'organization': u'University of Illinois at Urbana-Champaign'}
                             },
                 u'user': {u'realname': u'Karna Gowda', u'username': u'karnagowda'}
                },
                {u'profile': {u'metadata': {u'created': u'2017-11-28T04:06:14.371Z',
                                            u'createdBy': u'userprofile_ui_service'},
                              u'preferences': {},
                              u'synced': {u'gravatarHash': u'370bb047fc197fd60921eaf5d1683acf'},
                              u'userdata': {u'department': u'Spirit Youth',
                                            u'organization': u'WJS Canada'}
                             },
                 u'user': {u'realname': u'Nicole McMillan', u'username': u'n_mcmillan'}
                },
                .......
        ]
        """
        log("Fetching profile info for {} users:\n".format(len(user_ids) if user_ids else 'all'))
        user_prof = self.uprf_client.get_user_profile(user_ids)
        log(pformat(user_prof))
        return user_prof


    def filterUPROF_by_time_stage(self, user_prof, j_start_time, j_end_time):
        """
        example input data for user_prof:
        [
                {u'profile': {u'metadata': {u'created': u'2017-11-28T02:52:28.492Z',
                                            u'createdBy': u'userprofile_ui_service'},
                              u'preferences': {},
                              u'synced': {u'gravatarHash': u'81793127ae5301c545a054846941c061'},
                              u'userdata': {u'department': u'Physics',
                                            u'organization': u'University of Illinois at Urbana-Champaign'}
                             },
                 u'user': {u'realname': u'Karna Gowda', u'username': u'karnagowda'}
                },
                {u'profile': {u'metadata': {u'created': u'2017-11-28T04:06:14.371Z',
                                            u'createdBy': u'userprofile_ui_service'},
                              u'preferences': {},
                              u'synced': {u'gravatarHash': u'370bb047fc197fd60921eaf5d1683acf'},
                              u'userdata': {u'department': u'Spirit Youth',
                                            u'organization': u'WJS Canada'}
                             },
                 u'user': {u'realname': u'Nicole McMillan', u'username': u'n_mcmillan'}
                },
                .......
        ]
        """
        filtered_uprof = []
        for u_i in user_prof:
            u_crt = u_i['profile']['metadata']['created']
            if isinstance(u_crt, int):
                cr_time = datetime.datetime.utcfromtimestamp(u_crt / 1000)
            else:
                cr_time = _datetime_from_utc(u_crt)
            #log("Comparing {} between {} and {}".format(str(cr_time), str(j_start_time), str(j_end_time)))
            if (cr_time <= j_end_time and cr_time >= j_start_time):
                filtered_uprof.append({'user_name': u_i['user'],
                                       'creation_time': str(cr_time),
                                       'user_data': u_i['profile']['userdata']
                                })

        return filtered_uprof

    def process_met_parameters(self, params):
        if params.get('user_ids', None) is None:
            params['user_ids'] = []
        else:
            if not isinstance(params['user_ids'], list):
                raise ValueError('Variable user_ids' + ' must be a list.')
	if 'kbasetest' in params['user_ids']:
		params['user_ids'].remove('kbasetest')

        if (not params.get('start_time', None) is None and
		not params.get('end_time', None) is None):
	    params['start_time'] = _convert_to_datetime(params['start_time'])
	    params['end_time'] = _convert_to_datetime(params['end_time'])
            params['minTime'] = _unix_time_millis_from_datetime(params['start_time'])
            params['maxTime'] = _unix_time_millis_from_datetime(params['end_time'])
        elif (not params.get('start_time', None) is None and
		params.get('end_time', None) is None):
	    params['start_time'] = _convert_to_datetime(params['start_time'])
            params['end_time'] = params['start_time'] + datetime.timedelta(hours=48)
            params['minTime'] = _unix_time_millis_from_datetime(params['start_time'])
            params['maxTime'] = _unix_time_millis_from_datetime(params['end_time'])
        elif (params.get('start_time', None) is None and
		not params.get('end_time', None) is None):
	    params['end_time'] = _convert_to_datetime(params['end_time'])
            params['start_time'] = params['end_time'] - datetime.timedelta(hours=48)
            params['minTime'] = _unix_time_millis_from_datetime(params['start_time'])
            params['maxTime'] = _unix_time_millis_from_datetime(params['end_time'])
        else: #set the most recent 48 hours range
            maxTime = datetime.datetime.utcnow()
            minTime = maxTime - datetime.timedelta(hours=48)
            params['minTime'] = _unix_time_millis_from_datetime(minTime)
            params['maxTime'] = _unix_time_millis_from_datetime(maxTime)
        return params


