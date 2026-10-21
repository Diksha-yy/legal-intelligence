package com.legalai.legalaibackend.dto;

import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ClauseDifferenceDTO {

    private String clauseNumber;

    private String versionAText;

    private String versionBText;

    private String changeType;

    private String remarks;

}