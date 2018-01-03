
package us.kbase.kbmetrics;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import us.kbase.common.service.Tuple2;


/**
 * <p>Original spec-file type: UserMetricsParams</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "filter_str",
    "time_range"
})
public class UserMetricsParams {

    @JsonProperty("filter_str")
    private java.lang.String filterStr;
    @JsonProperty("time_range")
    private Tuple2 <String, String> timeRange;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("filter_str")
    public java.lang.String getFilterStr() {
        return filterStr;
    }

    @JsonProperty("filter_str")
    public void setFilterStr(java.lang.String filterStr) {
        this.filterStr = filterStr;
    }

    public UserMetricsParams withFilterStr(java.lang.String filterStr) {
        this.filterStr = filterStr;
        return this;
    }

    @JsonProperty("time_range")
    public Tuple2 <String, String> getTimeRange() {
        return timeRange;
    }

    @JsonProperty("time_range")
    public void setTimeRange(Tuple2 <String, String> timeRange) {
        this.timeRange = timeRange;
    }

    public UserMetricsParams withTimeRange(Tuple2 <String, String> timeRange) {
        this.timeRange = timeRange;
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
        return ((((((("UserMetricsParams"+" [filterStr=")+ filterStr)+", timeRange=")+ timeRange)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
