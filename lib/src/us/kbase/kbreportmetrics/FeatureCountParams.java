
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
 * <p>Original spec-file type: FeatureCountParams</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "genome_file_urls",
    "file_format",
    "genome_source",
    "genome_domain",
    "refseq_category",
    "workspace_name",
    "create_report"
})
public class FeatureCountParams {

    @JsonProperty("genome_file_urls")
    private List<String> genomeFileUrls;
    @JsonProperty("file_format")
    private java.lang.String fileFormat;
    @JsonProperty("genome_source")
    private java.lang.String genomeSource;
    @JsonProperty("genome_domain")
    private java.lang.String genomeDomain;
    @JsonProperty("refseq_category")
    private java.lang.String refseqCategory;
    @JsonProperty("workspace_name")
    private java.lang.String workspaceName;
    @JsonProperty("create_report")
    private Long createReport;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("genome_file_urls")
    public List<String> getGenomeFileUrls() {
        return genomeFileUrls;
    }

    @JsonProperty("genome_file_urls")
    public void setGenomeFileUrls(List<String> genomeFileUrls) {
        this.genomeFileUrls = genomeFileUrls;
    }

    public FeatureCountParams withGenomeFileUrls(List<String> genomeFileUrls) {
        this.genomeFileUrls = genomeFileUrls;
        return this;
    }

    @JsonProperty("file_format")
    public java.lang.String getFileFormat() {
        return fileFormat;
    }

    @JsonProperty("file_format")
    public void setFileFormat(java.lang.String fileFormat) {
        this.fileFormat = fileFormat;
    }

    public FeatureCountParams withFileFormat(java.lang.String fileFormat) {
        this.fileFormat = fileFormat;
        return this;
    }

    @JsonProperty("genome_source")
    public java.lang.String getGenomeSource() {
        return genomeSource;
    }

    @JsonProperty("genome_source")
    public void setGenomeSource(java.lang.String genomeSource) {
        this.genomeSource = genomeSource;
    }

    public FeatureCountParams withGenomeSource(java.lang.String genomeSource) {
        this.genomeSource = genomeSource;
        return this;
    }

    @JsonProperty("genome_domain")
    public java.lang.String getGenomeDomain() {
        return genomeDomain;
    }

    @JsonProperty("genome_domain")
    public void setGenomeDomain(java.lang.String genomeDomain) {
        this.genomeDomain = genomeDomain;
    }

    public FeatureCountParams withGenomeDomain(java.lang.String genomeDomain) {
        this.genomeDomain = genomeDomain;
        return this;
    }

    @JsonProperty("refseq_category")
    public java.lang.String getRefseqCategory() {
        return refseqCategory;
    }

    @JsonProperty("refseq_category")
    public void setRefseqCategory(java.lang.String refseqCategory) {
        this.refseqCategory = refseqCategory;
    }

    public FeatureCountParams withRefseqCategory(java.lang.String refseqCategory) {
        this.refseqCategory = refseqCategory;
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

    public FeatureCountParams withWorkspaceName(java.lang.String workspaceName) {
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

    public FeatureCountParams withCreateReport(Long createReport) {
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
        return ((((((((((((((((("FeatureCountParams"+" [genomeFileUrls=")+ genomeFileUrls)+", fileFormat=")+ fileFormat)+", genomeSource=")+ genomeSource)+", genomeDomain=")+ genomeDomain)+", refseqCategory=")+ refseqCategory)+", workspaceName=")+ workspaceName)+", createReport=")+ createReport)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
