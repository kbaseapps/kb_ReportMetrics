
package us.kbase.kbreportmetrics;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: StatsReportParams</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "stats_name",
    "user_ids",
    "start_time",
    "end_time",
    "workspace_name",
    "create_report"
})
public class StatsReportParams {

    @JsonProperty("stats_name")
    private java.lang.String statsName;
    @JsonProperty("user_ids")
    private List<String> userIds;
    @JsonProperty("start_time")
    private java.lang.String startTime;
    @JsonProperty("end_time")
    private java.lang.String endTime;
    @JsonProperty("workspace_name")
    private java.lang.String workspaceName;
    @JsonProperty("create_report")
    private Long createReport;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("stats_name")
    public java.lang.String getStatsName() {
        return statsName;
    }

    @JsonProperty("stats_name")
    public void setStatsName(java.lang.String statsName) {
        this.statsName = statsName;
    }

    public StatsReportParams withStatsName(java.lang.String statsName) {
        this.statsName = statsName;
        return this;
    }

    @JsonProperty("user_ids")
    public List<String> getUserIds() {
        return userIds;
    }

    @JsonProperty("user_ids")
    public void setUserIds(List<String> userIds) {
        this.userIds = userIds;
    }

    public StatsReportParams withUserIds(List<String> userIds) {
        this.userIds = userIds;
        return this;
    }

    @JsonProperty("start_time")
    public java.lang.String getStartTime() {
        return startTime;
    }

    @JsonProperty("start_time")
    public void setStartTime(java.lang.String startTime) {
        this.startTime = startTime;
    }

    public StatsReportParams withStartTime(java.lang.String startTime) {
        this.startTime = startTime;
        return this;
    }

    @JsonProperty("end_time")
    public java.lang.String getEndTime() {
        return endTime;
    }

    @JsonProperty("end_time")
    public void setEndTime(java.lang.String endTime) {
        this.endTime = endTime;
    }

    public StatsReportParams withEndTime(java.lang.String endTime) {
        this.endTime = endTime;
        return this;
    }

    @JsonProperty("workspace_name")
    public java.lang.String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(java.lang.String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public StatsReportParams withWorkspaceName(java.lang.String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("create_report")
    public Long getCreateReport() {
        return createReport;
    }

    @JsonProperty("create_report")
    public void setCreateReport(Long createReport) {
        this.createReport = createReport;
    }

    public StatsReportParams withCreateReport(Long createReport) {
        this.createReport = createReport;
        return this;
    }

    @JsonAnyGetter
    public Map<java.lang.String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(java.lang.String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public java.lang.String toString() {
        return ((((((((((((((("StatsReportParams"+" [statsName=")+ statsName)+", userIds=")+ userIds)+", startTime=")+ startTime)+", endTime=")+ endTime)+", workspaceName=")+ workspaceName)+", createReport=")+ createReport)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
