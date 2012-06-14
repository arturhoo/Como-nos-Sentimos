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
    String weather;

    Location() {
    }

    /**
    * Returns a human-readable string compromising the city, state and weather,
    * if the former and latter are present.
    */
    String formatLocation() {
        String locationString = "";
        if(city != null)
            locationString = city + ", ";
        locationString += stateAbbreviation.get(state).toUpperCase();
        if(weather != null && city != null) {
            locationString += ", quando estava ";
            locationString += weatherTranslations.get(weather);
        }
        return locationString;
    }
}

class Tweet {
    Author author;
    Location location;
    long id;
    String text;
    String created_at;
    String created_at_bsb;
    String created_at_local;
    String[] feelings;
    int[] frgb;

    Tweet() {
        this.location = null;
    }

    /**
    * Passes the relevant information to the html page. This information will be
    * by the javascript function to draw this information in the appropriate
    * area of the page.
    */
    void showTweet() {
        String locationString = "algum lugar";
        if(location != null)
            locationString = location.formatLocation();
        setTweetMeta(id, text, author.name, author.screen_name, locationString, created_at_bsb);
    }
}
