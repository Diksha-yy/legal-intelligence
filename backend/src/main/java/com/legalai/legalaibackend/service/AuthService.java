package com.legalai.legalaibackend.service;

import com.legalai.legalaibackend.dto.LoginRequest;
import com.legalai.legalaibackend.dto.LoginResponse;

public interface AuthService {

    LoginResponse login(LoginRequest request);

}