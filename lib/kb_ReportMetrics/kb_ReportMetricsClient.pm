package kb_ReportMetrics::kb_ReportMetricsClient;

use JSON::RPC::Client;
use POSIX;
use strict;
use Data::Dumper;
use URI;
use Bio::KBase::Exceptions;
my $get_time = sub { time, 0 };
eval {
    require Time::HiRes;
    $get_time = sub { Time::HiRes::gettimeofday() };
};

use Bio::KBase::AuthToken;

# Client version should match Impl version
# This is a Semantic Version number,
# http://semver.org
our $VERSION = "0.1.0";

=head1 NAME

kb_ReportMetrics::kb_ReportMetricsClient

=head1 DESCRIPTION


A KBase module: kb_ReportMetrics
This KBase SDK module implements methods for generating reports on various KBase metrics.


=cut

sub new
{
    my($class, $url, @args) = @_;
    

    my $self = {
	client => kb_ReportMetrics::kb_ReportMetricsClient::RpcClient->new,
	url => $url,
	headers => [],
    };

    chomp($self->{hostname} = `hostname`);
    $self->{hostname} ||= 'unknown-host';

    #
    # Set up for propagating KBRPC_TAG and KBRPC_METADATA environment variables through
    # to invoked services. If these values are not set, we create a new tag
    # and a metadata field with basic information about the invoking script.
    #
    if ($ENV{KBRPC_TAG})
    {
	$self->{kbrpc_tag} = $ENV{KBRPC_TAG};
    }
    else
    {
	my ($t, $us) = &$get_time();
	$us = sprintf("%06d", $us);
	my $ts = strftime("%Y-%m-%dT%H:%M:%S.${us}Z", gmtime $t);
	$self->{kbrpc_tag} = "C:$0:$self->{hostname}:$$:$ts";
    }
    push(@{$self->{headers}}, 'Kbrpc-Tag', $self->{kbrpc_tag});

    if ($ENV{KBRPC_METADATA})
    {
	$self->{kbrpc_metadata} = $ENV{KBRPC_METADATA};
	push(@{$self->{headers}}, 'Kbrpc-Metadata', $self->{kbrpc_metadata});
    }

    if ($ENV{KBRPC_ERROR_DEST})
    {
	$self->{kbrpc_error_dest} = $ENV{KBRPC_ERROR_DEST};
	push(@{$self->{headers}}, 'Kbrpc-Errordest', $self->{kbrpc_error_dest});
    }

    #
    # This module requires authentication.
    #
    # We create an auth token, passing through the arguments that we were (hopefully) given.

    {
	my %arg_hash2 = @args;
	if (exists $arg_hash2{"token"}) {
	    $self->{token} = $arg_hash2{"token"};
	} elsif (exists $arg_hash2{"user_id"}) {
	    my $token = Bio::KBase::AuthToken->new(@args);
	    if (!$token->error_message) {
	        $self->{token} = $token->token;
	    }
	}
	
	if (exists $self->{token})
	{
	    $self->{client}->{token} = $self->{token};
	}
    }

    my $ua = $self->{client}->ua;	 
    my $timeout = $ENV{CDMI_TIMEOUT} || (30 * 60);	 
    $ua->timeout($timeout);
    bless $self, $class;
    #    $self->_validate_version();
    return $self;
}




=head2 count_ncbi_genomes

  $return_records = $obj->count_ncbi_genomes($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a kb_ReportMetrics.GenomeCountParams
$return_records is a kb_ReportMetrics.StatsResults
GenomeCountParams is a reference to a hash where the following keys are defined:
	genome_source has a value which is a string
	genome_domain has a value which is a string
	refseq_category has a value which is a string
	workspace_name has a value which is a string
	create_report has a value which is a kb_ReportMetrics.bool
bool is an int
StatsResults is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string

</pre>

=end html

=begin text

$params is a kb_ReportMetrics.GenomeCountParams
$return_records is a kb_ReportMetrics.StatsResults
GenomeCountParams is a reference to a hash where the following keys are defined:
	genome_source has a value which is a string
	genome_domain has a value which is a string
	refseq_category has a value which is a string
	workspace_name has a value which is a string
	create_report has a value which is a kb_ReportMetrics.bool
bool is an int
StatsResults is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string


=end text

=item Description

The actual function is declared using 'funcdef' to specify the name
and input/return arguments to the function.  For all typical KBase
Apps that run in the Narrative, your function should have the 
'authentication required' modifier.

=back

=cut

 sub count_ncbi_genomes
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function count_ncbi_genomes (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to count_ncbi_genomes:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'count_ncbi_genomes');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "kb_ReportMetrics.count_ncbi_genomes",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'count_ncbi_genomes',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method count_ncbi_genomes",
					    status_line => $self->{client}->status_line,
					    method_name => 'count_ncbi_genomes',
				       );
    }
}
 


=head2 count_ncbi_genome_features

  $return_records = $obj->count_ncbi_genome_features($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a kb_ReportMetrics.FeatureCountParams
$return_records is a kb_ReportMetrics.StatsResults
FeatureCountParams is a reference to a hash where the following keys are defined:
	genome_file_urls has a value which is a reference to a list where each element is a string
	file_format has a value which is a string
	genome_source has a value which is a string
	genome_domain has a value which is a string
	refseq_category has a value which is a string
	workspace_name has a value which is a string
	create_report has a value which is a kb_ReportMetrics.bool
bool is an int
StatsResults is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string

</pre>

=end html

=begin text

$params is a kb_ReportMetrics.FeatureCountParams
$return_records is a kb_ReportMetrics.StatsResults
FeatureCountParams is a reference to a hash where the following keys are defined:
	genome_file_urls has a value which is a reference to a list where each element is a string
	file_format has a value which is a string
	genome_source has a value which is a string
	genome_domain has a value which is a string
	refseq_category has a value which is a string
	workspace_name has a value which is a string
	create_report has a value which is a kb_ReportMetrics.bool
bool is an int
StatsResults is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string


=end text

=item Description



=back

=cut

 sub count_ncbi_genome_features
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function count_ncbi_genome_features (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to count_ncbi_genome_features:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'count_ncbi_genome_features');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "kb_ReportMetrics.count_ncbi_genome_features",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'count_ncbi_genome_features',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method count_ncbi_genome_features",
					    status_line => $self->{client}->status_line,
					    method_name => 'count_ncbi_genome_features',
				       );
    }
}
 


=head2 count_genome_features_from_files

  $return_records = $obj->count_genome_features_from_files($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a kb_ReportMetrics.FeatureCountParams
$return_records is a kb_ReportMetrics.StatsResults
FeatureCountParams is a reference to a hash where the following keys are defined:
	genome_file_urls has a value which is a reference to a list where each element is a string
	file_format has a value which is a string
	genome_source has a value which is a string
	genome_domain has a value which is a string
	refseq_category has a value which is a string
	workspace_name has a value which is a string
	create_report has a value which is a kb_ReportMetrics.bool
bool is an int
StatsResults is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string

</pre>

=end html

=begin text

$params is a kb_ReportMetrics.FeatureCountParams
$return_records is a kb_ReportMetrics.StatsResults
FeatureCountParams is a reference to a hash where the following keys are defined:
	genome_file_urls has a value which is a reference to a list where each element is a string
	file_format has a value which is a string
	genome_source has a value which is a string
	genome_domain has a value which is a string
	refseq_category has a value which is a string
	workspace_name has a value which is a string
	create_report has a value which is a kb_ReportMetrics.bool
bool is an int
StatsResults is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string


=end text

=item Description



=back

=cut

 sub count_genome_features_from_files
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function count_genome_features_from_files (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to count_genome_features_from_files:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'count_genome_features_from_files');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "kb_ReportMetrics.count_genome_features_from_files",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'count_genome_features_from_files',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method count_genome_features_from_files",
					    status_line => $self->{client}->status_line,
					    method_name => 'count_genome_features_from_files',
				       );
    }
}
 


=head2 report_metrics

  $return_records = $obj->report_metrics($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a kb_ReportMetrics.StatsReportParams
$return_records is a kb_ReportMetrics.StatsResults
StatsReportParams is a reference to a hash where the following keys are defined:
	stats_name has a value which is a string
	user_ids has a value which is a reference to a list where each element is a kb_ReportMetrics.user_id
	start_time has a value which is a kb_ReportMetrics.timestamp
	end_time has a value which is a kb_ReportMetrics.timestamp
	workspace_name has a value which is a string
	create_report has a value which is a kb_ReportMetrics.bool
user_id is a string
timestamp is a string
bool is an int
StatsResults is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string

</pre>

=end html

=begin text

$params is a kb_ReportMetrics.StatsReportParams
$return_records is a kb_ReportMetrics.StatsResults
StatsReportParams is a reference to a hash where the following keys are defined:
	stats_name has a value which is a string
	user_ids has a value which is a reference to a list where each element is a kb_ReportMetrics.user_id
	start_time has a value which is a kb_ReportMetrics.timestamp
	end_time has a value which is a kb_ReportMetrics.timestamp
	workspace_name has a value which is a string
	create_report has a value which is a kb_ReportMetrics.bool
user_id is a string
timestamp is a string
bool is an int
StatsResults is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string


=end text

=item Description



=back

=cut

 sub report_metrics
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function report_metrics (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to report_metrics:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'report_metrics');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "kb_ReportMetrics.report_metrics",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'report_metrics',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method report_metrics",
					    status_line => $self->{client}->status_line,
					    method_name => 'report_metrics',
				       );
    }
}
 


=head2 dummy_test0

  $return_records = $obj->dummy_test0($params)

=over 4

=item Parameter and return types

=begin html

<pre>
$params is a kb_ReportMetrics.StatsReportParams
$return_records is a kb_ReportMetrics.StatsResults
StatsReportParams is a reference to a hash where the following keys are defined:
	stats_name has a value which is a string
	user_ids has a value which is a reference to a list where each element is a kb_ReportMetrics.user_id
	start_time has a value which is a kb_ReportMetrics.timestamp
	end_time has a value which is a kb_ReportMetrics.timestamp
	workspace_name has a value which is a string
	create_report has a value which is a kb_ReportMetrics.bool
user_id is a string
timestamp is a string
bool is an int
StatsResults is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string

</pre>

=end html

=begin text

$params is a kb_ReportMetrics.StatsReportParams
$return_records is a kb_ReportMetrics.StatsResults
StatsReportParams is a reference to a hash where the following keys are defined:
	stats_name has a value which is a string
	user_ids has a value which is a reference to a list where each element is a kb_ReportMetrics.user_id
	start_time has a value which is a kb_ReportMetrics.timestamp
	end_time has a value which is a kb_ReportMetrics.timestamp
	workspace_name has a value which is a string
	create_report has a value which is a kb_ReportMetrics.bool
user_id is a string
timestamp is a string
bool is an int
StatsResults is a reference to a hash where the following keys are defined:
	report_name has a value which is a string
	report_ref has a value which is a string


=end text

=item Description



=back

=cut

 sub dummy_test0
{
    my($self, @args) = @_;

# Authentication: required

    if ((my $n = @args) != 1)
    {
	Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
							       "Invalid argument count for function dummy_test0 (received $n, expecting 1)");
    }
    {
	my($params) = @args;

	my @_bad_arguments;
        (ref($params) eq 'HASH') or push(@_bad_arguments, "Invalid type for argument 1 \"params\" (value was \"$params\")");
        if (@_bad_arguments) {
	    my $msg = "Invalid arguments passed to dummy_test0:\n" . join("", map { "\t$_\n" } @_bad_arguments);
	    Bio::KBase::Exceptions::ArgumentValidationError->throw(error => $msg,
								   method_name => 'dummy_test0');
	}
    }

    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
	    method => "kb_ReportMetrics.dummy_test0",
	    params => \@args,
    });
    if ($result) {
	if ($result->is_error) {
	    Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
					       code => $result->content->{error}->{code},
					       method_name => 'dummy_test0',
					       data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
					      );
	} else {
	    return wantarray ? @{$result->result} : $result->result->[0];
	}
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method dummy_test0",
					    status_line => $self->{client}->status_line,
					    method_name => 'dummy_test0',
				       );
    }
}
 
  
sub status
{
    my($self, @args) = @_;
    if ((my $n = @args) != 0) {
        Bio::KBase::Exceptions::ArgumentValidationError->throw(error =>
                                   "Invalid argument count for function status (received $n, expecting 0)");
    }
    my $url = $self->{url};
    my $result = $self->{client}->call($url, $self->{headers}, {
        method => "kb_ReportMetrics.status",
        params => \@args,
    });
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(error => $result->error_message,
                           code => $result->content->{error}->{code},
                           method_name => 'status',
                           data => $result->content->{error}->{error} # JSON::RPC::ReturnObject only supports JSONRPC 1.1 or 1.O
                          );
        } else {
            return wantarray ? @{$result->result} : $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(error => "Error invoking method status",
                        status_line => $self->{client}->status_line,
                        method_name => 'status',
                       );
    }
}
   

sub version {
    my ($self) = @_;
    my $result = $self->{client}->call($self->{url}, $self->{headers}, {
        method => "kb_ReportMetrics.version",
        params => [],
    });
    if ($result) {
        if ($result->is_error) {
            Bio::KBase::Exceptions::JSONRPC->throw(
                error => $result->error_message,
                code => $result->content->{code},
                method_name => 'dummy_test0',
            );
        } else {
            return wantarray ? @{$result->result} : $result->result->[0];
        }
    } else {
        Bio::KBase::Exceptions::HTTP->throw(
            error => "Error invoking method dummy_test0",
            status_line => $self->{client}->status_line,
            method_name => 'dummy_test0',
        );
    }
}

sub _validate_version {
    my ($self) = @_;
    my $svr_version = $self->version();
    my $client_version = $VERSION;
    my ($cMajor, $cMinor) = split(/\./, $client_version);
    my ($sMajor, $sMinor) = split(/\./, $svr_version);
    if ($sMajor != $cMajor) {
        Bio::KBase::Exceptions::ClientServerIncompatible->throw(
            error => "Major version numbers differ.",
            server_version => $svr_version,
            client_version => $client_version
        );
    }
    if ($sMinor < $cMinor) {
        Bio::KBase::Exceptions::ClientServerIncompatible->throw(
            error => "Client minor version greater than Server minor version.",
            server_version => $svr_version,
            client_version => $client_version
        );
    }
    if ($sMinor > $cMinor) {
        warn "New client version available for kb_ReportMetrics::kb_ReportMetricsClient\n";
    }
    if ($sMajor == 0) {
        warn "kb_ReportMetrics::kb_ReportMetricsClient version is $svr_version. API subject to change.\n";
    }
}

=head1 TYPES



=head2 bool

=over 4



=item Description

A boolean - 0 for false, 1 for true.
@range (0, 1)


=item Definition

=begin html

<pre>
an int
</pre>

=end html

=begin text

an int

=end text

=back



=head2 GenomeCountParams

=over 4



=item Description

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


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
genome_source has a value which is a string
genome_domain has a value which is a string
refseq_category has a value which is a string
workspace_name has a value which is a string
create_report has a value which is a kb_ReportMetrics.bool

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
genome_source has a value which is a string
genome_domain has a value which is a string
refseq_category has a value which is a string
workspace_name has a value which is a string
create_report has a value which is a kb_ReportMetrics.bool


=end text

=back



=head2 FeatureCountParams

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
genome_file_urls has a value which is a reference to a list where each element is a string
file_format has a value which is a string
genome_source has a value which is a string
genome_domain has a value which is a string
refseq_category has a value which is a string
workspace_name has a value which is a string
create_report has a value which is a kb_ReportMetrics.bool

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
genome_file_urls has a value which is a reference to a list where each element is a string
file_format has a value which is a string
genome_source has a value which is a string
genome_domain has a value which is a string
refseq_category has a value which is a string
workspace_name has a value which is a string
create_report has a value which is a kb_ReportMetrics.bool


=end text

=back



=head2 StatsResults

=over 4



=item Description

Here is the definition of the output of the function.  The output
can be used by other SDK modules which call your code, or the output
visualizations in the Narrative.  'report_name' and 'report_ref' are
special output fields- if defined, the Narrative can automatically
render your Report.


=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
report_name has a value which is a string
report_ref has a value which is a string


=end text

=back



=head2 user_id

=over 4



=item Description

A string for the user id


=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 timestamp

=over 4



=item Description

A time in the format YYYY-MM-DDThh:mm:ssZ, where Z is the difference
in time to UTC in the format +/-HHMM, eg:
        2012-12-17T23:24:06-0500 (EST time)
        2013-04-03T08:56:32+0000 (UTC time)


=item Definition

=begin html

<pre>
a string
</pre>

=end html

=begin text

a string

=end text

=back



=head2 StatsReportParams

=over 4



=item Definition

=begin html

<pre>
a reference to a hash where the following keys are defined:
stats_name has a value which is a string
user_ids has a value which is a reference to a list where each element is a kb_ReportMetrics.user_id
start_time has a value which is a kb_ReportMetrics.timestamp
end_time has a value which is a kb_ReportMetrics.timestamp
workspace_name has a value which is a string
create_report has a value which is a kb_ReportMetrics.bool

</pre>

=end html

=begin text

a reference to a hash where the following keys are defined:
stats_name has a value which is a string
user_ids has a value which is a reference to a list where each element is a kb_ReportMetrics.user_id
start_time has a value which is a kb_ReportMetrics.timestamp
end_time has a value which is a kb_ReportMetrics.timestamp
workspace_name has a value which is a string
create_report has a value which is a kb_ReportMetrics.bool


=end text

=back



=cut

package kb_ReportMetrics::kb_ReportMetricsClient::RpcClient;
use base 'JSON::RPC::Client';
use POSIX;
use strict;

#
# Override JSON::RPC::Client::call because it doesn't handle error returns properly.
#

sub call {
    my ($self, $uri, $headers, $obj) = @_;
    my $result;


    {
	if ($uri =~ /\?/) {
	    $result = $self->_get($uri);
	}
	else {
	    Carp::croak "not hashref." unless (ref $obj eq 'HASH');
	    $result = $self->_post($uri, $headers, $obj);
	}

    }

    my $service = $obj->{method} =~ /^system\./ if ( $obj );

    $self->status_line($result->status_line);

    if ($result->is_success) {

        return unless($result->content); # notification?

        if ($service) {
            return JSON::RPC::ServiceObject->new($result, $self->json);
        }

        return JSON::RPC::ReturnObject->new($result, $self->json);
    }
    elsif ($result->content_type eq 'application/json')
    {
        return JSON::RPC::ReturnObject->new($result, $self->json);
    }
    else {
        return;
    }
}


sub _post {
    my ($self, $uri, $headers, $obj) = @_;
    my $json = $self->json;

    $obj->{version} ||= $self->{version} || '1.1';

    if ($obj->{version} eq '1.0') {
        delete $obj->{version};
        if (exists $obj->{id}) {
            $self->id($obj->{id}) if ($obj->{id}); # if undef, it is notification.
        }
        else {
            $obj->{id} = $self->id || ($self->id('JSON::RPC::Client'));
        }
    }
    else {
        # $obj->{id} = $self->id if (defined $self->id);
	# Assign a random number to the id if one hasn't been set
	$obj->{id} = (defined $self->id) ? $self->id : substr(rand(),2);
    }

    my $content = $json->encode($obj);

    $self->ua->post(
        $uri,
        Content_Type   => $self->{content_type},
        Content        => $content,
        Accept         => 'application/json',
	@$headers,
	($self->{token} ? (Authorization => $self->{token}) : ()),
    );
}



1;
