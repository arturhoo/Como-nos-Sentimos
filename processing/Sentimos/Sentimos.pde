// ArrayList<Particle> particlesList;
static final int MAX_NUM_PARTICLES = 1000;
static int NUM_PARTICLES = 0;
Particle[] particles = new Particle[MAX_NUM_PARTICLES];
ArrayList<Feeling> feelings;
HashMap feelingsOccurrence;
HashMap feelignsRGB;
Tweet tweet = null;
PFont font;
boolean written = false;

void setup() {
    size(640, 360);
    smooth();
    // particlesList = new ArrayList<Particle>();
    feelings = new ArrayList<Feeling>();
    feelingsOccurrence = new HashMap();
    feelingsRGB = new HashMap();
    font = createFont("Arial Bold",48);
    frameRate(30);
    // for(int i=0; i<100; i++) {
    //     Particle p = new Particle(new PVector(width/2, height/2, 0));
    //     particles.add(p);
    // }
}

void draw() {
    background(40, 40, 40);
    textFont(font,12);
    for (int i=NUM_PARTICLES-1; i >= 0; i--) {
        particles[i].run();
    }
    fill(255);
    textAlign(LEFT);
    text(frameRate,20,20);
    if(written == false && NUM_PARTICLES >= 20) {
        for(int i=0; i<NUM_PARTICLES; i++) {
            String text = particles[i].tweet.text;
            String frgb =  (String) particles[i].tweet.frgb;
            setFromProcessing(text + ": " + frgb);
        }
            
        written = true;

        for(int i=0; i<feelings.size(); i++) {
            int occurrence = feelingsOccurrence.get(feelings.get(i).text);
            String text = feelings.get(i).text;
            if(occurrence > 0) {
                setFeelings(text + ": " + occurrence);
            }
        }
    }
}


