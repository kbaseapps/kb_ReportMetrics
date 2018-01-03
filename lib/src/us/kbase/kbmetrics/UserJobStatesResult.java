
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
 * <p>Original spec-file type: UserJobStatesResult</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "user_job_states"
})
public class UserJobStatesResult {

    @JsonProperty("user_job_states")
    private UObject userJobStates;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("user_job_states")
    public UObject getUserJobStates() {
        return userJobStates;
    }

    @JsonProperty("user_job_states")
    public void setUserJobStates(UObject userJobStates) {
        this.userJobStates = userJobStates;
    }

    public UserJobStatesResult withUserJobStates(UObject userJobStates) {
        this.userJobStates = userJobStates;
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
        return ((((("UserJobStatesResult"+" [userJobStates=")+ userJobStates)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
