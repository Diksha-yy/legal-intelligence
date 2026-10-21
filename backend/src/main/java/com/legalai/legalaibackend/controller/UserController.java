package com.legalai.legalaibackend.controller;

import com.legalai.legalaibackend.dto.UserRegisterRequest;
import com.legalai.legalaibackend.dto.UserResponse;
import com.legalai.legalaibackend.service.UserService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/users")
public class UserController {

    @Autowired
    private UserService userService;

    // Public API - Anyone can register
    @PostMapping("/register")
    public UserResponse createUser(
            @Valid @RequestBody UserRegisterRequest request) {

        return userService.createUser(request);
    }

    // Only ADMIN can see all users
    @PreAuthorize("hasRole('ADMIN')")
    @GetMapping
    public List<UserResponse> getAllUsers() {
        return userService.getAllUsers();
    }

    // ADMIN or CLIENT can access
    @PreAuthorize("hasAnyRole('ADMIN','CLIENT')")
    @GetMapping("/{id}")
    public UserResponse getUserById(@PathVariable Long id) {
        return userService.getUserById(id);
    }

    // Only ADMIN can update users
    @PreAuthorize("hasRole('ADMIN')")
    @PutMapping("/{id}")
    public UserResponse updateUser(
            @PathVariable Long id,
            @Valid @RequestBody UserRegisterRequest request) {

        return userService.updateUser(id, request);
    }

    // Only ADMIN can delete users
    @PreAuthorize("hasRole('ADMIN')")
    @DeleteMapping("/{id}")
    public String deleteUser(@PathVariable Long id) {

        userService.deleteUser(id);
        return "User deleted successfully!";
    }
}