package us.kbase.kbmetrics;

import com.fasterxml.jackson.core.type.TypeReference;
import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import us.kbase.auth.AuthToken;
import us.kbase.common.service.JsonClientCaller;
import us.kbase.common.service.JsonClientException;
import us.kbase.common.service.RpcContext;
import us.kbase.common.service.UnauthorizedException;

/**
 * <p>Original spec-file module name: kb_Metrics</p>
 * <pre>
 * A KBase module: kb_Metrics
 * This KBase SDK module implements methods for generating various KBase metrics.
 * </pre>
 */
public class KbMetricsClient {
    private JsonClientCaller caller;
    private String serviceVersion = null;


    /** Constructs a client with a custom URL and no user credentials.
     * @param url the URL of the service.
     */
    public KbMetricsClient(URL url) {
        caller = new JsonClientCaller(url);
    }
    /** Constructs a client with a custom URL.
     * @param url the URL of the service.
     * @param token the user's authorization token.
     * @throws UnauthorizedException if the token is not valid.
     * @throws IOException if an IOException occurs when checking the token's
     * validity.
     */
    public KbMetricsClient(URL url, AuthToken token) throws UnauthorizedException, IOException {
        caller = new JsonClientCaller(url, token);
    }

    /** Constructs a client with a custom URL.
     * @param url the URL of the service.
     * @param user the user name.
     * @param password the password for the user name.
     * @throws UnauthorizedException if the credentials are not valid.
     * @throws IOException if an IOException occurs when checking the user's
     * credentials.
     */
    public KbMetricsClient(URL url, String user, String password) throws UnauthorizedException, IOException {
        caller = new JsonClientCaller(url, user, password);
    }

    /** Constructs a client with a custom URL
     * and a custom authorization service URL.
     * @param url the URL of the service.
     * @param user the user name.
     * @param password the password for the user name.
     * @param auth the URL of the authorization server.
     * @throws UnauthorizedException if the credentials are not valid.
     * @throws IOException if an IOException occurs when checking the user's
     * credentials.
     */
    public KbMetricsClient(URL url, String user, String password, URL auth) throws UnauthorizedException, IOException {
        caller = new JsonClientCaller(url, user, password, auth);
    }

    /** Get the token this client uses to communicate with the server.
     * @return the authorization token.
     */
    public AuthToken getToken() {
        return caller.getToken();
    }

    /** Get the URL of the service with which this client communicates.
     * @return the service URL.
     */
    public URL getURL() {
        return caller.getURL();
    }

    /** Set the timeout between establishing a connection to a server and
     * receiving a response. A value of zero or null implies no timeout.
     * @param milliseconds the milliseconds to wait before timing out when
     * attempting to read from a server.
     */
    public void setConnectionReadTimeOut(Integer milliseconds) {
        this.caller.setConnectionReadTimeOut(milliseconds);
    }

    /** Check if this client allows insecure http (vs https) connections.
     * @return true if insecure connections are allowed.
     */
    public boolean isInsecureHttpConnectionAllowed() {
        return caller.isInsecureHttpConnectionAllowed();
    }

    /** Deprecated. Use isInsecureHttpConnectionAllowed().
     * @deprecated
     */
    public boolean isAuthAllowedForHttp() {
        return caller.isAuthAllowedForHttp();
    }

    /** Set whether insecure http (vs https) connections should be allowed by
     * this client.
     * @param allowed true to allow insecure connections. Default false
     */
    public void setIsInsecureHttpConnectionAllowed(boolean allowed) {
        caller.setInsecureHttpConnectionAllowed(allowed);
    }

    /** Deprecated. Use setIsInsecureHttpConnectionAllowed().
     * @deprecated
     */
    public void setAuthAllowedForHttp(boolean isAuthAllowedForHttp) {
        caller.setAuthAllowedForHttp(isAuthAllowedForHttp);
    }

    /** Set whether all SSL certificates, including self-signed certificates,
     * should be trusted.
     * @param trustAll true to trust all certificates. Default false.
     */
    public void setAllSSLCertificatesTrusted(final boolean trustAll) {
        caller.setAllSSLCertificatesTrusted(trustAll);
    }
    
    /** Check if this client trusts all SSL certificates, including
     * self-signed certificates.
     * @return true if all certificates are trusted.
     */
    public boolean isAllSSLCertificatesTrusted() {
        return caller.isAllSSLCertificatesTrusted();
    }
    /** Sets streaming mode on. In this case, the data will be streamed to
     * the server in chunks as it is read from disk rather than buffered in
     * memory. Many servers are not compatible with this feature.
     * @param streamRequest true to set streaming mode on, false otherwise.
     */
    public void setStreamingModeOn(boolean streamRequest) {
        caller.setStreamingModeOn(streamRequest);
    }

    /** Returns true if streaming mode is on.
     * @return true if streaming mode is on.
     */
    public boolean isStreamingModeOn() {
        return caller.isStreamingModeOn();
    }

    public void _setFileForNextRpcResponse(File f) {
        caller.setFileForNextRpcResponse(f);
    }

    public String getServiceVersion() {
        return this.serviceVersion;
    }

    public void setServiceVersion(String newValue) {
        this.serviceVersion = newValue;
    }

    /**
     * <p>Original spec-file function name: count_ncbi_genome_features</p>
     * <pre>
     * The actual function is declared using 'funcdef' to specify the name
     * and input/return arguments to the function.  For all typical KBase
     * Apps that run in the Narrative, your function should have the 
     * 'authentication required' modifier.
     * </pre>
     * @param   params   instance of type {@link us.kbase.kbmetrics.FeatureCountParams FeatureCountParams}
     * @return   parameter "output" of type {@link us.kbase.kbmetrics.StatResults StatResults}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public StatResults countNcbiGenomeFeatures(FeatureCountParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<StatResults>> retType = new TypeReference<List<StatResults>>() {};
        List<StatResults> res = caller.jsonrpcCall("kb_Metrics.count_ncbi_genome_features", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: count_genome_features</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.kbmetrics.FeatureCountParams FeatureCountParams}
     * @return   parameter "output" of type {@link us.kbase.kbmetrics.StatResults StatResults}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public StatResults countGenomeFeatures(FeatureCountParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<StatResults>> retType = new TypeReference<List<StatResults>>() {};
        List<StatResults> res = caller.jsonrpcCall("kb_Metrics.count_genome_features", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: refseq_genome_counts</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.kbmetrics.GenomeCountParams GenomeCountParams}
     * @return   parameter "output" of type {@link us.kbase.kbmetrics.StatResults StatResults}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public StatResults refseqGenomeCounts(GenomeCountParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<StatResults>> retType = new TypeReference<List<StatResults>>() {};
        List<StatResults> res = caller.jsonrpcCall("kb_Metrics.refseq_genome_counts", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: report_metrics</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.kbmetrics.StatsReportParams StatsReportParams}
     * @return   parameter "output" of type {@link us.kbase.kbmetrics.StatResults StatResults}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public StatResults reportMetrics(StatsReportParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<StatResults>> retType = new TypeReference<List<StatResults>>() {};
        List<StatResults> res = caller.jsonrpcCall("kb_Metrics.report_metrics", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: dummy_test0</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.kbmetrics.StatsReportParams StatsReportParams}
     * @return   parameter "output" of type {@link us.kbase.kbmetrics.StatResults StatResults}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public StatResults dummyTest0(StatsReportParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<StatResults>> retType = new TypeReference<List<StatResults>>() {};
        List<StatResults> res = caller.jsonrpcCall("kb_Metrics.dummy_test0", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_app_metrics</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.kbmetrics.AppMetricsParams AppMetricsParams}
     * @return   parameter "output" of type {@link us.kbase.kbmetrics.AppMetricsResult AppMetricsResult}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public AppMetricsResult getAppMetrics(AppMetricsParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<AppMetricsResult>> retType = new TypeReference<List<AppMetricsResult>>() {};
        List<AppMetricsResult> res = caller.jsonrpcCall("kb_Metrics.get_app_metrics", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_user_metrics</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.kbmetrics.UserMetricsParams UserMetricsParams}
     * @return   parameter "output" of type {@link us.kbase.kbmetrics.UserMetricsResult UserMetricsResult}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public UserMetricsResult getUserMetrics(UserMetricsParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<UserMetricsResult>> retType = new TypeReference<List<UserMetricsResult>>() {};
        List<UserMetricsResult> res = caller.jsonrpcCall("kb_Metrics.get_user_metrics", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_user_job_states</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.kbmetrics.UserJobStatesParams UserJobStatesParams}
     * @return   parameter "ujs_records" of type {@link us.kbase.kbmetrics.UserJobStatesResult UserJobStatesResult}
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public UserJobStatesResult getUserJobStates(UserJobStatesParams params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<UserJobStatesResult>> retType = new TypeReference<List<UserJobStatesResult>>() {};
        List<UserJobStatesResult> res = caller.jsonrpcCall("kb_Metrics.get_user_job_states", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    public Map<String, Object> status(RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        TypeReference<List<Map<String, Object>>> retType = new TypeReference<List<Map<String, Object>>>() {};
        List<Map<String, Object>> res = caller.jsonrpcCall("kb_Metrics.status", args, retType, true, false, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }
}
