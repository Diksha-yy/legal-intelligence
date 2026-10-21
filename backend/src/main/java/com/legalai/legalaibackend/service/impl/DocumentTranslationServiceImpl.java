package com.legalai.legalaibackend.service.impl;

import com.legalai.legalaibackend.dto.DocumentTranslationResponse;
import com.legalai.legalaibackend.entity.Document;
import com.legalai.legalaibackend.entity.DocumentTranslation;
import com.legalai.legalaibackend.exception.ResourceNotFoundException;
import com.legalai.legalaibackend.repository.DocumentRepository;
import com.legalai.legalaibackend.repository.DocumentTranslationRepository;
import com.legalai.legalaibackend.service.DocumentTranslationService;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;

@Service
public class DocumentTranslationServiceImpl implements DocumentTranslationService {

    private final DocumentRepository documentRepository;
    private final DocumentTranslationRepository translationRepository;

    public DocumentTranslationServiceImpl(
            DocumentRepository documentRepository,
            DocumentTranslationRepository translationRepository) {

        this.documentRepository = documentRepository;
        this.translationRepository = translationRepository;
    }

    @Override
    public DocumentTranslationResponse generateTranslation(Long documentId, String language) {

        Document document = documentRepository.findById(documentId)
                .orElseThrow(() ->
                        new ResourceNotFoundException("Document not found with id: " + documentId));

        String translatedText = generateMockTranslation(document, language);

        DocumentTranslation translation = translationRepository
                .findByDocument(document)
                .orElse(new DocumentTranslation());

        translation.setDocument(document);
        translation.setSourceLanguage("Original");
        translation.setTargetLanguage(language);
        translation.setTranslatedText(translatedText);
        translation.setTranslationModel("Mock AI");
        translation.setTranslatedAt(LocalDateTime.now());

        translation = translationRepository.save(translation);

        return mapToResponse(translation);
    }

    @Override
    public DocumentTranslationResponse getTranslation(Long documentId) {

        Document document = documentRepository.findById(documentId)
                .orElseThrow(() ->
                        new ResourceNotFoundException("Document not found with id: " + documentId));

        DocumentTranslation translation = translationRepository
                .findByDocument(document)
                .orElseThrow(() ->
                        new ResourceNotFoundException("Translation not found for document id: " + documentId));

        return mapToResponse(translation);
    }

    private String generateMockTranslation(Document document, String language) {

        String title = document.getTitle() != null
                ? document.getTitle()
                : "Document";

        switch (language.toLowerCase()) {

            case "hindi":
                return "यह \"" + title + "\" दस्तावेज़ का हिंदी अनुवाद है।";

            case "marathi":
                return "हा \"" + title + "\" दस्तऐवजाचा मराठी अनुवाद आहे.";

            case "english":
                return "This is the English version of \"" + title + "\".";

            default:
                return "Translated (" + language + ") version of \"" + title + "\".";
        }
    }

    private DocumentTranslationResponse mapToResponse(DocumentTranslation translation) {

        DocumentTranslationResponse response = new DocumentTranslationResponse();

        response.setId(translation.getId());
        response.setDocumentId(translation.getDocument().getId());
        response.setDocumentTitle(translation.getDocument().getTitle());
        response.setSourceLanguage(translation.getSourceLanguage());
        response.setTargetLanguage(translation.getTargetLanguage());
        response.setTranslatedText(translation.getTranslatedText());
        response.setTranslationModel(translation.getTranslationModel());
        response.setTranslatedAt(translation.getTranslatedAt());

        return response;
    }
}