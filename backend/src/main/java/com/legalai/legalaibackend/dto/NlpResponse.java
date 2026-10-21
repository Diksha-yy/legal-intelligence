package com.legalai.legalaibackend.dto;

import java.util.List;

public class NlpResponse {

    private List<NlpClauseDto> clauses;

    public NlpResponse() {
    }

    public List<NlpClauseDto> getClauses() {
        return clauses;
    }

    public void setClauses(List<NlpClauseDto> clauses) {
        this.clauses = clauses;
    }
}