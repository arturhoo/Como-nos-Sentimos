class Particle{
    Tweet tweet;
    PVector loc, vel, acc;
    float r;

    Particle(PVector l) {
        acc = new PVector(0, 0, 0);
        vel = new PVector(random(-1, 1), random(-1, 1), 0);
        loc = l.get();
        r = 10.0;
    }

    void run() {
        update();
        render();
    }

    void update() {
        acc.set(random(-0.08, 0.08), random(-0.08, 0.08), 0);
        vel.add(acc);
        loc.add(vel);
        if (loc.x > width || loc.x < 0) vel.x *= -1;
        if (loc.y > height || loc.y < 0) vel.y *= -1;
    }

    void render() {
        ellipseMode(CENTER);
        stroke(255, 255, 255);
        fill(100);
        ellipse(loc.x, loc.y, r, r);
    }
}