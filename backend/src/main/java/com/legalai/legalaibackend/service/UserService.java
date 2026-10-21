package com.legalai.legalaibackend.service;

import com.legalai.legalaibackend.dto.UserRegisterRequest;
import com.legalai.legalaibackend.dto.UserResponse;

import java.util.List;

public interface UserService {

    UserResponse createUser(UserRegisterRequest request);

    List<UserResponse> getAllUsers();

    UserResponse getUserById(Long id);

    UserResponse updateUser(Long id, UserRegisterRequest request);

    void deleteUser(Long id);
}