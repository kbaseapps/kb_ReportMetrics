# -*- coding: utf-8 -*-
#BEGIN_HEADER
# The header block is where all import statments should live
import os
from Bio import SeqIO
from pprint import pprint, pformat
from AssemblyUtil.AssemblyUtilClient import AssemblyUtil
from KBaseReport.KBaseReportClient import KBaseReport

from kb_ReportMetrics.core.genome_feature_stats import genome_feature_stats
from kb_ReportMetrics.core.report_utils import report_utils
from kb_ReportMetrics.core.UJS_CAT_NJS_DataUtils import UJS_CAT_NJS_DataUtils
#END_HEADER


class kb_ReportMetrics:
    '''
    Module Name:
    kb_ReportMetrics

    Module Description:
    A KBase module: kb_ReportMetrics
This KBase SDK module implements methods for generating reports on various KBase metrics.
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = "https://github.com/kbaseapps/kb_ReportMetrics.git"
    GIT_COMMIT_HASH = "9de955bc4d567b6eb5856833e7a22de7a0ac979e"

    #BEGIN_CLASS_HEADER
    # Class variables and functions can be defined in this block
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR

        # Any configuration parameters that are important should be parsed and
        # saved in the constructor.
        #self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.ws_url = config['workspace-url']
        self.shared_folder = config['scratch']
        self.config = config
        #END_CONSTRUCTOR
        pass


    def count_ncbi_genomes(self, ctx, params):
        """
        The actual function is declared using 'funcdef' to specify the name
        and input/return arguments to the function.  For all typical KBase
        Apps that run in the Narrative, your function should have the 
        'authentication required' modifier.
        :param params: instance of type "GenomeCountParams" (A 'typedef' can
           also be used to define compound or container objects, like lists,
           maps, and structures.  The standard KBase convention is to use
           structures, as shown here, to define the input and output of your
           function.  Here the input is a reference to the Assembly data
           object, a workspace to save output, and a length threshold for
           filtering. To define lists and maps, use a syntax similar to C++
           templates to indicate the type contained in the list or map.  For
           example: list <string> list_of_strings; mapping <string, int>
           map_of_ints;) -> structure: parameter "genome_source" of String,
           parameter "genome_domain" of String, parameter "refseq_category"
           of String, parameter "workspace_name" of String, parameter
           "create_report" of type "bool" (A boolean - 0 for false, 1 for
           true. @range (0, 1))
        :returns: instance of type "StatResults" (Here is the definition of
           the output of the function.  The output can be used by other SDK
           modules which call your code, or the output visualizations in the
           Narrative.  'report_name' and 'report_ref' are special output
           fields- if defined, the Narrative can automatically render your
           Report.) -> structure: parameter "report_name" of String,
           parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: return_records
        #BEGIN count_ncbi_genomes
        gfs = genome_feature_stats(self.config, ctx.provenance)
        return_records = gfs.count_refseq_genomes(params)
        #END count_ncbi_genomes

        # At some point might do deeper type checking...
        if not isinstance(return_records, dict):
            raise ValueError('Method count_ncbi_genomes return value ' +
                             'return_records is not type dict as required.')
        # return the results
        return [return_records]

    def count_ncbi_genome_features(self, ctx, params):
        """
        :param params: instance of type "FeatureCountParams" -> structure:
           parameter "genbank_file_urls" of list of String, parameter
           "file_format" of String, parameter "genome_source" of String,
           parameter "genome_domain" of String, parameter "refseq_category"
           of String, parameter "workspace_name" of String, parameter
           "create_report" of type "bool" (A boolean - 0 for false, 1 for
           true. @range (0, 1))
        :returns: instance of type "StatResults" (Here is the definition of
           the output of the function.  The output can be used by other SDK
           modules which call your code, or the output visualizations in the
           Narrative.  'report_name' and 'report_ref' are special output
           fields- if defined, the Narrative can automatically render your
           Report.) -> structure: parameter "report_name" of String,
           parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: return_records
        #BEGIN count_ncbi_genome_features
        gfs = genome_feature_stats(self.config, ctx.provenance)
        return_records = gfs.count_ncbi_genome_features(params)
        #END count_ncbi_genome_features

        # At some point might do deeper type checking...
        if not isinstance(return_records, dict):
            raise ValueError('Method count_ncbi_genome_features return value ' +
                             'return_records is not type dict as required.')
        # return the results
        return [return_records]

    def count_genome_features(self, ctx, params):
        """
        :param params: instance of type "FeatureCountParams" -> structure:
           parameter "genbank_file_urls" of list of String, parameter
           "file_format" of String, parameter "genome_source" of String,
           parameter "genome_domain" of String, parameter "refseq_category"
           of String, parameter "workspace_name" of String, parameter
           "create_report" of type "bool" (A boolean - 0 for false, 1 for
           true. @range (0, 1))
        :returns: instance of type "StatResults" (Here is the definition of
           the output of the function.  The output can be used by other SDK
           modules which call your code, or the output visualizations in the
           Narrative.  'report_name' and 'report_ref' are special output
           fields- if defined, the Narrative can automatically render your
           Report.) -> structure: parameter "report_name" of String,
           parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: return_records
        #BEGIN count_genome_features
        gfs = genome_feature_stats(self.config, ctx.provenance)
        return_records = gfs.count_genome_features(params)
        #END count_genome_features

        # At some point might do deeper type checking...
        if not isinstance(return_records, dict):
            raise ValueError('Method count_genome_features return value ' +
                             'return_records is not type dict as required.')
        # return the results
        return [return_records]

    def report_exec_stats(self, ctx, params):
        """
        :param params: instance of type "StatsReportParams" -> structure:
           parameter "stats_name" of String, parameter "workspace_name" of
           String, parameter "create_report" of type "bool" (A boolean - 0
           for false, 1 for true. @range (0, 1))
        :returns: instance of type "StatResults" (Here is the definition of
           the output of the function.  The output can be used by other SDK
           modules which call your code, or the output visualizations in the
           Narrative.  'report_name' and 'report_ref' are special output
           fields- if defined, the Narrative can automatically render your
           Report.) -> structure: parameter "report_name" of String,
           parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: return_records
        #BEGIN report_exec_stats
        rps = report_utils(self.config, ctx.provenance)
        return_records = rps.create_exec_stats_reports(params)
        #END report_exec_stats

        # At some point might do deeper type checking...
        if not isinstance(return_records, dict):
            raise ValueError('Method report_exec_stats return value ' +
                             'return_records is not type dict as required.')
        # return the results
        return [return_records]

    def dummy_test0(self, ctx, params):
        """
        :param params: instance of type "StatsReportParams" -> structure:
           parameter "stats_name" of String, parameter "workspace_name" of
           String, parameter "create_report" of type "bool" (A boolean - 0
           for false, 1 for true. @range (0, 1))
        :returns: instance of type "StatResults" (Here is the definition of
           the output of the function.  The output can be used by other SDK
           modules which call your code, or the output visualizations in the
           Narrative.  'report_name' and 'report_ref' are special output
           fields- if defined, the Narrative can automatically render your
           Report.) -> structure: parameter "report_name" of String,
           parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: return_records
        #BEGIN dummy_test0
        rps = report_utils(self.config, ctx.provenance)
        #return_records = rps.get_module_stats_from_cat()
        return_records = rps.create_stats_report(params)
        #END dummy_test0

        # At some point might do deeper type checking...
        if not isinstance(return_records, dict):
            raise ValueError('Method dummy_test0 return value ' +
                             'return_records is not type dict as required.')
        # return the results
        return [return_records]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
