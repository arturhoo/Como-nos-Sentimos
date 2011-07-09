class FeelingButton extends Button {
  int feeling_id;

  FeelingButton (String ttext, PVector loc, int fontSize) {
    super(ttext, loc, fontSize);
  }
}

class Menu {
  ArrayList<FeelingButton> buttonList;
  Button all;
  Button search;
  int recty;

  Menu() {
    buttonList = new ArrayList<FeelingButton>();
    int x = 50, y = 20;    
    Iterator j = feelingsHash.entrySet().iterator();
    int i= 0;
    while (j.hasNext ()) {
      Map.Entry me = (Map.Entry)j.next();  
      if (i%6 == 0 && i>0) {
        x+=80;
        y = 20;
      }
      String feeling = (String) me.getValue();
      FeelingButton feelingButton = new FeelingButton(feeling, new PVector(x, y, 0), 12);
      feelingButton.feeling_id = (Integer) me.getKey();
      buttonList.add(feelingButton);
      y += 20;
      i++;
    }
    recty = 10;
    all = new Button("TODOS", new PVector(width-50, 20, 0), 14);
    search = new Button("BUSCAR", new PVector(width-50, 120, 0), 16);
  }

  void drawMenu() {
    fill(0, 0, 0, 220);
    noStroke();
    rectMode(CORNER);
    rect(0, 0, width, recty);
    if (recty == 140) {
      for (int i=0; i<buttonList.size(); i++) buttonList.get(i).draw(0);
      fill(20, 20, 20);
      rect(width-100, 0, 100, 140);
      all.draw(0);
      search.draw(0);
    }
    else recty += 5;
  }

  void mmousePressed() {
    for (int i=0; i<buttonList.size(); i++) {
      if (buttonList.get(i).isIn()) {
        if (!buttonList.get(i).active) {
          buttonList.get(i).ccolor = color(219, 13, 61);
          buttonList.get(i).active = true;
        } 
        else {
          buttonList.get(i).ccolor = color(72, 66, 67);
          buttonList.get(i).active = false;
          all.ccolor = color(72, 66, 67);
          all.active = false;
        }
      }
    }

    if (all.isIn()) {
      if (!all.active) {
        for (int i=0; i<buttonList.size(); i++) {
          buttonList.get(i).ccolor = color(219, 13, 61);
          buttonList.get(i).active = true;
        }
        all.ccolor = color(219, 13, 61);
        all.active = true;
      } 
      else {
        for (int i=0; i<buttonList.size(); i++) {
          buttonList.get(i).ccolor = color(72, 66, 67);
          buttonList.get(i).active = false;
        }
        all.ccolor = color(72, 66, 67);
        all.active = false;
      }
    }

    if (search.isIn()) {
      MENU = -1;
      pheight = height-filterMenu;
      
      MADNESS = 1;
      FEELINGS = -1;
      STATES = -1;
      STATES2 = -1;
      anarquia.ccolor = color(219, 13, 61);
      sentimentos.ccolor = color(72, 66, 67);
      estados.ccolor = color(72, 66, 67);
      mapa.ccolor = color(72, 66, 67);
      
      readDBFiltered();
      sortFeelingsList();
      sortStatesList();
      
      recty = 10;
    }
  }
}

