class Particle{
    static final float defaultRadius = 10.0;
    Tweet tweet;
    PVector loc, vel, acc;
    float r;

    Particle(PVector l) {
        this.acc = new PVector(0, 0, 0);
        this.vel = new PVector(random(-1, 1), random(-1, 1), 0);
        this.loc = l.get();
        this.r = this.defaultRadius;
    }

    void run() {
        update();
        render();
    }

    void update() {
        // Sets the new, random, acceleration
        float randomLimit = 0.32;
        float randomAcc1 = random(-randomLimit, randomLimit);
        float randomAcc2 = random(-randomLimit, randomLimit);
        acc.set(randomAcc1, randomAcc2, 0);
        

        // Bounce on the walls
        if (loc.x > width || loc.x < 0) vel.x *= -1;
        if (loc.y > height || loc.y < 0) vel.y *= -1;

        // Prevent the particle from going too fast
        if (abs(vel.x) > randomLimit*20 || abs(vel.y) > randomLimit*20) {
            vel.mult(0.5);
        }

        // If mouse is close
        if (abs(mouseX - loc.x) < r*3 && abs(mouseY - loc.y) < r*3) {
            vel.mult(0.9);
            acc.add((mouseX - loc.x)*0.01, (mouseY - loc.y)*0.01, 0);
        }

        // If mouse is over
        if (this.isIn(mouseX, mouseY)) {
            r = 14.0;
        }
        else r = defaultRadius;

        // Updates speed and location
        vel.add(acc);
        loc.add(vel);
    }

    void render() {
        ellipseMode(CENTER);
        stroke(255, 255, 255);
        fill(tweet.frgb[0], tweet.frgb[1], tweet.frgb[2]);
        ellipse(loc.x, loc.y, r, r);
    }

    boolean isIn(int x, int y) {
    if (((x - loc.x)*(x - loc.x) + (y - loc.y)*(y - loc.y)) <= (r * r))
        return true;
    else return false;
  }
}