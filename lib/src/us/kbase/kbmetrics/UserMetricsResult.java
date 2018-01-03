
package us.kbase.kbmetrics;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import us.kbase.common.service.UObject;


/**
 * <p>Original spec-file type: UserMetricsResult</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "user_metrics"
})
public class UserMetricsResult {

    @JsonProperty("user_metrics")
    private UObject userMetrics;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("user_metrics")
    public UObject getUserMetrics() {
        return userMetrics;
    }

    @JsonProperty("user_metrics")
    public void setUserMetrics(UObject userMetrics) {
        this.userMetrics = userMetrics;
    }

    public UserMetricsResult withUserMetrics(UObject userMetrics) {
        this.userMetrics = userMetrics;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((("UserMetricsResult"+" [userMetrics=")+ userMetrics)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
