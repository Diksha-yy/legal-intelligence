package com.legalai.legalaibackend.engine;

import com.legalai.legalaibackend.dto.RiskFactorDTO;
import com.legalai.legalaibackend.entity.Clause;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;

@Component
public class RiskRuleEngine {

    public List<RiskFactorDTO> calculateRiskFactors(List<Clause> clauses) {

        List<RiskFactorDTO> factors = new ArrayList<>();

        for (Clause clause : clauses) {

            String clauseName = clause.getClauseName() == null
                    ? ""
                    : clause.getClauseName().toUpperCase();

            String clauseText = clause.getClauseText() == null
                    ? ""
                    : clause.getClauseText().toLowerCase();

            if (clauseName.contains("PENALTY")) {
                factors.add(new RiskFactorDTO(
                        "High Penalty Clause",
                        25,
                        "Penalty clause detected."
                ));
            }

            if (clauseName.contains("TERMINATION")) {
                factors.add(new RiskFactorDTO(
                        "Termination Clause",
                        20,
                        "Termination conditions found."
                ));
            }

            if (clauseName.contains("INDEMNITY")) {
                factors.add(new RiskFactorDTO(
                        "Indemnity Clause",
                        15,
                        "Indemnity obligations detected."
                ));
            }

            if (clauseName.contains("ARBITRATION")) {
                factors.add(new RiskFactorDTO(
                        "Arbitration Clause",
                        10,
                        "Dispute resolution clause detected."
                ));
            }

            if (clauseText.contains("non-refundable")
                    || clauseText.contains("non refundable")) {

                factors.add(new RiskFactorDTO(
                        "Non Refundable Amount",
                        20,
                        "Non-refundable condition detected."
                ));
            }

            if (clauseText.contains("security deposit")) {

                factors.add(new RiskFactorDTO(
                        "Security Deposit",
                        10,
                        "Security deposit mentioned."
                ));
            }
        }

        return factors;
    }

    public int calculateTotalScore(List<RiskFactorDTO> factors) {

        return Math.min(
                factors.stream()
                        .mapToInt(RiskFactorDTO::getWeight)
                        .sum(),
                100
        );
    }

    public String determineRiskLevel(int score) {

        if (score <= 30)
            return "LOW";

        if (score <= 60)
            return "MEDIUM";

        if (score <= 80)
            return "HIGH";

        return "CRITICAL";
    }
}