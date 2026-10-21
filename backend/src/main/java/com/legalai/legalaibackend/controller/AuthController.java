package com.legalai.legalaibackend.controller;

import com.legalai.legalaibackend.dto.LoginRequest;
import com.legalai.legalaibackend.dto.LoginResponse;
import com.legalai.legalaibackend.service.AuthService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    @Autowired
    private AuthService authService;

    @PostMapping("/login")
    public LoginResponse login(@Valid @RequestBody LoginRequest request) {
        return authService.login(request);
    }
}