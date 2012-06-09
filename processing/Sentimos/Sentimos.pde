static final int MAX_NUM_PARTICLES = 1000;
static int NUM_PARTICLES = 0;
Particle[] particles = new Particle[MAX_NUM_PARTICLES];
ArrayList<Feeling> feelings;
HashMap feelingsOccurrence;
HashMap feelignsRGB;

PFont font;
boolean aFocusedTweet;
boolean written = false;

void setup() {
    size(800, 460);
    smooth();
    feelings = new ArrayList<Feeling>();
    feelingsOccurrence = new HashMap();
    feelingsRGB = new HashMap();
    font = createFont("Helvetica-Bold", 24);
    frameRate(30);
}

void draw() {
    background(#1A1711);
    textFont(font,12);

    aFocusedTweet = false;
    for (int i=NUM_PARTICLES-1; i >= 0; i--) {
        particles[i].run();
    }
    fill(255);
    textAlign(LEFT);
    text(frameRate,20,20);
}

void mouseClicked() {
    for (int i=NUM_PARTICLES-1; i >= 0; i--) {
        if(particles[i].isIn(mouseX, mouseY)) {
            long id = particles[i].tweet.id;
            String text = particles[i].tweet.text;
            String screen_name = particles[i].tweet.author.screen_name;
            String name = particles[i].tweet.author.name;
            String location = "algum lugar";
            if(particles[i].tweet.location != null) {
                location = "";
                if(particles[i].tweet.location.city != null)
                    location = particles[i].tweet.location.city + ", ";
                location += particles[i].tweet.location.state;
            }
            String created_at = particles[i].tweet.created_at;
            // console.log(created_at_local);
            // setTweetText(text);
            setTweetMeta(id, text, name, screen_name, location, created_at);
        }
    }
}


