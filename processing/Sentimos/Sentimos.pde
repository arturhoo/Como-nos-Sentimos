static final int MAX_NUM_PARTICLES = 1000;
static int NUM_PARTICLES = 0;
static final float PARTICLE_RADIUS = 10.0;
static final int HISTOGRAM_FONT_SIZE = 13;
Particle[] particles = new Particle[MAX_NUM_PARTICLES];
ArrayList<Feeling> feelingList;
HashMap feelingOccurrence;
HashMap feelingRGB;
ArrayList<Weather> weatherList;
HashMap weatherOccurrence;
HashMap weatherTranslations;
ArrayList<State> stateList;
HashMap stateOccurrence;
HashMap stateAbbreviation;

PFont font;
boolean aFocusedTweet;
Particle pFocusedTweet;
boolean written = false;

void setup() {
    size(800, 460);
    smooth();
    feelingList = new ArrayList<Feeling>();
    feelingOccurrence = new HashMap();
    feelingRGB = new HashMap();

    weatherList = new ArrayList<Weather>();
    weatherOccurrence = new HashMap();
    weatherTranslations = new HashMap();

    stateList = new ArrayList<State>();
    stateOccurrence = new HashMap();
    stateAbbreviation = new HashMap();

    font = loadFont("Helvetica", 24);
    frameRate(30);
}

void draw() {
    background(40, 40, 40);
    textFont(font,12);

    aFocusedTweet = false;
    pFocusedTweet = null;
    // for (int i=NUM_PARTICLES-1; i >= 0; i--) {
    //     particles[i].run();
    // }
    Iterator<Feeling> itr = feelingList.iterator();
    while (itr.hasNext()) {
        Feeling tempFeeling = itr.next();
        if(tempFeeling.occurrence > 0) {
            tempFeeling.drawText();
        }
    }
    fill(255);
    textAlign(LEFT);
    text(frameRate,20,20);
}

void mouseClicked() {
    for (int i=NUM_PARTICLES-1; i >= 0; i--) {
        if(particles[i].isIn(mouseX, mouseY)) {
            particles[i].tweet.showTweet();
        }
    }
    sortListThatHasTextAndOccurrenceFields(feelingList, feelingOccurrence);
    setListElementsLocation(feelingList);
    // for (int i=0; i<feelingList.size(); i++)
    //     println(feelingList.get(i).text + ": " + feelingList.get(i).occurrence);
    // sortListThatHasTextAndOccurrenceFields(stateList, stateOccurrence);
    // for (int i=0; i<stateList.size(); i++)
    //     println(stateList.get(i).abbreviation + ": " + stateList.get(i).occurrence);
}
