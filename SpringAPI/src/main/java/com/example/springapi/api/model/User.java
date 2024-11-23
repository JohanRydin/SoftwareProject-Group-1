package com.example.springapi.api.model;

import java.util.List;

public class User {
    private int id;
    private String username;
    private List<String> genrePref;  
    private List<String> gamePref;  // These should also be classes 
    private List<Integer> wishlist; //TODO: Integer as type, should define class? 

    
    public User(int id, String username, List<String> genrePref, List<String> gamePref, List<Integer> wishlist) {
        this.id = id;
        this.username = username;
        this.genrePref = genrePref;
        this.gamePref = gamePref;
        this.wishlist = wishlist;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        //TODO: This needs to be checked in Controller/Service that new username is not taken! 
        this.username = username;
    }

    public List<String> getGenrePref() {
        return genrePref;
    }

    public void updateGenrePref(List<String> genrePref) {
        this.genrePref.addAll(genrePref);
    }

    public List<String> getGamePref() {
        return gamePref;
    }

    public void updateGamePref(List<String> gamePref) {
        this.gamePref.addAll(gamePref);
    }

    public List<Integer> getWishlist() {
        return wishlist;
    }

    public void updateWishlist(List<Integer> wishlist) {
        this.wishlist.addAll(wishlist);
    }

    @Override
    public String toString() {
        return "User{" +
                "id=" + id +
                ", username='" + username + '\'' +
                ", genrePref=" + genrePref +
                ", gamePref=" + gamePref +
                ", wishlist=" + wishlist +
                '}';
    }
}
