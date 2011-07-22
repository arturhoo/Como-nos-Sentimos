//import de.bezier.data.sql.*;
//MySQL db;
//MySQL db2;
ParticleSystem ps;

int width = 800;
int height = 600;
int pwidth = width;
int filterMenu = 16;
int pheight = height-filterMenu;
int numParticles = 180;
PFont font1;
PImage img;
PImage brasil;
boolean alreadyShowing;

String host;
String database;
String user;
String pass;

int MADNESS = 1;
int FEELINGS = -1;
int STATES = -1;
int STATES2 = -1;
int MENU = -1;

HashMap feelingsHash;
HashMap feelingsOccurrence;
HashMap statesOccurrence;
HashMap feelingsRGB;
ArrayList<Tweet> tweetsList;
ArrayList<Feeling> feelingsList;
ArrayList<State> statesList;
ArrayList<Integer> questionList;

Button anarquia;
Button sentimentos;
Button estados;
Button mapa;
Menu menu;

void setup() {
  //String slines[] = loadStrings("mysql_settings.txt");
  //host = slines[0]; database = slines[1]; user = slines[2]; pass = slines[3];
  
  font1 = loadFont("LucidaGrande-24.vlw");
  size(width, height);
  frameRate (60);

  brasil = loadImage("brasil_gray.png");

  anarquia = new Button("Anarquia", new PVector(width-40, height-70), 12);
  anarquia.ccolor = color(219, 13, 61);
  sentimentos = new Button("Sentimentos", new PVector(width-40, height-50), 12);
  estados = new Button("Estados", new PVector(width-40, height-30), 12);
  mapa = new Button("Mapa", new PVector(width-40, height-10), 12);

  img = loadImage("question4.png");
  img.loadPixels();
  questionList = new ArrayList<Integer>();
  for (int i=0; i<(img.width*img.height); i++) {
    if (img.pixels[i] == color(0, 0, 0)) questionList.add(i);
  }

  ps = new ParticleSystem(0, new PVector(width/2, height/2, 0));
  //readDB(db, db2);
  sortFeelingsList();
  sortStatesList();

  menu = new Menu();

  smooth();
  print("pronto\n");
}

void draw() {  
  //background(75, 70, 56);
  background(30, 30, 30);
  if (pheight != height) {
    noStroke();
    fill(64, 59, 51);
    rectMode(CORNER);
    rect(0, 0, width, height - pheight);
  }

  anarquia.draw(0);
  sentimentos.draw(0);
  estados.draw(0);
  mapa.draw(0);

  if (FEELINGS == 1) {
    // Escape distance
    int y = 100;
    int x = 0;
    for (int i=0; i<feelingsList.size(); i++) {
      if (feelingsList.get(i).occurrence > 0) {
        feelingsList.get(i).escape = 0;
        textFont(font1, 12);
        fill(193, 191, 191);
        text((String) (feelingsList.get(i).feeling+"("+feelingsList.get(i).occurrence+")"), 30+x, y);
        feelingsList.get(i).loc.set((float)30+x, (float)y, 0);
        y += (feelingsList.get(i).occurrence/30*22) + 22;
        // Para dividir colunas
        if (y > height-100) {
          x = width/2;
          y -= 22*7;
        }
      }
    }
  }
  if (STATES == 1 && STATES2 == 1) image(brasil, (width-400)/2, (height-400)/2);
  if (STATES == 1 && STATES2 != 1) {
    int y = 100;
    int x = 0;
    for (int i=0; i<statesList.size(); i++) {
      if (statesList.get(i).occurrence > 0) {
        statesList.get(i).escape = 0;
        textFont(font1, 12);
        fill(193, 191, 191);
        text((String) (statesList.get(i).st.toUpperCase()+"("+statesList.get(i).occurrence+")"), 30+x, y);
        statesList.get(i).loc.set((float)30+x, (float)y, 0);
        y += (statesList.get(i).occurrence/30*22) + 22;
        // Para dividir colunas
        if (y > height-100) {
          x = width/2;
          y -= 22*7;
        }
      }
    }
  }
  ps.run();

  if (MENU == -1) {
    rectMode(CORNER);
    fill(219, 13, 61);
    noStroke();
    rect(0, 0, width, filterMenu);
    textFont(font1, 11);
    fill(0, 0, 0);
    textAlign(CENTER);
    text("Filtrar", width/2, 12);
  } 
  else if (MENU == 1) menu.drawMenu();
}

void mousePressed() {
  if (MENU == -1) {
    for (int i = ps.particles.size()-1; i >= 0; i--) {
      Particle p = (Particle) ps.particles.get(i);
      if (p.onClick()) {
        for (int j = ps.particles.size()-1; j >= 0; j--) {
          Particle p1 = (Particle) ps.particles.get(j);
          p1.tweet.show = false;
        }
        p.tweet.show = true;
      }
    }
  }

  if (anarquia.isIn() || sentimentos.isIn() || estados.isIn() || mapa.isIn()) {
    anarquia.ccolor = color(72, 66, 67);
    sentimentos.ccolor = color(72, 66, 67);
    estados.ccolor = color(72, 66, 67);
    mapa.ccolor = color(72, 66, 67);
    for (int j = ps.particles.size()-1; j >= 0; j--) {
      Particle p1 = (Particle) ps.particles.get(j);
      p1.tweet.show = false;
    }
    pheight = height-filterMenu;
    MADNESS = -1;
    FEELINGS = -1;
    STATES = -1;
    STATES2 = -1;
  }

  if (anarquia.isIn()) {
    MADNESS = 1;
    anarquia.ccolor = color(219, 13, 61);
  } 
  else if (sentimentos.isIn()) {
    FEELINGS = 1;
    sentimentos.ccolor = color(219, 13, 61);
  } 
  else if (estados.isIn()) {
    STATES = 1;
    estados.ccolor = color(219, 13, 61);
  } 
  else if (mapa.isIn()) {
    STATES = 1;
    STATES2 = 1;
    mapa.ccolor = color(219, 13, 61);
  }

  if (mouseY < filterMenu && MENU == -1) MENU = 1;

  if (MENU == 1) {
    menu.mmousePressed();
  }
}

