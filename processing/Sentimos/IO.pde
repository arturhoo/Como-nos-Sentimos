void addFeeling(Feeling pFeeling) {
    feelingsOccurrence.put(pFeeling.text, 0);
    feelingsRGB.put(pFeeling.text, pFeeling.frgb);
    feelings.add(pFeeling);
}

void addTweet(Tweet tweet) {
    String sFeeling = tweet.feelings[0];

    // Setting the RGB of the tweet based on its feeling
    tweet.frgb = feelingsRGB.get(sFeeling);

    // Updating the occurrence of the feeling
    int occurrence = (Integer) feelingsOccurrence.get(sFeeling);
    feelingsOccurrence.put(sFeeling, occurrence+1);

    // Creating a particle for the tweet and adding to the array
    Particle particle = new Particle(new PVector(int(width/2), int(height/2), 0));
    particle.tweet = tweet;
    particles.add(particle);
}

interface JavaScriptInterface {
    void setFromProcessing(String text);
    void setFeeling(String text);
}

JavaScriptInterface js;

void setInterfaceLink (JavaScriptInterface jsin) {
    js = jsin;
}