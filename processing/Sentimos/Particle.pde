// A simple Particle class

class Particle {
  Tweet tweet;
  PVector loc;
  PVector vel;
  PVector acc;
  float r;
  float timer;
  PVector mmap;

  // Another constructor (the one we are using here)
  Particle(PVector l, Tweet tweet) {
    this.tweet = tweet;
    acc = new PVector(0, 0, 0);
    vel = new PVector(random(-1, 1), random(-1, 1), 0);
    loc = l.get();
    r = 10.0;
    timer = 100.0;
  }

  void run() {
    update();
    render();
  }

  // Method to update location
  void update() {
    if (MADNESS == 1) {
      // If needs to be shown
      if (this.tweet.show) this.tweet.showTweet();
      // Define new aceleration
      acc.set(random(-0.08, 0.08), random(-0.08, 0.08), 0);
      // If mouse is close
      if (abs(mouseX - loc.x) < width*0.02 && abs(mouseY - loc.y) < height*0.02) {
        vel.mult(0.95);
        //acc.set(random(-0.01,0.01),random(-0.01,0.01),0);
        acc.add((mouseX - loc.x)*0.01, (mouseY - loc.y)*0.01, 0);
      }
      // If it is too fast
      if (abs(vel.x) > 3 || abs(vel.y) > 3) {
        vel.mult(0.5);
      }
      // Sets new vel and location
      vel.add(acc);
      loc.add(vel);
      // Bounce when try to escape
      if (loc.x > width || loc.x < 0) vel.x *= -1;
      if (loc.y > height || loc.y < height - pheight) vel.y *= -1;
      float disX = width - loc.x;
      float disY = height - loc.y;
      if (sqrt(sq(disX) + sq(disY)) < 120 ) vel.mult(-1);

      // If mouse is over
      if (this.isIn(mouseX, mouseY) && alreadyShowing == false) {
        r = 14.0;
        this.tweet.showFeeling(loc.x, loc.y);
        alreadyShowing = true;
      }
      else r = 10.0;
    }
    //--------------------//
    //      FEELINGS      //
    //--------------------//
    else if (FEELINGS == 1) {
      if (this.tweet.show) this.tweet.showTweet();
      int i;
      for (i=0; i < feelingsList.size(); i++)
        if (this.tweet.feeling == feelingsList.get(i).id) break;
      loc.x += ((feelingsList.get(i).loc.x - loc.x)+110+(feelingsList.get(i).escape%600))/16;
      loc.y += ((feelingsList.get(i).loc.y+(feelingsList.get(i).escape/600*22) - loc.y)-5)/16;
      feelingsList.get(i).escape += 20;
      // ---------------      
      r += random(-1.0, 1.0);
      if (r > 14.0) r -= 2;
      if (r < 6.0) r += 2;
    } 
    //--------------------//
    //       STATES       //
    //--------------------//
    else if (STATES == 1) {
      if (this.tweet.state != "" && this.tweet.state != null) {
        if (this.tweet.show) this.tweet.showTweet();
        int i;
        for (i=0; i < statesList.size(); i++) 
          if (this.tweet.state.equals(statesList.get(i).st)) break;
        if (STATES2 != 1) {
          loc.x += ((statesList.get(i).loc.x - loc.x)+60+(statesList.get(i).escape%600))/16;
          loc.y += ((statesList.get(i).loc.y+(statesList.get(i).escape/600*22) - loc.y)-5)/16;
          statesList.get(i).escape += 20;
          // ---------------
          r += random(-1.0, 1.0);
          if (r > 14.0) r -= 2;
          if (r < 6.0) r += 2;
        } 
        else {
          if (this.mmap == null) {
            int pos = (int) random(statesList.get(i).mapLocList.size());
            this.mmap = new PVector(statesList.get(i).mapLocList.get(pos)%400 + (width-400)/2, (height-400)/2 + statesList.get(i).mapLocList.get(pos)/400);
          }
          this.goTo(this.mmap);
          // If mouse is over
          if (this.isIn(mouseX, mouseY) && alreadyShowing == false) {
            r = 12.0;
            this.tweet.showFeeling(loc.x, loc.y);
            alreadyShowing = true;
          }
          else this.r = 8.0;
        }
      }
      else {
        if (this.tweet.show) this.tweet.showTweet();
        if (mmap == null) {
          int pos = (int) random(questionList.size());
          mmap = new PVector(questionList.get(pos)%img.width + width-170, (height-80) + questionList.get(pos)/img.width);
        }
        this.goTo(mmap);
        // If mouse is over
        if (this.isIn(mouseX, mouseY) && alreadyShowing == false) {
          r = 12.0;
          this.tweet.showFeeling(loc.x, loc.y);
          alreadyShowing = true;
        }
        else r = 8.0;
      }
    }
  }

  void goTo(PVector l) {
    acc.set(random(-0.08, 0.08), random(-0.08, 0.08), 0);
    acc.add((l.x - loc.x)*0.01, (l.y - loc.y)*0.01, 0);
    vel.add(acc);
    loc.add(vel);
    vel.mult(0.8);
  }

  // Method to display
  void render() {
    ellipseMode(CENTER);
    stroke(255, 255, 255);
    fill(this.tweet.frgb[0], this.tweet.frgb[1], this.tweet.frgb[2]);
    ellipse(loc.x, loc.y, r, r);
  }

  boolean isIn(int x, int y) {    
    if (((x - loc.x)*(x - loc.x) + (y - loc.y)*(y - loc.y)) <= (r * r))
      return true;
    else return false;
  }

  boolean onClick() {
    if (this.isIn(mouseX, mouseY)) {
      pheight = height - 80;
      // Tira todo mundo do espaço de cima
      for (int i = ps.particles.size()-1; i >= 0; i--) {
        Particle p = (Particle) ps.particles.get(i);
        if (p.loc.y <= height - pheight) p.loc.y = height - pheight;
      }
      return true;
    }
    else return false;
  }
}

