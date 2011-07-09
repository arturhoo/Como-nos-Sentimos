class State {
  String st;
  String state;
  int occurrence = 0;
  PVector loc;
  int escape = 0;
  ArrayList<Integer> mapLocList;
  color ccolor;
  
  State (String st, String state, color ccolor) {
    this.st = st;
    this.state = state;
    this.loc = new PVector();
    this.ccolor = ccolor;
    this.mapLocList = new ArrayList<Integer>();
    
    PImage brasil = loadImage("brasil_color.png");
    brasil.loadPixels();
    for(int i=0; i<(brasil.width*brasil.height); i++) {
      if (brasil.pixels[i] == this.ccolor) {
        this.mapLocList.add(i);
      }
    }
  }
}
