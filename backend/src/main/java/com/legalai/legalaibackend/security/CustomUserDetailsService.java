package com.legalai.legalaibackend.security;

import com.legalai.legalaibackend.entity.User;
import com.legalai.legalaibackend.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class CustomUserDetailsService implements UserDetailsService {

    @Autowired
    private UserRepository userRepository;

    @Override
    public UserDetails loadUserByUsername(String email) {

        // Debug Log
        System.out.println("==================================");
        System.out.println("Loading user: " + email);

        User user = userRepository.findByEmail(email)
                .orElseThrow(() -> {
                    System.out.println("User not found!");
                    return new RuntimeException("User not found");
                });

        System.out.println("User found: " + user.getName());
        System.out.println("Email: " + user.getEmail());
        System.out.println("Role found: " + user.getRole());
        System.out.println("Password (Encrypted): " + user.getPassword());
        System.out.println("Creating Spring Security UserDetails...");
        System.out.println("==================================");

        return new org.springframework.security.core.userdetails.User(
                user.getEmail(),
                user.getPassword(),
                List.of(
                        new SimpleGrantedAuthority(
                                "ROLE_" + user.getRole().name()
                        )
                )
        );
    }
}