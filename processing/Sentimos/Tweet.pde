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

    Tweet() {
    }

    Tweet(String text) {
        this.text = text;
    }

    Tweet(Author author, Location location, String text, String created_at,
          String created_at_local, String[] feelings) {
        this.author           = author;
        this.location         = location;
        this.text             = text;
        this.created_at       = created_at;
        this.created_at_local = created_at_local;
        this.feelings         = feelings;
    }
}