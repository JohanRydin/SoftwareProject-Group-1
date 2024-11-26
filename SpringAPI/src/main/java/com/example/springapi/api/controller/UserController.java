package com.example.springapi.api.controller;

import com.example.springapi.api.model.User;
import com.example.springapi.service.UserService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
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
    public ResponseEntity<Integer> getUser(@RequestParam String username) {
        Optional<User> user = userService.getUser(username);
        if (user.isPresent()) {
            return ResponseEntity.ok(user.get().getId());
        }
        return ResponseEntity.notFound().build();
    }
    
    @PostMapping("/user")
    public ResponseEntity<Integer> postUser(@RequestParam String username) {
        Optional<User> newUser = userService.newUser(username);
        if (newUser.isEmpty()) { 
            return ResponseEntity.badRequest().body(null); // Bad request  if username already exists
        }
        return ResponseEntity.ok(newUser.get().getId());
    }
    

    @DeleteMapping("/user")
    public ResponseEntity<?> deleteUser(@RequestParam String username) {
        return (ResponseEntity<?>) ResponseEntity.noContent(); //TODO: Fix when/if we allow deleting user 
    }



    @GetMapping("user/genrepref")
    public ResponseEntity<?> getUserGenrePref(@RequestParam String username) {
        return (ResponseEntity<?>) ResponseEntity.noContent();
    }
    @PostMapping("user/genrepref")
    public ResponseEntity<?> postUserGenrePref(@RequestParam String username) {
        return (ResponseEntity<?>) ResponseEntity.noContent();
    }
    @DeleteMapping("user/genrepref")
    public ResponseEntity<?> deleteUserGenrePref(@RequestParam String username) {
        return (ResponseEntity<?>) ResponseEntity.noContent();
    }


    @GetMapping("user/gamepref")
    public ResponseEntity<?> getUserGamePref(@RequestParam String username) {
        return (ResponseEntity<?>) ResponseEntity.noContent();
    }

    @PostMapping("user/gamepref")
    public ResponseEntity<?> postUserGamePref(@RequestParam String username) {
        return (ResponseEntity<?>) ResponseEntity.noContent();
    }

    @DeleteMapping("user/gamepref")
    public ResponseEntity<?> deleteUserGamePref(@RequestParam String username) {
        return (ResponseEntity<?>) ResponseEntity.noContent();
    }

    
    @GetMapping("user/wishlist")
    public ResponseEntity<?> getUserWishlist(@RequestParam String username) {
        return (ResponseEntity<?>) ResponseEntity.noContent();
    }
    @PostMapping("user/wishlist")
    public ResponseEntity<?> postUserWishlist(@RequestParam String username) {
        return (ResponseEntity<?>) ResponseEntity.noContent();
    }

    @DeleteMapping("user/wishlist")
    public ResponseEntity<?> deleteUserWishlist(@RequestParam String username) {
        return (ResponseEntity<?>) ResponseEntity.noContent();
    }


}
