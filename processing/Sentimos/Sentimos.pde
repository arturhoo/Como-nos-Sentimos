static int WIDTH  = 800;
static int HEIGHT = 460;

static final int MAX_NUM_PARTICLES = 1000;
static int NUM_PARTICLES = 0;
static final float PARTICLE_RADIUS = 10.0;
static final int HISTOGRAM_FONT_SIZE = 13;

static float LEFT_BORDER_OFFSET           = WIDTH*0.05;
static float RIGHT_BORDER_OFFSET          = WIDTH*0.05;
static float TOP_BORDER_OFFSET            = HEIGHT*0.10;
static float BOTTOM_BORDER_OFFSET         = HEIGHT*0.10;
static float DIST_BTWN_TEXT_AND_PARTICLES = WIDTH*0.05;
static float DIST_BTWN_PARTICLES          = PARTICLE_RADIUS*0.80;
static float DIST_BTWN_HISTOGRAM_ENTRIES  = PARTICLE_RADIUS*1.00;
static float TEXT_WIDTH                   = WIDTH*0.10;
static float PARTICLES_WIDTH              = WIDTH - LEFT_BORDER_OFFSET - RIGHT_BORDER_OFFSET - DIST_BTWN_TEXT_AND_PARTICLES;

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
    size(WIDTH, HEIGHT);
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

    aFocusedTweet = false;
    pFocusedTweet = null;
    for (int i=NUM_PARTICLES-1; i >= 0; i--) {
        if(particles[i].feelingLoc != null) particles[i].render();
        // particles[i].run();
    }
    Iterator<Feeling> itr = feelingList.iterator();
    while (itr.hasNext()) {
        Feeling tempFeeling = itr.next();
        if(tempFeeling.occurrence > 0) {
            tempFeeling.drawText();
        }
    }

    textFont(font,12);
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
    for (int i=NUM_PARTICLES-1; i >= 0; i--) {
        if(particles[i].feelingLoc == null) particles[i].setFeelingLoc();
    }
    // for (int i=0; i<feelingList.size(); i++)
    //     println(feelingList.get(i).text + ": " + feelingList.get(i).occurrence);
    // sortListThatHasTextAndOccurrenceFields(stateList, stateOccurrence);
    // for (int i=0; i<stateList.size(); i++)
    //     println(stateList.get(i).abbreviation + ": " + stateList.get(i).occurrence);
}
