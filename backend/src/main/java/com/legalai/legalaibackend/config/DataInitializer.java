package com.legalai.legalaibackend.config;

import com.legalai.legalaibackend.entity.DocumentType;
import com.legalai.legalaibackend.entity.MandatoryClause;
import com.legalai.legalaibackend.repository.DocumentTypeRepository;
import com.legalai.legalaibackend.repository.MandatoryClauseRepository;
import jakarta.annotation.PostConstruct;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

@Component
public class DataInitializer {

    @Autowired
    private DocumentTypeRepository documentTypeRepository;

    @Autowired
    private MandatoryClauseRepository mandatoryClauseRepository;

    @PostConstruct
    public void init() {

        if (documentTypeRepository.count() > 0) {
            return;
        }

        loadDocumentTypes();
    }

    private void loadDocumentTypes() {

        Map<String, List<String>> documents = new LinkedHashMap<>();

        // ==========================================================
        // RENTAL
        // ==========================================================

        documents.put("RENTAL_AGREEMENT", List.of(
                "PARTIES",
                "PROPERTY_DETAILS",
                "RENT",
                "SECURITY_DEPOSIT",
                "NOTICE_PERIOD",
                "TERMINATION",
                "MAINTENANCE",
                "DISPUTE_RESOLUTION",
                "SIGNATURES"
        ));

        documents.put("LEASE_AGREEMENT", List.of(
                "PARTIES",
                "LEASE_PERIOD",
                "RENT",
                "SECURITY_DEPOSIT",
                "MAINTENANCE",
                "TERMINATION",
                "DISPUTE_RESOLUTION",
                "SIGNATURES"
        ));

        // ==========================================================
        // PROPERTY
        // ==========================================================

        documents.put("PROPERTY_AGREEMENT", List.of(
                "PARTIES",
                "PROPERTY_DETAILS",
                "SALE_PRICE",
                "PAYMENT_TERMS",
                "OWNERSHIP",
                "REGISTRATION",
                "DISPUTE_RESOLUTION",
                "SIGNATURES"
        ));

        documents.put("PROPERTY_SALE_DEED", List.of(
                "PARTIES",
                "PROPERTY_DETAILS",
                "SALE_PRICE",
                "TRANSFER_OF_OWNERSHIP",
                "REGISTRATION",
                "STAMP_DUTY",
                "SIGNATURES"
        ));

        // ==========================================================
        // POWER OF ATTORNEY
        // ==========================================================

        documents.put("POWER_OF_ATTORNEY", List.of(
                "PRINCIPAL",
                "AGENT",
                "POWERS_GRANTED",
                "LIMITATIONS",
                "VALIDITY",
                "REVOCATION",
                "SIGNATURES"
        ));

        documents.put("GENERAL_POWER_OF_ATTORNEY", List.of(
                "PRINCIPAL",
                "AGENT",
                "POWERS_GRANTED",
                "VALIDITY",
                "REVOCATION",
                "SIGNATURES"
        ));

        documents.put("SPECIAL_POWER_OF_ATTORNEY", List.of(
                "PRINCIPAL",
                "AGENT",
                "SPECIFIC_POWER",
                "VALIDITY",
                "REVOCATION",
                "SIGNATURES"
        ));

        // ==========================================================
        // EMPLOYMENT
        // ==========================================================

        documents.put("EMPLOYMENT_CONTRACT", List.of(
                "PARTIES",
                "JOB_ROLE",
                "SALARY",
                "WORKING_HOURS",
                "LEAVE_POLICY",
                "BENEFITS",
                "NOTICE_PERIOD",
                "TERMINATION",
                "CONFIDENTIALITY",
                "SIGNATURES"
        ));

        documents.put("APPOINTMENT_LETTER", List.of(
                "EMPLOYEE",
                "EMPLOYER",
                "JOB_ROLE",
                "SALARY",
                "DATE_OF_JOINING",
                "SIGNATURES"
        ));

        // ==========================================================
        // SERVICE
        // ==========================================================

        documents.put("SERVICE_AGREEMENT", List.of(
                "PARTIES",
                "SERVICES",
                "PAYMENT",
                "CONFIDENTIALITY",
                "LIABILITY",
                "TERMINATION",
                "DISPUTE_RESOLUTION",
                "SIGNATURES"
        ));

        documents.put("CONSULTANCY_AGREEMENT", List.of(
                "PARTIES",
                "CONSULTING_SERVICES",
                "PAYMENT",
                "CONFIDENTIALITY",
                "TERM",
                "TERMINATION",
                "SIGNATURES"
        ));

        documents.put("FREELANCER_AGREEMENT", List.of(
                "PARTIES",
                "WORK_SCOPE",
                "PAYMENT",
                "DEADLINES",
                "CONFIDENTIALITY",
                "SIGNATURES"
        ));

        // ==========================================================
        // NDA
        // ==========================================================

        documents.put("NON_DISCLOSURE_AGREEMENT", List.of(
                "PARTIES",
                "CONFIDENTIAL_INFORMATION",
                "OBLIGATIONS",
                "EXCEPTIONS",
                "TERM",
                "SIGNATURES"
        ));

        documents.put("NON_COMPETE_AGREEMENT", List.of(
                "PARTIES",
                "RESTRICTIONS",
                "DURATION",
                "LOCATION",
                "COMPENSATION",
                "SIGNATURES"
        ));

        // ==========================================================
        // BUSINESS
        // ==========================================================

        documents.put("PARTNERSHIP_DEED", List.of(
                "PARTNERS",
                "CAPITAL_CONTRIBUTION",
                "PROFIT_SHARING",
                "DUTIES",
                "DISSOLUTION",
                "SIGNATURES"
        ));

        documents.put("LLP_AGREEMENT", List.of(
                "PARTNERS",
                "CAPITAL",
                "MANAGEMENT",
                "PROFIT_SHARING",
                "EXIT",
                "SIGNATURES"
        ));

        documents.put("SHAREHOLDERS_AGREEMENT", List.of(
                "PARTIES",
                "SHARES",
                "VOTING_RIGHTS",
                "TRANSFER_RESTRICTIONS",
                "EXIT",
                "SIGNATURES"
        ));

        // ==========================================================
        // LOAN
        // ==========================================================

        documents.put("LOAN_AGREEMENT", List.of(
                "PARTIES",
                "LOAN_AMOUNT",
                "INTEREST_RATE",
                "REPAYMENT",
                "DEFAULT",
                "PENALTY",
                "SECURITY",
                "SIGNATURES"
        ));

        documents.put("HOME_LOAN_AGREEMENT", List.of(
                "PARTIES",
                "PROPERTY_DETAILS",
                "LOAN_AMOUNT",
                "INTEREST_RATE",
                "EMI",
                "DEFAULT",
                "SIGNATURES"
        ));

        documents.put("PERSONAL_LOAN_AGREEMENT", List.of(
                "PARTIES",
                "LOAN_AMOUNT",
                "INTEREST_RATE",
                "REPAYMENT",
                "DEFAULT",
                "SIGNATURES"
        ));

        // ==========================================================
        // FAMILY
        // ==========================================================

        documents.put("DIVORCE_AGREEMENT", List.of(
                "PARTIES",
                "PROPERTY_DIVISION",
                "CHILD_CUSTODY",
                "ALIMONY",
                "DISPUTE_RESOLUTION",
                "SIGNATURES"
        ));

        documents.put("MARRIAGE_AGREEMENT", List.of(
                "PARTIES",
                "PROPERTY",
                "FINANCIAL_TERMS",
                "RESPONSIBILITIES",
                "SIGNATURES"
        ));

        // ==========================================================
        // LEGAL NOTICE
        // ==========================================================

        documents.put("LEGAL_NOTICE", List.of(
                "SENDER",
                "RECIPIENT",
                "SUBJECT",
                "CLAIM",
                "TIME_LIMIT",
                "SIGNATURE"
        ));

        documents.put("COURT_NOTICE", List.of(
                "COURT",
                "CASE_NUMBER",
                "PARTIES",
                "HEARING_DATE",
                "ORDER",
                "SIGNATURE"
        ));

        documents.put("GOVERNMENT_NOTICE", List.of(
                "AUTHORITY",
                "NOTICE_DETAILS",
                "LEGAL_REFERENCE",
                "COMPLIANCE",
                "SIGNATURE"
        ));

        // ==========================================================
        // WILL
        // ==========================================================

        documents.put("WILL", List.of(
                "TESTATOR",
                "BENEFICIARIES",
                "EXECUTOR",
                "ASSETS",
                "WITNESSES",
                "SIGNATURES"
        ));

        documents.put("TRUST_DEED", List.of(
                "SETTLOR",
                "TRUSTEES",
                "BENEFICIARIES",
                "TRUST_PROPERTY",
                "OBJECTIVES",
                "SIGNATURES"
        ));

        // ==========================================================
        // INSURANCE
        // ==========================================================

        documents.put("INSURANCE_POLICY", List.of(
                "POLICY_HOLDER",
                "INSURER",
                "PREMIUM",
                "COVERAGE",
                "EXCLUSIONS",
                "CLAIM_PROCESS",
                "SIGNATURES"
        ));

        // ==========================================================
        // BUSINESS CONTRACTS
        // ==========================================================

        documents.put("FRANCHISE_AGREEMENT", List.of(
                "PARTIES",
                "FRANCHISE_RIGHTS",
                "FEES",
                "ROYALTY",
                "TERM",
                "TERMINATION",
                "SIGNATURES"
        ));

        documents.put("ARBITRATION_AGREEMENT", List.of(
                "PARTIES",
                "ARBITRATOR",
                "PROCEDURE",
                "JURISDICTION",
                "AWARD",
                "SIGNATURES"
        ));

        documents.put("CONSTRUCTION_CONTRACT", List.of(
                "PARTIES",
                "PROJECT_SCOPE",
                "PAYMENT",
                "TIMELINE",
                "PENALTY",
                "QUALITY",
                "SIGNATURES"
        ));


        // ==========================================================
        // COURT
        // ==========================================================

        documents.put("COURT_ORDER", List.of(
                "COURT",
                "CASE_NUMBER",
                "ORDER",
                "DATE",
                "JUDGE",
                "SIGNATURE"
        ));

        documents.put("COURT_JUDGMENT", List.of(
                "COURT",
                "CASE_NUMBER",
                "PARTIES",
                "JUDGMENT",
                "ORDER",
                "SIGNATURE"
        ));

        documents.put("BAIL_ORDER", List.of(
                "COURT",
                "CASE_NUMBER",
                "BAIL_CONDITIONS",
                "DATE",
                "SIGNATURE"
        ));

        documents.put("FIR_DOCUMENT", List.of(
                "POLICE_STATION",
                "COMPLAINANT",
                "ACCUSED",
                "OFFENCE",
                "DATE",
                "SIGNATURE"
        ));


        // ==========================================================
        // GOVERNMENT
        // ==========================================================

        documents.put("TAX_NOTICE", List.of(
                "AUTHORITY",
                "TAX_DETAILS",
                "AMOUNT",
                "DUE_DATE",
                "SIGNATURE"
        ));

        documents.put("GST_NOTICE", List.of(
                "AUTHORITY",
                "GST_NUMBER",
                "NOTICE",
                "COMPLIANCE",
                "SIGNATURE"
        ));

        documents.put("INCOME_TAX_NOTICE", List.of(
                "AUTHORITY",
                "PAN",
                "ASSESSMENT_YEAR",
                "NOTICE",
                "SIGNATURE"
        ));

        documents.put("MUNICIPAL_NOTICE", List.of(
                "AUTHORITY",
                "PROPERTY",
                "NOTICE",
                "COMPLIANCE",
                "SIGNATURE"
        ));


        // ==========================================================
        // INTELLECTUAL PROPERTY
        // ==========================================================

        documents.put("PATENT_LICENSE", List.of(
                "PARTIES",
                "PATENT",
                "LICENSE",
                "ROYALTY",
                "TERM",
                "SIGNATURES"
        ));

        documents.put("COPYRIGHT_AGREEMENT", List.of(
                "PARTIES",
                "WORK",
                "OWNERSHIP",
                "RIGHTS",
                "SIGNATURES"
        ));

        documents.put("TRADEMARK_LICENSE", List.of(
                "PARTIES",
                "TRADEMARK",
                "LICENSE",
                "TERM",
                "SIGNATURES"
        ));

        documents.put("SOFTWARE_LICENSE", List.of(
                "PARTIES",
                "SOFTWARE",
                "LICENSE",
                "RESTRICTIONS",
                "SIGNATURES"
        ));

        // ==========================================================
        // INSURANCE
        // ==========================================================

        documents.put("HEALTH_INSURANCE", List.of(
                "POLICY_HOLDER",
                "INSURER",
                "PREMIUM",
                "COVERAGE",
                "CLAIMS",
                "SIGNATURES"
        ));

        documents.put("LIFE_INSURANCE", List.of(
                "POLICY_HOLDER",
                "NOMINEE",
                "SUM_ASSURED",
                "PREMIUM",
                "SIGNATURES"
        ));

        documents.put("VEHICLE_INSURANCE", List.of(
                "OWNER",
                "VEHICLE",
                "PREMIUM",
                "COVERAGE",
                "CLAIMS",
                "SIGNATURES"
        ));


        // ==========================================================
        // SAVE TO DATABASE
        // ==========================================================

        documents.put("ARCHITECT_AGREEMENT", List.of(
                "PARTIES",
                "PROJECT",
                "FEES",
                "RESPONSIBILITIES",
                "SIGNATURES"
        ));

        documents.put("WORK_ORDER", List.of(
                "PARTIES",
                "WORK_SCOPE",
                "PAYMENT",
                "TIMELINE",
                "SIGNATURES"
        ));

        documents.put("PROJECT_CONTRACT", List.of(
                "PARTIES",
                "PROJECT_SCOPE",
                "PAYMENT",
                "TIMELINE",
                "QUALITY",
                "SIGNATURES"
        ));


        // ==========================================================
        // ESTATE
        // ==========================================================

        documents.put("SUCCESSION_CERTIFICATE", List.of(
                "DECEASED",
                "LEGAL_HEIRS",
                "PROPERTY",
                "COURT",
                "SIGNATURES"
        ));

        documents.put("NOMINATION_FORM", List.of(
                "OWNER",
                "NOMINEE",
                "ASSETS",
                "SIGNATURES"
        ));

        // ==========================================================
        // SAVE TO DATABASE
        // ==========================================================

        for (Map.Entry<String, List<String>> entry : documents.entrySet()) {

            DocumentType documentType = new DocumentType();
            documentType.setName(entry.getKey());

            documentType = documentTypeRepository.save(documentType);

            for (String clause : entry.getValue()) {

                MandatoryClause mandatoryClause = new MandatoryClause();
                mandatoryClause.setClauseName(clause);
                mandatoryClause.setDocumentType(documentType);

                mandatoryClauseRepository.save(mandatoryClause);
            }
        }
    }
}