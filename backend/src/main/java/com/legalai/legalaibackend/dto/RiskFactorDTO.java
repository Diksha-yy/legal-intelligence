package com.legalai.legalaibackend.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class RiskFactorDTO {

    private String factor;

    private int weight;

    private String description;
}