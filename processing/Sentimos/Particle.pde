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
        // Sets the new, random, acceleration
        float randomLimit = 0.32;
        float randomAcc1 = random(-randomLimit, randomLimit);
        float randomAcc2 = random(-randomLimit, randomLimit);
        acc.set(randomAcc1, randomAcc2, 0);
        vel.add(acc);
        loc.add(vel);

        // Bounce on the walls
        if (loc.x > width || loc.x < 0) vel.x *= -1;
        if (loc.y > height || loc.y < 0) vel.y *= -1;

        // Prevent the particle from going too fast
        if (abs(vel.x) > randomLimit*20 || abs(vel.y) > randomLimit*20) {
            vel.mult(0.5);
        }
    }

    void render() {
        ellipseMode(CENTER);
        stroke(255, 255, 255);
        fill(tweet.frgb[0], tweet.frgb[1], tweet.frgb[2]);
        ellipse(loc.x, loc.y, r, r);
    }
}