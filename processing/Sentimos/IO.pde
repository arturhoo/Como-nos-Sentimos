void addFeeling(Feeling pFeeling) {
    feelingOccurrence.put(pFeeling.text, 0);
    feelingRGB.put(pFeeling.text, pFeeling.frgb);
    feelingList.add(pFeeling);
}

void addWeather(Weather pWeather) {
    weatherOccurrence.put(pWeather.condition, 0);
    weatherTranslations.put(pWeather.condition, pWeather.translation);
    weatherList.add(pWeather);
}

void addState(State pState) {
    stateOccurrence.put(pState.abbreviation, 0);
    stateAbbreviation.put(pState.text, pState.abbreviation);
    stateList.add(pState);
}

void addTweet(Tweet tweet) {
    String sFeeling = tweet.feelings[0];

    // Setting the RGB of the tweet based on its feeling
    tweet.frgb = feelingRGB.get(sFeeling);

    // Updating the occurrence of the feeling
    int occurrence = (Integer) feelingOccurrence.get(sFeeling);
    feelingOccurrence.put(sFeeling, occurrence+1);

    if(tweet.location != null) {
        // Updating the occurrence of the weather, if present
        if(tweet.location.weather != null) {
            String sCondition = tweet.location.weather;
            int occurrence = (Integer) weatherOccurrence.get(sCondition);
            weatherOccurrence.put(sCondition, occurrence+1);
        }
        // Updating the occurrence of the state
        String abbreviation = stateAbbreviation.get(tweet.location.state);
        int occurrence = (Integer) stateOccurrence.get(abbreviation);
        stateOccurrence.put(abbreviation, occurrence+1);

    }

    // Creating a particle for the tweet and adding to the array
    Particle particle = new Particle(new PVector(int(width/2), int(height/2), 0));
    particle.tweet = tweet;
    particles[NUM_PARTICLES] = particle;
    NUM_PARTICLES++;
}

interface JavaScriptInterface {
    void setTweetsText(String text);
    void setFeeling(String text);
    void setTweetText(String text);
    void setTweetMeta(long id, String text, String name, String screen_name, String location, String created_at_bsb);
}

JavaScriptInterface js;

void setInterfaceLink (JavaScriptInterface jsin) {
    js = jsin;
}