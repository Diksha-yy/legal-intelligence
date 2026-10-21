package com.legalai.legalaibackend.config;

import org.springframework.context.annotation.Configuration;

import jakarta.annotation.PostConstruct;
import java.io.File;

@Configuration
public class FileStorageConfig {

    private static final String UPLOAD_DIR = "uploads";

    @PostConstruct
    public void init() {

        File folder = new File(UPLOAD_DIR);

        if (!folder.exists()) {
            folder.mkdirs();
        }
    }
}