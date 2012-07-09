/* @pjs font="static/fonts/MavenPro-Bold.ttf"; */
/* @pjs preload="static/images/question4.png,static/images/brasil_color.png,static/images/brasil_gray.png" */

static int WIDTH  = 800;
static int HEIGHT = 460;

static final int MAX_NUM_PARTICLES = 1000;
static int NUM_PARTICLES = 0;
static final float PARTICLE_RADIUS = 10.0;
static final int HISTOGRAM_FONT_SIZE = 13;
static final int FILL_TRANSPARENCY = 215;

static float LEFT_BORDER_OFFSET           = WIDTH*0.05;
static float RIGHT_BORDER_OFFSET          = WIDTH*0.05;
static float TOP_BORDER_OFFSET            = HEIGHT*0.10;
static float BOTTOM_BORDER_OFFSET         = HEIGHT*0.10;
static float DIST_BTWN_TEXT_AND_PARTICLES = WIDTH*0.05;
static float DIST_BTWN_PARTICLES          = PARTICLE_RADIUS*0.80;
static float DIST_BTWN_HISTOGRAM_ENTRIES  = PARTICLE_RADIUS*1.00;
static float TEXT_WIDTH                   = WIDTH*0.10;
static float PARTICLES_WIDTH              = WIDTH -
                                            TEXT_WIDTH -
                                            LEFT_BORDER_OFFSET -
                                            RIGHT_BORDER_OFFSET -
                                            DIST_BTWN_TEXT_AND_PARTICLES;

static final String LOADING_TEXT   = "CARREGANDO";
static final String EXTRA_FEELIGNS = "E outros mais abaixo!";

static final int MADNESS = 1;
static final int FEELINGS = 2;
static final int STATES = 3;
static final int MAP = 4;
static final int WEATHER = 5;
static int VIEW = MADNESS;

static boolean MOUSE_OUT = false;

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

PImage questionMarkImage;
ArrayList questionMarkPixels;
Pimage countryGrayMapImage;
PImage countryMapImage;
ArrayList countryMapPixels;

PFont font;
Particle pFocusedTweet;
boolean written = false;

void setup() {
    size(WIDTH, HEIGHT);
    smooth();
    feelingList         = new ArrayList<Feeling>();
    feelingOccurrence   = new HashMap();
    feelingRGB          = new HashMap();

    weatherList         = new ArrayList<Weather>();
    weatherOccurrence   = new HashMap();
    weatherTranslations = new HashMap();

    stateList           = new ArrayList<State>();
    stateOccurrence     = new HashMap();
    stateAbbreviation   = new HashMap();

    questionMarkImage   = loadImage("static/images/question4.png");
    countryMapImage     = loadImage("static/images/brasil_color.png");
    countryGrayMapImage = loadImage("static/images/brasil_gray.png");
    font2               = createFont("static/fonts/MavenPro-Bold.ttf", 24);
    font                = loadFont("Helvetica", 24);
    frameRate(30);
    textMode(SCREEN);
}

void draw() {
    background(40, 40, 40);

    pFocusedTweet = null;

    if(NUM_PARTICLES == 0) {
        textFont(font, 12);
        fill(255);
        textAlign(CENTER);
        text(LOADING_TEXT, width/2, height/2);
    }

    // Draw feelings text
    if(VIEW == FEELINGS) {
        Iterator<Feeling> itr = feelingList.iterator();
        boolean paginated_drawn = false;
        while(itr.hasNext()) {
            Feeling tempFeeling = itr.next();
            if(tempFeeling.occurrence > 0) {
                tempFeeling.drawText();
            }
            if(tempFeeling.paginated && !paginated_drawn) {
                textAlign(RIGHT);
                text(EXTRA_FEELIGNS, tempFeeling.loc.x, tempFeeling.loc.y);
                paginated_drawn = true;
                textAlign(LEFT);
            }
        }
    }

    // Draw states text
    if(VIEW == STATES) {
        Iterator<State> itr = stateList.iterator();
        while(itr.hasNext()) {
            State tempState = itr.next();
            if(tempState.occurrence > 0) {
                tempState.drawText();
            }
        }
    }

    // Draw map
    if(VIEW == MAP) {
        imgWidth = countryGrayMapImage.width;
        imgHeight = countryGrayMapImage.height;
        image(countryGrayMapImage, (width - imgWidth)/2, (height-imgHeight)/2);
    }

    // Draw states text
    if(VIEW == 5) {
        Iterator<Weather> itr = weatherList.iterator();
        while(itr.hasNext()) {
            Weather tempWeather = itr.next();
            if(tempWeather.occurrence > 0) {
                tempWeather.drawText();
            }
        }
    }

    for(int i=NUM_PARTICLES-1; i >= 0; i--) {
        particles[i].run();
    }
    if(pFocusedTweet != null) pFocusedTweet.render();


    // Draw Frame Rate
    textFont(font, 12);
    fill(255);
    textAlign(LEFT);
    text(frameRate, 20, 20);
}

void mouseClicked() {
    if(pFocusedTweet != null) {
        pFocusedTweet.tweet.showTweet();
        for(int i=NUM_PARTICLES-1; i >= 0; i--) {
            if(particles[i] != pFocusedTweet) {
                float distance = sqrt(pow(particles[i].loc.x - mouseX, 2) + pow(particles[i].loc.y - mouseY, 2)) * (float) 2.0;
                float ang = atan2(particles[i].loc.x - mouseX, particles[i].loc.y - mouseY);
                f = min(1 / distance, 3) * 250;
                particles[i].vel.x += sin(ang) * f;
                particles[i].vel.y += cos(ang) * f;
            }
        }
    }
}

void mouseOut() {
    MOUSE_OUT = true;
}

void mouseOver() {
    MOUSE_OUT = false;
}
