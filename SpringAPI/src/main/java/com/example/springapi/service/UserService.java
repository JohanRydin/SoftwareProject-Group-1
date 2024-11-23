package com.example.springapi.service;

import com.example.springapi.api.model.User;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;

@Service
public class UserService {

    // Simulates database connection
    private final List<User> userList;

    public UserService() {
        userList = new ArrayList<>();
        User user1 = new User(1, "Johan");
        User user2 = new User(2, "Jane");
        userList.addAll(Arrays.asList(user1, user2));
    }

    public Optional<User> getUser(Integer id) {
        Optional<User> optional = Optional.empty();
        for (User user : userList) {
            if (id.equals(user.getId())) {
                optional = Optional.of(user);
                return optional;
            }
        }
        return optional;
    }
}
