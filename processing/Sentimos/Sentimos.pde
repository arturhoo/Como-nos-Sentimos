// ArrayList<Particle> particlesList;
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
    // particlesList = new ArrayList<Particle>();
    feelings = new ArrayList<Feeling>();
    feelingsOccurrence = new HashMap();
    feelingsRGB = new HashMap();
    font = createFont("Helvetica-Bold", 24);
    frameRate(30);
    // for(int i=0; i<100; i++) {
    //     Particle p = new Particle(new PVector(width/2, height/2, 0));
    //     particles.add(p);
    // }
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
    // if(written == false && NUM_PARTICLES >= 20) {
    //     for(int i=0; i<NUM_PARTICLES; i++) {
    //         String text = particles[i].tweet.text;
    //         String frgb =  (String) particles[i].tweet.frgb;
    //         setTweetsText(text + ": " + frgb);
    //     }
            
    //     written = true;

    //     for(int i=0; i<feelings.size(); i++) {
    //         int occurrence = feelingsOccurrence.get(feelings.get(i).text);
    //         String text = feelings.get(i).text;
    //         if(occurrence > 0) {
    //             setFeelings(text + ": " + occurrence);
    //         }
    //     }
    // }
}

void mouseClicked() {
    for (int i=NUM_PARTICLES-1; i >= 0; i--) {
        if(particles[i].isIn(mouseX, mouseY)) {
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
            setTweetMeta(text, name, screen_name, location, created_at);
        }
    }
}


