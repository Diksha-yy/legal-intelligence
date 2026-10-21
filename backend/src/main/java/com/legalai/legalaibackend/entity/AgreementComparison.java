package com.legalai.legalaibackend.entity;

import jakarta.persistence.*;
import lombok.*;
import com.legalai.legalaibackend.enums.ComparisonStatus;

import java.time.LocalDateTime;

@Entity
@Table(name = "agreement_comparisons")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class AgreementComparison {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    /**
     * First document version
     */
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "version_a_document_id", nullable = false)
    private Document versionADocument;

    /**
     * Second document version
     */
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "version_b_document_id", nullable = false)
    private Document versionBDocument;

    /**
     * Overall comparison summary returned by AI
     */
    @Column(columnDefinition = "TEXT")
    private String comparisonSummary;

    /**
     * Raw comparison response (JSON/String)
     */
    @Lob
    @Column(columnDefinition = "LONGTEXT")
    private String comparisonResult;

    /**
     * Statistics
     */
    private Integer totalClausesCompared;

    private Integer matchedClauses;

    private Integer modifiedClauses;

    private Integer addedClauses;

    private Integer removedClauses;

    /**
     * AI model used
     */
    private String comparisonModel;

    /**
     * Current processing status
     */
    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private ComparisonStatus comparisonStatus;

    /**
     * Audit fields
     */
    private LocalDateTime createdAt;

    private LocalDateTime updatedAt;

    @PrePersist
    public void onCreate() {
        this.createdAt = LocalDateTime.now();
        this.updatedAt = LocalDateTime.now();

        if (comparisonStatus == null) {
            comparisonStatus = ComparisonStatus.PENDING;
        }
    }

    @PreUpdate
    public void onUpdate() {
        this.updatedAt = LocalDateTime.now();
    }
}