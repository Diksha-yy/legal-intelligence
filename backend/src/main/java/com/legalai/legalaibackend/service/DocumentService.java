package com.legalai.legalaibackend.service;

import com.legalai.legalaibackend.dto.DocumentRequest;
import com.legalai.legalaibackend.dto.DocumentResponse;
import com.legalai.legalaibackend.entity.Document;
import com.legalai.legalaibackend.entity.User;
import com.legalai.legalaibackend.enums.DocumentStatus;
import com.legalai.legalaibackend.exception.ResourceNotFoundException;
import com.legalai.legalaibackend.repository.DocumentRepository;
import com.legalai.legalaibackend.repository.UserRepository;
import com.legalai.legalaibackend.service.storage.FileStorageService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class DocumentService {

    @Autowired
    private DocumentRepository documentRepository;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private FileStorageService fileStorageService;

    // =========================
    // Save Document (JSON API)
    // =========================
    public DocumentResponse saveDocument(DocumentRequest request) {

        if (request == null) {
            throw new IllegalArgumentException("Request body cannot be null.");
        }

        if (request.getUserId() == null) {
            throw new IllegalArgumentException("User Id is required.");
        }

        if (request.getTitle() == null || request.getTitle().trim().isEmpty()) {
            throw new IllegalArgumentException("Document title is required.");
        }

        User user = userRepository.findById(request.getUserId())
                .orElseThrow(() ->
                        new ResourceNotFoundException(
                                "User not found with id : " + request.getUserId()));

        Document document = new Document();

        document.setTitle(request.getTitle().trim());
        document.setFileName(request.getFileName());
        document.setFileType(request.getFileType());
        document.setFilePath(request.getFilePath());
        document.setUploadedAt(LocalDateTime.now());
        document.setStatus(DocumentStatus.UPLOADED);
        document.setUploadedBy(user);

        Document saved = documentRepository.save(document);

        return mapToResponse(saved);
    }

    // =========================
    // Upload File
    // =========================
    public DocumentResponse uploadDocument(
            MultipartFile file,
            String title,
            Long userId
    ) {

        if (file == null || file.isEmpty()) {
            throw new IllegalArgumentException("Please upload a file.");
        }

        if (title == null || title.trim().isEmpty()) {
            throw new IllegalArgumentException("Document title is required.");
        }

        User user = userRepository.findById(userId)
                .orElseThrow(() ->
                        new ResourceNotFoundException(
                                "User not found with id : " + userId));

        String filePath = fileStorageService.saveFile(file);

        Document document = new Document();

        document.setTitle(title.trim());
        document.setFileName(file.getOriginalFilename());
        document.setFileType(file.getContentType());
        document.setFilePath(filePath);
        document.setUploadedAt(LocalDateTime.now());
        document.setStatus(DocumentStatus.UPLOADED);
        document.setUploadedBy(user);

        Document saved = documentRepository.save(document);

        return mapToResponse(saved);
    }

    // =========================
    // Get All Documents
    // =========================
    public List<DocumentResponse> getAllDocuments() {

        return documentRepository.findAll()
                .stream()
                .map(this::mapToResponse)
                .collect(Collectors.toList());
    }

    // =========================
    // Get By Id
    // =========================
    public DocumentResponse getDocumentById(Long id) {

        Document document = documentRepository.findById(id)
                .orElseThrow(() ->
                        new ResourceNotFoundException(
                                "Document not found with id : " + id));

        return mapToResponse(document);
    }

    // =========================
    // Delete
    // =========================
    public void deleteDocument(Long id) {

        Document document = documentRepository.findById(id)
                .orElseThrow(() ->
                        new ResourceNotFoundException(
                                "Document not found with id : " + id));

        documentRepository.delete(document);
    }

    // =========================
    // Entity → DTO
    // =========================
    private DocumentResponse mapToResponse(Document document) {

        DocumentResponse response = new DocumentResponse();

        response.setId(document.getId());
        response.setTitle(document.getTitle());
        response.setFileName(document.getFileName());
        response.setFileType(document.getFileType());
        response.setFilePath(document.getFilePath());
        response.setUploadedAt(document.getUploadedAt());

        if (document.getUploadedBy() != null) {
            response.setUploadedBy(document.getUploadedBy().getName());
        }

        if (document.getStatus() != null) {
            response.setStatus(document.getStatus().name());
        }

        return response;
    }
}