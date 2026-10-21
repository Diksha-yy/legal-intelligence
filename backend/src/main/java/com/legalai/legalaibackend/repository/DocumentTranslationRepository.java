package com.legalai.legalaibackend.repository;

import com.legalai.legalaibackend.entity.Document;
import com.legalai.legalaibackend.entity.DocumentTranslation;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface DocumentTranslationRepository
        extends JpaRepository<DocumentTranslation, Long> {

    Optional<DocumentTranslation> findByDocument(Document document);

}