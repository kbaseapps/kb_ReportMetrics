/*
A KBase module: kb_ReportMetrics
This KBase SDK module implements methods for generating reports on various KBase metrics.
*/

module kb_ReportMetrics {
    /* 
        A 'typedef' allows you to provide a more specific name for
        a type.  Built-in primitive types include 'string', 'int',
        'float'.  Here we define a type named assembly_ref to indicate
        a string that should be set to a KBase ID reference to an
        Assembly data object.
    */

    /* A boolean - 0 for false, 1 for true.
        @range (0, 1)
    */
 
    typedef int bool;

    /*
        A 'typedef' can also be used to define compound or container
        objects, like lists, maps, and structures.  The standard KBase
        convention is to use structures, as shown here, to define the
        input and output of your function.  Here the input is a
        reference to the Assembly data object, a workspace to save
        output, and a length threshold for filtering.

        To define lists and maps, use a syntax similar to C++ templates
        to indicate the type contained in the list or map.  For example:

            list <string> list_of_strings;
            mapping <string, int> map_of_ints;
    */
    typedef structure {
        string genome_source;
        string genome_domain;
        string refseq_category;
        string workspace_name;
        bool create_report;
    } GenomeCountParams;

    typedef structure {
        list <string> genome_file_urls;
        string file_format;
        string genome_source;
        string genome_domain;
        string refseq_category;
        string workspace_name;
        bool create_report;
    } FeatureCountParams;

    /*
        Here is the definition of the output of the function.  The output
        can be used by other SDK modules which call your code, or the output
        visualizations in the Narrative.  'report_name' and 'report_ref' are
        special output fields- if defined, the Narrative can automatically
        render your Report.
    */
    typedef structure {
        string report_name;
        string report_ref;
    } StatsResults;

    /*
        The actual function is declared using 'funcdef' to specify the name
        and input/return arguments to the function.  For all typical KBase
        Apps that run in the Narrative, your function should have the 
        'authentication required' modifier.
    */

    funcdef count_ncbi_genomes(GenomeCountParams params)
        returns (StatsResults return_records) authentication required;

    funcdef count_ncbi_genome_features(FeatureCountParams params)
        returns (StatsResults return_records) authentication required;

    funcdef count_genome_features_from_files(FeatureCountParams params)
        returns (StatsResults return_records) authentication required;

    /*
        A string for the user id
    */
    typedef string user_id;

    /* 
        A time in the format YYYY-MM-DDThh:mm:ssZ, where Z is the difference
        in time to UTC in the format +/-HHMM, eg:
                2012-12-17T23:24:06-0500 (EST time)
                2013-04-03T08:56:32+0000 (UTC time)
    */
    typedef string timestamp;

    typedef structure {
        string stats_name;
        list<user_id> user_ids;
        timestamp start_time;
        timestamp end_time;
        string workspace_name;
        bool create_report;
    } StatsReportParams;

    funcdef report_metrics(StatsReportParams params)
        returns (StatsResults return_records) authentication required;

    funcdef dummy_test0(StatsReportParams params)
        returns (StatsResults return_records) authentication required;
    
};
