package com.example.springapi.service;

import com.example.springapi.api.model.Genre;
import com.example.springapi.api.model.User;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;



@Service
public class UserService {

    private final List<User> userList;

    public UserService() {
        userList = new ArrayList<>();
        userList.add(new User(1, "Johan", List.of(Genre.ACTION), List.of("Dishonored", "Batman"), List.of(2, 3)));
        userList.add(new User(2, "Lawend", List.of(Genre.HORROR, Genre.DRAMA), List.of("Portal"), List.of(4, 5)));
    }

    public Optional<User> getUser(String username) {
        return userList.stream()
                .filter(user -> user.getUsername().equalsIgnoreCase(username))
                .findFirst();
    }

    public Optional<User> newUser(String username) {
        if (userList.stream().anyMatch(user -> user.getUsername().equalsIgnoreCase(username))) {
            return Optional.empty(); 
        }
        // Generate a new unique id for now, but we will have to connect to database!
        int newId = userList.size() + 1;
        User newUser = new User(newId, username, List.of(), List.of(), List.of());
        userList.add(newUser);
        return Optional.of(newUser);
    }
}
