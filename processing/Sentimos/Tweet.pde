class Author {
    String location;
    String screen_name;
    String name;

    Author() {
    }
}

class Location {
    String city;
    String state;

    Location() {
    }
}

class Tweet {
    Author author;
    Location location;
    long id;
    String text;
    String created_at;
    String created_at_local;
    String[] feelings;
    int[] frgb;

    Tweet() {
        this.location = null;
    }
}