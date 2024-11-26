package com.example.springapi.api.model;

import java.util.List;

public class User {
    private int id;
    private String username;
    private List<Genre> genrePref;  //NOTE: Genre is enum right now. Should base on database storage of allowed genres. 
    private List<String> gamePref;  // These should also be classes 
    private List<Integer> wishlist; //TODO: Integer as type, should define class? 

    
    public User(int id, String username, List<Genre> genrePref, List<String> gamePref, List<Integer> wishlist) {
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

    public List<Genre> getGenrePref() {
        return this.genrePref;
    }

    public void updateGenrePref(List<Genre> genrePref) {
        this.genrePref.addAll(genrePref);
    }

    public List<String> getGamePref() {
        return this.gamePref;
    }

    public void updateGamePref(List<String> gamePref) {
        this.gamePref.addAll(gamePref);
    }

    public List<Integer> getWishlist() {
        return this.wishlist;
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
