
package us.kbase.kbreportmetrics;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: GenomeCountParams</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "genome_source",
    "genome_domain",
    "refseq_category",
    "workspace_name",
    "create_report"
})
public class GenomeCountParams {

    @JsonProperty("genome_source")
    private String genomeSource;
    @JsonProperty("genome_domain")
    private String genomeDomain;
    @JsonProperty("refseq_category")
    private String refseqCategory;
    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("create_report")
    private Long createReport;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("genome_source")
    public String getGenomeSource() {
        return genomeSource;
    }

    @JsonProperty("genome_source")
    public void setGenomeSource(String genomeSource) {
        this.genomeSource = genomeSource;
    }

    public GenomeCountParams withGenomeSource(String genomeSource) {
        this.genomeSource = genomeSource;
        return this;
    }

    @JsonProperty("genome_domain")
    public String getGenomeDomain() {
        return genomeDomain;
    }

    @JsonProperty("genome_domain")
    public void setGenomeDomain(String genomeDomain) {
        this.genomeDomain = genomeDomain;
    }

    public GenomeCountParams withGenomeDomain(String genomeDomain) {
        this.genomeDomain = genomeDomain;
        return this;
    }

    @JsonProperty("refseq_category")
    public String getRefseqCategory() {
        return refseqCategory;
    }

    @JsonProperty("refseq_category")
    public void setRefseqCategory(String refseqCategory) {
        this.refseqCategory = refseqCategory;
    }

    public GenomeCountParams withRefseqCategory(String refseqCategory) {
        this.refseqCategory = refseqCategory;
        return this;
    }

    @JsonProperty("workspace_name")
    public String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public GenomeCountParams withWorkspaceName(String workspaceName) {
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

    public GenomeCountParams withCreateReport(Long createReport) {
        this.createReport = createReport;
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
        return ((((((((((((("GenomeCountParams"+" [genomeSource=")+ genomeSource)+", genomeDomain=")+ genomeDomain)+", refseqCategory=")+ refseqCategory)+", workspaceName=")+ workspaceName)+", createReport=")+ createReport)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
