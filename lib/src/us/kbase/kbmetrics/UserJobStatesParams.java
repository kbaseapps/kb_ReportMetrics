
package us.kbase.kbmetrics;

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
 * <p>Original spec-file type: UserJobStatesParams</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "user_ids",
    "before",
    "after"
})
public class UserJobStatesParams {

    @JsonProperty("user_ids")
    private List<String> userIds;
    @JsonProperty("before")
    private Long before;
    @JsonProperty("after")
    private Long after;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("user_ids")
    public List<String> getUserIds() {
        return userIds;
    }

    @JsonProperty("user_ids")
    public void setUserIds(List<String> userIds) {
        this.userIds = userIds;
    }

    public UserJobStatesParams withUserIds(List<String> userIds) {
        this.userIds = userIds;
        return this;
    }

    @JsonProperty("before")
    public Long getBefore() {
        return before;
    }

    @JsonProperty("before")
    public void setBefore(Long before) {
        this.before = before;
    }

    public UserJobStatesParams withBefore(Long before) {
        this.before = before;
        return this;
    }

    @JsonProperty("after")
    public Long getAfter() {
        return after;
    }

    @JsonProperty("after")
    public void setAfter(Long after) {
        this.after = after;
    }

    public UserJobStatesParams withAfter(Long after) {
        this.after = after;
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
        return ((((((((("UserJobStatesParams"+" [userIds=")+ userIds)+", before=")+ before)+", after=")+ after)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
