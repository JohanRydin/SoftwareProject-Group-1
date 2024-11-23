package com.example.springapi.api.controller;

import com.example.springapi.api.model.User;
import com.example.springapi.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.Optional;

@RestController
public class UserController {

    private final UserService userService;

    @Autowired
    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping("/user")
    public ResponseEntity<User> getUser(@RequestParam Integer id) {
        Optional<User> user = userService.getUser(id);
        if (user.isPresent()) {
            return ResponseEntity.ok(user.get());
        }
        return ResponseEntity.notFound().build();
    }
    
    @PostMapping("/user")
    public ResponseEntity<User> postUser(@RequestParam String username) {
        Optional<User> newUser = userService.newUser(username);
        if (newUser.isPresent()) {
            return ResponseEntity.ok(newUser.get());
        }
        return ResponseEntity.badRequest().build(); // Bad request response if we already has such a user. 
    }
}