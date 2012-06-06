ArrayList<Particle> particles;
Tweet tweet = null;
PFont font;

void setup() {
    size(640, 360);
    smooth();
    particles = new ArrayList<Particle>();
    font = createFont("Arial Bold",48);
    for(int i=0; i<100; i++) {
        Particle p = new Particle(new PVector(width/2, height/2, 0));
        particles.add(p);
    }
}

void draw() {
    background(0);
    textFont(font,12);
    // Cycle through all particle systems, run them and delete old ones
    // for (int i=particles.size()-1; i >= 0; i--) {
        // particles.get(i).run();
    // }
    fill(255);
    textAlign(LEFT);
    text(frameRate,20,20);
    if(tweet != null) {
        text(tweet.text, 50, 100);
    }
}

void setTweet(String text) {
    tweet = new Tweet(text=text);
}