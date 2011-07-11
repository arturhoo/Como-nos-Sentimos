class Button {
  String ttext;
  PVector loc;
  int fontSize;
  PFont font;
  color ccolor;
  boolean active = false;  

  Button (String ttext, PVector loc, int fontSize) {
    this.ttext = ttext;
    this.fontSize = fontSize;
    this.loc = loc;
    ccolor = color(72, 66, 67);
    font = loadFont("LucidaGrande-24.vlw");
  }

  void draw(int align) {
    textFont(font, fontSize);
    if (align == 0) textAlign(CENTER);
    if (align == 1) textAlign(LEFT);
    if (this.isIn()) fill(201, 75, 2);
    else fill(ccolor);
    text(this.ttext, loc.x, loc.y);
    textAlign(LEFT);
  }  

  boolean isIn() {
    if ((mouseX > (loc.x - textWidth(ttext)/2)) && (mouseX  < (loc.x + textWidth(ttext)/2))) {
      if ((mouseY > loc.y - fontSize/2) && (mouseY < loc.y + fontSize/2)) return true;
    }
    return false;
  }

  
}

