package com.legalai.legalaibackend.entity;

import jakarta.persistence.*;

import java.util.List;

@Entity
@Table(name = "document_types")
public class DocumentType {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String name;

    @OneToMany(mappedBy = "documentType",
            cascade = CascadeType.ALL,
            orphanRemoval = true)
    private List<MandatoryClause> mandatoryClauses;

    public DocumentType() {
    }

    public DocumentType(Long id,
                        String name,
                        List<MandatoryClause> mandatoryClauses) {
        this.id = id;
        this.name = name;
        this.mandatoryClauses = mandatoryClauses;
    }

    public Long getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public List<MandatoryClause> getMandatoryClauses() {
        return mandatoryClauses;
    }

    public void setMandatoryClauses(List<MandatoryClause> mandatoryClauses) {
        this.mandatoryClauses = mandatoryClauses;
    }
}