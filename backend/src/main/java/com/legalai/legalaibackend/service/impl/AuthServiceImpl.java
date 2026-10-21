package com.legalai.legalaibackend.service.impl;

import com.legalai.legalaibackend.dto.LoginRequest;
import com.legalai.legalaibackend.dto.LoginResponse;
import com.legalai.legalaibackend.entity.User;
import com.legalai.legalaibackend.repository.UserRepository;
import com.legalai.legalaibackend.security.JwtService;
import com.legalai.legalaibackend.service.AuthService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class AuthServiceImpl implements AuthService {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    @Autowired
    private JwtService jwtService;

    @Override
    public LoginResponse login(LoginRequest request) {

        // Find user by email
        User user = userRepository.findByEmail(request.getEmail())
                .orElseThrow(() -> new RuntimeException("Invalid email or password"));

        // Verify password
        if (!passwordEncoder.matches(request.getPassword(), user.getPassword())) {
            throw new RuntimeException("Invalid email or password");
        }

        // Generate JWT Token with Email and Role
        String token = jwtService.generateToken(
                user.getEmail(),
                user.getRole().name()
        );

        // Return Login Response
        return new LoginResponse(
                "Login Successful",
                token
        );
    }
}