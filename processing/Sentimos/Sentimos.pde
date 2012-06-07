ArrayList<Particle> particles;
ArrayList<Feeling> feelings;
HashMap feelingsOccurrence;
HashMap feelignsRGB;
Tweet tweet = null;
PFont font;
boolean written = false;

void setup() {
    size(640, 360);
    smooth();
    particles = new ArrayList<Particle>();
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
    background(30, 30, 30);
    textFont(font,12);
    for (int i=particles.size()-1; i >= 0; i--) {
        particles.get(i).run();
    }
    fill(255);
    textAlign(LEFT);
    text(frameRate,20,20);
    if(written == false && particles.size() >= 10) {
        for(int i=0; i<particles.size(); i++) {
            String text = particles.get(i).tweet.text;
            String frgb =  (String) particles.get(i).tweet.frgb;
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


