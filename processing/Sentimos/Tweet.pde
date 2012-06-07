class Author {
    String location;
    String screen_name;
    String name;
}

class Location {
    String city;
    String state;
}

class Tweet {
    Author author;
    Location location;
    String text;
    String created_at;
    String created_at_local;
    String[] feelings;
    int[] frgb;

    Tweet() {
    }
}