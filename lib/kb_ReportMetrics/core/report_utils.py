import time
import datetime
import csv, json
import os
import re
import copy
import uuid
import subprocess
import shutil
import sys
import zipfile
import gzip
from pprint import pprint, pformat
from urllib2 import Request, urlopen
from urllib2 import URLError, HTTPError
import urllib
import errno

from Bio import Entrez, SeqIO
from numpy import median, mean, max

from KBaseReport.KBaseReportClient import KBaseReport
from kb_ReportMetrics.core.UJS_CAT_NJS_DataUtils import UJS_CAT_NJS_DataUtils

def log(message, prefix_newline=False):
    """Logging function, provides a hook to suppress or redirect log messages."""
    print(('\n' if prefix_newline else '') + '{0:.2f}'.format(time.time())
		+ ': ' + message.encode('utf-8'))


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


class report_utils:
    PARAM_IN_WS = 'workspace_name'

    def __init__(self, scratch_dir, workspace_url, callback_url, srv_wiz_url,
				job_service_url, njsw_url, auth_service_url,
				kbase_endpoint, provenance, token):
        self.scratch = scratch_dir
        self.callback_url = callback_url

        self.workspace_url = workspace_url
        self.job_service_url = job_service_url
        self.njsw_url = njsw_url
        self.auth_service_url = auth_service_url
	self.srv_wiz_url = srv_wiz_url
	self.kbase_endpoint = kbase_endpoint
        self.provenance = provenance
	self.token = token

        _mkdir_p(self.scratch)
        self.metrics_dir = os.path.join(self.scratch, str(uuid.uuid4()))
        _mkdir_p(self.metrics_dir)

	self.statdu = UJS_CAT_NJS_DataUtils(self.workspace_url,
				self.job_service_url, self.srv_wiz_url,
				self.njsw_url, self.auth_service_url,
				self.kbase_endpoint, self.provenance, self.token)
        self.kbr = KBaseReport(self.callback_url)
	self.metrics_apps = ['user_details', 'user_counts_per_day', 'user_ws_stats',
				'user_narrative_stats', 'user_numObjs', 'total_logins']

    def create_metrics_reports(self, params):
        """
        """
        if params.get(self.PARAM_IN_WS, None) is None:
           raise ValueError(self.PARAM_IN_WS + ' parameter is mandatory')

        if params.get('stats_name', None) is None:
            raise ValueError('Variable stats_name' + ' parameter is mandatory')

        stats_name = params['stats_name']

        ret_stats = []
        if stats_name == 'exec_stats':
            ret_stats = self.statdu.get_exec_stats_from_cat()
        elif stats_name == 'exec_aggr_stats':
            ret_stats = self.statdu.get_exec_aggrStats_from_cat()
        elif stats_name == 'exec_aggr_table':
            ret_stats = self.statdu.get_exec_aggrTable_from_cat()
        elif stats_name == 'app_stats':
            ret_stats = self.statdu.get_app_metrics(params)
        elif stats_name in self.metrics_apps:
            ret_stats = self.statdu.get_user_metrics(params)
	    if len(ret_stats['metrics_result']) > 0:
		#print('Number of records returned={}'.format(len(ret_stats['metrics_result'])))
		self._write_stats_json_tsv_files(ret_stats['metrics_result'], stats_name)
        else:
	    ret_metrics['metrics_result'] = []

        returnVal = {
            "report_ref": None,
            "report_name": None
        }

        if len(ret_stats['metrics_result']) == 0:
            return returnVal

        col_caps = ['module_name', 'full_app_id', 'number_of_calls', 'number_of_errors',
                        'type', 'time_range', 'total_exec_time', 'total_queue_time']
        if params['create_report'] == 1:
	    if stats_name == 'app_stats':
		report_info = self.generate_app_report(self.metrics_dir, ret_stats, params)
            elif stats_name in self.metrics_apps:
		if stats_name == 'user_details':
		    col_caps = ['username', 'email', 'full_name', 'signup_at', 'last_signin_at', 'roles', 'kbase_staff']
		else:
		    col_caps = None
		report_info = self.generate_user_report(self.metrics_dir,
				ret_stats['metrics_result'], params, col_caps)
	    elif stats_name in ['exec_stats', 'exec_aggr_stats', 'exec_aggr_table']:
		report_info = self.generate_exec_report(self.metrics_dir, ret_stats, params)
	    else:
		report_info['name'] = None
		report_info['ref'] = None

            returnVal = {
                'report_name': report_info['name'],
                'report_ref': report_info['ref']
            }

        return returnVal

    def _write_stats_json_tsv_files(self, stats_data, stats_name):
	json_full_path = os.path.join(self.metrics_dir, '{}_metrics.json'.format(stats_name))
	tsv_full_path = os.path.join(self.metrics_dir, '{}_metrics.tsv'.format(stats_name))

	with open(json_full_path, 'w') as metrics_json:
	    json.dump(stats_data, metrics_json)
 
	enc_data = []
	for sd in stats_data:
	    #produce a new dictionary, which replaces the values with the encoded values
	    enc_data.append(dict((k, v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in sd.iteritems()))
	with open(tsv_full_path, 'wb') as metrics_tsv:
	    dw = csv.DictWriter(metrics_tsv, fieldnames=enc_data[0].keys(), delimiter='\t')
	    dw.writeheader()
	    dw.writerows(enc_data)

    def generate_user_report(self, metrics_dir, data_info, params, col_caps=None):
	output_html_files = self._generate_user_html_report(metrics_dir, data_info, params, col_caps)
        output_files = self._generate_output_file_list(metrics_dir)

        # create report
        report_text = 'Summary of {} metrics for {}:\n\n'.format(params['stats_name'],
			','.join(params['user_ids']) if len(params['user_ids'])>0 else 'all_users')

        report_info = self.kbr.create_extended_report({
                        'message': report_text,
                        'report_object_name': 'kb_ReportMetrics_UserReport_' + str(uuid.uuid4()),
                        'file_links': output_files,
                        'direct_html_link_index': 0,
                        'html_links': output_html_files,
                        'html_window_height': 366,
                        'workspace_name': params[self.PARAM_IN_WS]
                      })

        return report_info

    def _generate_user_html_report(self, out_dir, dt_info, params, col_caps=None):
        """
        _generate_user_html_report: generate html report given the json data

        """
        #log('start generating html report')
	stats_name = params['stats_name']
        rpt_title = 'Metrics report on {}'.format(stats_name)

        html_report = list()
        html_file_path = self._write_user_html(out_dir, dt_info, rpt_title, stats_name, col_caps)

        #log(html_file_path['html_file'])
        html_report.append({'path': html_file_path['html_path'],
                            'name': rpt_title,
                            'label': rpt_title,
                            'description': 'The user metrics report with charts'
                        })

        return html_report

    def _write_user_html(self, out_dir, input_dt, rpt_title, stats_nm, col_caps=None):
        headContent = self._write_headContent()
        if col_caps is None:
            callbackFunc = self._write_callback_function(input_dt)
        else:
            callbackFunc = self._write_callback_function(input_dt, col_caps)

        dashboard = self._write_user_dashboard(stats_nm)

        footContent = self._write_footcontent(rpt_title, stats_nm)

        html_str = headContent + callbackFunc + dashboard + footContent
        #log(html_str)

        html_file_path = os.path.join(out_dir, 'user_report_charts.html')

        with open(html_file_path, 'w') as html_file:
                html_file.write(html_str.encode('utf-8'))

        return {'html_file': html_str, 'html_path': html_file_path}


    def generate_app_report(self, metrics_dir, data_info, params, col_caps=None):
        if col_caps is None:
            pass#output_html_files = self._generate_html_report(metrics_dir, data_info)
        else:
            pass#output_html_files = self._generate_html_report(metrics_dir, data_info, col_caps)

        output_files = self._generate_output_file_list(metrics_dir)

        # create report
        report_text = 'Summary of app metrics for {}:\n\n'.format(
			','.join(params['user_ids']) if len(params['user_ids'])>0 else 'all_users')

        report_info = self.kbr.create_extended_report({
                        'message': report_text,
                        'report_object_name': 'kb_ReportMetrics_report_' + str(uuid.uuid4()),
                        'file_links': output_files,
                        #'direct_html_link_index': 0,
                        #'html_links': output_html_files,
                        'html_window_height': 366,
                        'workspace_name': params[self.PARAM_IN_WS]
                      })

        return report_info


    def generate_exec_report(self, metrics_dir, data_info, params, col_caps=None):
        if col_caps is None:
            output_html_files = self._generate_html_report(metrics_dir, data_info)
        else:
            output_html_files = self._generate_html_report(metrics_dir, data_info, col_caps)

        output_json_files = self._generate_output_file_list(metrics_dir)

        # create report
        report_text = 'Summary of {} stats:\n\n'.format(params['stats_name'])

        report_info = self.kbr.create_extended_report({
                        'message': report_text,
                        'report_object_name': 'kb_ReportMetrics_report_' + str(uuid.uuid4()),
                        'file_links': output_json_files,
                        'direct_html_link_index': 0,
                        'html_links': output_html_files,
                        'html_window_height': 366,
                        'workspace_name': params[self.PARAM_IN_WS]
                      })

        return report_info


    def _download_file_by_url(self, file_url):
        download_to_dir = os.path.join(self.scratch, str(uuid.uuid4()))
        _mkdir_p(download_to_dir)
        download_file = os.path.join(download_to_dir, 'genome_file.gbff.gz')

        try:
            urllib.urlretrieve(file_url, download_file)
        except HTTPError as e:
            log('The server couldn\'t download {}.'.format(file_url))
            log('Error code: ', e.code)
        except URLError as e:
            log('We failed to reach the server to download {}.'.format(file_url))
            log('Reason: ', e.reason)
        except IOError as e:
            log('Caught IOError when downloading {}.'.format(file_url))
            log('Error number: ', e.errno)
            log('Error code: ', e.strerror)
            if e.errno == errno.ENOSPC:
                log('No space left on device.')
            elif e.errno == 110:#[Errno ftp error] [Errno 110] Connection timed out
                log('Connection timed out, trying to urlopen!')
                try:
                    fh = urllib2.urlopen(file_url)
                    data = fh.read()
                    with open(download_file, "w") as dfh:
                        dfh.write(data)
                except:
                    log('Connection timed out, urlopen try also failed!')
                else:
                    pass
        else:# everything is fine
            pass

        return download_file


    def _get_file_content_by_url(self, file_url):
        req = Request(file_url)
        resp = ''
        try:
            resp = urlopen(req)
        except HTTPError as e:
            log('The server couldn\'t fulfill the request to download {}.'.format(file_url))
            log('Error code: ', e.code)
        except URLError as e:
            log('We failed to reach a server to download {}.'.format(file_url))
            log('Reason: ', e.reason)
        else:# everything is fine
            pass

        return resp


    def _generate_output_file_list(self, out_dir):
        """
        _generate_output_file_list: zip result files and generate file_links for report
        """
        log('start packing result files')

        output_files = list()

        output_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        _mkdir_p(output_directory)
        output_file_path = os.path.join(output_directory, 'output_files.zip')
        self.zip_folder(out_dir, output_file_path)

        output_files.append({'path': output_file_path,
                             'name': os.path.basename(output_file_path),
                             'label': os.path.basename(output_file_path),
                             'description': 'Output files generated by kb_ReportMetrics'})

        return output_files


    def zip_folder(self, folder_path, output_path):
        """Zip the contents of an entire folder (with that folder included in the archive).
        Empty subfolders could be included in the archive as well if the commented portion is used.
        """
        with zipfile.ZipFile(output_path, 'w',
                             zipfile.ZIP_DEFLATED,
                             allowZip64=True) as ziph:
            for root, folders, files in os.walk(folder_path):
                # Include all subfolders, including empty ones.
                #for folder_name in folders:
                #    absolute_path = os.path.join(root, folder_name)
                #    relative_path = os.path.join(os.path.basename(root), folder_name)
                #    print "Adding {} to archive.".format(absolute_path)
                #    ziph.write(absolute_path, relative_path)
                for f in files:
                    absolute_path = os.path.join(root, f)
                    relative_path = os.path.join(os.path.basename(root), f)
                    #print "Adding {} to archive.".format(absolute_path)
                    ziph.write(absolute_path, relative_path)

        print "{} created successfully.".format(output_path)

    def _write_headContent(self):
        """_write_headConten: returns the very first portion of the html file
        """
        head_content = ("\n<html>\n<head>\n"
            "<script type='text/javascript' src='https://www.google.com/jsapi'></script>\n"
            "<script type='text/javascript'>\n"
            "// Load the Visualization API and the controls package.\n"
            "  google.load('visualization', '1', {packages:['controls'], callback: drawDashboard});\n"
            "  google.setOnLoadCallback(drawDashboard);\n")

        return head_content

    def _write_callback_function(self, input_dt, col_caps=None):
        """
        _write_callback_function: write the callback function according to the input_dt and column captions
        """
        callback_func = ("\nfunction drawDashboard() {\n"
            "var data = new google.visualization.DataTable();\n")

        #table column captions
	pprint(input_dt[0])
        if col_caps is None:
            col_caps = input_dt[0].keys()

        cols = []
        for i, col in enumerate(col_caps):
            for k in input_dt[0].keys():
                if col == k:
                    col_type = type(input_dt[0][k]).__name__
                    if (col_type == 'str' 
			or col_type == 'unicode' 
			or col_type == 'list'
			or col_type == 'NoneType'):
                        col_type = 'string'
                    elif col_type == 'bool':
                        col_type = 'boolean'
                    else:
                        col_type = 'number'
                    callback_func += "data.addColumn('" + col_type + "','" + k + "');\n"
                    cols.append( col )

        #data rows
        dt_rows = ""
        for dt in input_dt:
            if dt_rows != "":
                dt_rows += ",\n"
            d_rows = []
            for j, c in enumerate( cols ):
                d_type = type(dt[c]).__name__
                if (d_type == 'str' or d_type == 'unicode'):
                    if dt[c] is None:
                        d_rows.append('"None"')
                    elif dt[c] == '':
			d_rows.append('""')
                    else:
			regex = re.compile(r'(#|")')
			dt[c] = regex.sub('_', dt[c])
                        d_rows.append('"' + dt[c] + '"')
                elif d_type == 'bool':
                    if dt[c]:
                        d_rows.append('true')
                    else:
                        d_rows.append('false')
                elif d_type == 'list':
                    if (dt[c] == [] or dt[c] is None):
			d_rows.append('""')
                    else:
		        dt[c] = '/'.join(dt[c])
                        d_rows.append('"' + dt[c] + '"')
                else:
                    if dt[c] is None:
                        d_rows.append('"None"')
                    elif dt[c] == '':
			d_rows.append('""')
                    else:
                        d_rows.append(str(dt[c]))

            dt_rows += '[' + ','.join(d_rows) + ']'

        callback_func += "\ndata.addRows([\n"
        callback_func += dt_rows
        callback_func += "\n]);"
	#log(callback_func)
        return callback_func

    def _write_category_picker(self, **kwargs):
	col_name = None
	if 'col_name' in kwargs:
	    col_name = kwargs['col_name']
	if col_name is None:
	    return ''

	initSelected = []
	if 'initSel' in kwargs:
	    initSelected = kwargs['initSel']

        cat_picker = ("\nvar categoryPicker = new google.visualization.ControlWrapper({\n"
                "controlType: 'CategoryFilter',\n"
                "containerId: 'cat_picker_div',\n"
                "options: {\n"
                "//filterColumnIndex: 0, // filter by this column\n"
                "filterColumnLabel: '" + col_name + "',\n"
                "ui: {\n"
                "    caption: 'Choose a value',\n"
                "    sortValues: true,\n"
                "    allowNone: true,\n"
                "    allowMultiple: true,\n"
                "    allowTyping: true\n"
                "  }\n"
                "},\n"
                "// Define an initial state, i.e. a set of metrics to be initially selected.\n"
                "state: {'selectedValues': ['" + "','".join(initSelected) + "']}\n"
            "});\n")

	return cat_picker

    def _write_string_filter(self, filterColumns, filter_name, filter_field=None):
	if filter_field is None:
	    return ''
	str_filter = ("\nvar " + filter_name + " = new google.visualization.ControlWrapper({\n"
            "    controlType: 'StringFilter',\n"
            "    containerId: 'string_filter_div',\n"
            "    options: {\n"
            "        //filterColumnLabel: '" + filter_field + "',\n"
            "        filterColumnIndex: 0,\n"
            "        matchType: 'any',\n"
            "        caseSensitive: false,\n"
            "        ui: {\n"
            "            label: 'Search data:'\n"
            "           }\n"
            "    },\n"
            "    view: {\n"
            "               columns: " + filterColumns + "\n"
            "          }\n"
            "});\n")

	return str_filter


    def _write_table_chart(self, tab_div):
        tab_chart = ("\n//create a list of columns for the table chart\n"
            "var filterColumns = [{\n"
            "// this column aggregates all of the data into one column for use with the string filter\n"
            "type: 'string',\n"
            "calc: function (dt, row) {\n"
            "for (var i = 0, vals = [], cols = dt.getNumberOfColumns(); i < cols; i++) {\n"
            "    vals.push(dt.getFormattedValue(row, i));\n"
            "}\n"
            "return vals.join('\\n');\n"
            "}\n"
            "}];\n"
            "var tab_columns = [];\n"
            "for (var j = 0, dcols = data.getNumberOfColumns(); j < dcols; j++) {\n"
            "    filterColumns.push(j);\n"
            "    tab_columns.push(j);\n"
            "}\n"
            "var table = new google.visualization.ChartWrapper({\n"
            "    chartType: 'Table',\n"
            "    containerId: '" + tab_div + "',\n"
            "    options: {\n"
            "        showRowNumber: true,\n"
            "        page: 'enable',\n"
            "        pageSize: 20\n"
            "    },\n"
            "    view: {\n"
            "               columns: tab_columns\n"
            "          }\n"
            "});\n")

	return tab_chart

    def _write_pie_chart(self, pc_nm, pc_div, w, h, ttl, cols):
        pie_chart = ("\n//Create a pie chart, passing some options\n"
                "var " + pc_nm + " = new google.visualization.ChartWrapper({\n"
                "'chartType': 'PieChart',\n"
                "'containerId': '" + pc_div + "',\n"
                "'options': {\n"
                "'width': " + str(w) + ",\n"
                "'height': " + str(h), ",\n"
                "'pieSliceText': 'value', //'label',\n"
                "'legend': 'none',\n"
                "'is3D': true,\n"
                "'chartArea': {'left': 15, 'top': 25, 'right': 0, 'bottom': 15},\n"
                "'title': '" + ttl + "'\n"
                "},\n"
                "'view': {'columns': [" + ",".join(str(x) for x in cols) + "]}\n"
                "});\n")

	return pie_chart

    def _write_line_chart(self, lc_nm, lc_div, w, h, ttl, cols):
        line_chart = ("\n//Create a line chart, passing some options\n"
		"var " + lc_nm + " = new google.visualization.ChartWrapper({\n"
                "'chartType' : 'Line',\n"
                "'containerId' : '" + lc_div + "',\n"
                "'options': {\n"
                "'width': " + str(w) + ",\n"
                "'height': " + str(h) + ",\n"
                "'hAxis': {\n"
                "'title': '" + ttl + "'\n"
                "},\n"
                "'vAxis': {\n"
                "'title': 'Seconds'\n"
                "},\n"
                "'chartArea': {'left': 15, 'top': 25, 'right': 0, 'bottom': 15}\n"
                "},\n"
                "'view': {'columns': [" + ",".join(str(x) for x in cols) + "]}\n"
                "});\n")

	return line_chart

    def _write_NumRangeFilter(self, filter_nm, containerId, col_label, minVal, maxVal, lowVal, highVal):
        num_slider = ("\n//Create a range slider, passing some options\n"
                "var " + filter_nm + " = new google.visualization.ControlWrapper({\n"
                "'controlType': 'NumberRangeFilter',\n"
                "'containerId': '" + containerId + "',\n"
                "'options': {\n"
                "'filterColumnLabel': '" + col_label + "',\n"
                "'minValue': " + str(minVal) + ",\n"
                "'maxValue': " + str(maxVal) + "\n"
                "},\n"
                "'state': {'lowValue': " + str(lowVal) + ", 'highValue': " + str(highVal) + "}\n"
                "});\n")
	return num_slider


    def _write_charts(self):
        cat_picker = self._write_category_picker(col_name='user')

        time_slider = self._write_NumRangeFilter('timeRangeSlider', 'number_filter_div',
						'run_time', 1, 3600, 5, 600)

        num_slider2 = self._write_NumRangeFilter('queueTimeRangeSlider', 'number_filter_div2',
				'queued_time', 1, 20000, 1000, 10000)

        line_chart = self._write_line_chart('lineChart', 'line_div', 600, 300, 'app_id', [6, 9, 10])
        pie_chart = self._write_pie_chart('pieChart', 'pie_div', 300, 300, 'set_your_own_title', [3,4])
	str_filter = self._write_string_filter('filterColumns', 'stringFilter', 'username')
        tab_chart = str_filter + self._write_table_chart('table_div')

        return cat_picker + tab_chart + time_slider + line_chart + num_slider2 + pie_chart


    def _write_user_dashboard(self, stats_nm):
        """
        _write_user_dashboard: writes the dashboard layout and bind controls with charts
        """
        #the dashboard components (table, charts and filters)
	dashboard = ''
	dash_componets = ''
	if (stats_nm == 'user_details' or stats_nm == 'user_ws_stats'):
	    field_nm = 'username'
	    strfilter_nm = field_nm + 'Filter'
            dash_components = (self._write_category_picker(initSel=['qzhang', 'srividya22'],
								col_name=field_nm)
				+ self._write_table_chart('table_div')
				+ self._write_string_filter('filterColumns', strfilter_nm, field_nm))
	    dashboard = ("\n"
		    "var dashboard = new google.visualization.Dashboard(document.querySelector('#dashboard_div'));\n"
		    "dashboard.bind([categoryPicker], [table]);\n"
		    "dashboard.bind([" + strfilter_nm + "], [table]);\n"
		    "dashboard.draw(data);\n"
		"}\n")
	elif stats_nm == 'user_counts_per_day':
	    field_nm = 'yyyy-mm-dd'
	    strfilter_nm = field_nm.replace('-', '_') + 'Filter'
	    slider_nm = 'numRangeSlider1'
            dash_components = (self._write_table_chart('table_div')
				+ self._write_string_filter('filterColumns', strfilter_nm, field_nm)
				+ self._write_NumRangeFilter(slider_nm, 'number_filter_div1',
							'numOfUsers', 1, 100, 1, 50)
				+ self._write_line_chart('lineChart', 'line_div',
							660, 500, 'user counts per day', [0,1]))
	    dashboard = ("\n"
		    "var dashboard = new google.visualization.Dashboard(document.querySelector('#dashboard_div'));\n"
		    "dashboard.bind([" + slider_nm + "," + strfilter_nm + "], [table]);\n"
		    "dashboard.bind([" + slider_nm + "," + strfilter_nm + "], [lineChart]);\n"
		    "dashboard.draw(data);\n"
		"}\n")

        return dash_components + dashboard

    def _write_dashboard(self):
        """
        _write_dashboard: writes the dashboard layout and bind controls with charts
        """
        #the dashboard components (table, charts and filters)
        dash_components = self._write_charts()
        dashboard = ("\n"
            "var dashboard = new google.visualization.Dashboard(document.querySelector('#dashboard_div'));\n"
            "dashboard.bind([categoryPicker], [pieChart, lineChart],[table]);\n"
            "//dashboard.bind([callsRangeSlider], [pieChart]);\n"
            "dashboard.bind([timeRangeSlider], [pieChart, lineChart]);\n"
            "dashboard.bind([stringFilter], [table]);\n"
            "dashboard.draw(data);\n"
        "}\n")

        return dash_components + dashboard

    def _write_footcontent(self, report_title="Report_title_here", stats_nm=''):
        footContent = "</script></head>\n<body>\n"
        footContent += "<h4>" + report_title + "</h4>\n"
        footContent += "  <div id='dashboard_div'>\n"

	if stats_nm == 'user_counts_per_day':
	    footContent += "<table class='columns'><tr>\n" \
        	"<td width='30%'><div id='string_filter_div'></div></td>\n" \
        	"<td><div id='number_filter_div1'></div></td></tr>\n" \
        	"<tr><td><div id='table_div'></div></td>\n" \
        	"<td><div id='line_div'></div></td>\n" \
        	"</tr></table>\n"
	else:
            footContent += "<div id='cat_picker_div'></div>\n" \
                "<div id='number_filter_div'></div>\n" \
                "<div style='display: inline-block'>\n" \
                "<div id='number_filter_div1'></div>\n" \
                "<div id='chart_div'></div>\n" \
                "</div>\n" \
                "<div style='display: inline-block'>\n" \
                "<div id='number_filter_div2'></div>\n" \
                "<div id='line_div'></div>\n" \
                "</div>\n" \
                "<div id='string_filter_div'></div>\n" \
                "<div id='table_div'></div>\n"

	footContent += "</div>\n</body>\n</html>"

        return footContent

    def _write_html(self, out_dir, input_dt, col_caps=None):
        log('\nInput json with {} data items\n'.format(len(input_dt)))
        dt = input_dt[0:200]#For the sake of testing, limit the rows for datatable

        headContent = self._write_headContent()

        if col_caps is None:
            callbackFunc = self._write_callback_function(dt)
        else:
            callbackFunc = self._write_callback_function(dt, col_caps)

        dashboard = self._write_dashboard()

        footContent = self._write_footcontent()

        html_str = headContent + callbackFunc + dashboard + footContent
        #log(html_str)

        html_file_path = os.path.join(out_dir, 'metrics_report_charts.html')

        with open(html_file_path, 'w') as html_file:
                html_file.write(html_str)

        return {'html_file': html_str, 'html_path': html_file_path}


    def _generate_html_report(self, out_dir, dt_info, col_caps=None):
        """
        _generate_html_report: generate html report given the json data

        """
        #log('start generating html report')
        html_report = list()

        if col_caps is None:
            html_file_path = self._write_html(out_dir, dt_info)
        else:
            html_file_path = self._write_html(out_dir, dt_info, col_caps)

        rpt_title = 'Report with charts'

        #log(html_file_path['html_file'])
        html_report.append({'path': html_file_path['html_path'],
                            'name': rpt_title,
                            'label': rpt_title,
                            'description': 'The report with charts'
                        })

        return html_report



