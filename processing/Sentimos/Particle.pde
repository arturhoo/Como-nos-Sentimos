class Particle{
    Tweet tweet;
    PVector loc, vel, acc;
    float r;

    Particle(PVector l) {
        this.acc = new PVector(0, 0, 0);
        this.vel = new PVector(random(-1, 1), random(-1, 1), 0);
        this.loc = l.get();
        this.r = PARTICLE_RADIUS;
    }

    float getVelocity() {
        return sqrt(vel.x * vel.x + vel.y * vel.y);
    }

    float getMotionDirection() {
        return atan2(vel.x, vel.y);
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


        // Bounce off the walls
        this.bounceOffWalls();

        // Bounce off each other
        // for (int i=NUM_PARTICLES-1; i >= 0; i--) {
        //     bounce(this, particles[i]);
        // }

        // Prevent the particle from going too fast
        if (abs(vel.x) > randomLimit*15 || abs(vel.y) > randomLimit*15) {
            vel.mult(0.5);
        }

        // If mouse is close
        if (abs(mouseX - loc.x) < r*3 && abs(mouseY - loc.y) < r*3) {
            vel.mult(0.9);
            acc.add((mouseX - loc.x)*0.01, (mouseY - loc.y)*0.01, 0);
        }

        // If mouse is over
        if (this.isIn(mouseX, mouseY) && aFocusedTweet == false) {
            r = 14.0;
            textFont(font, 12);
            fill(255);
            text(tweet.feelings[0], loc.x+12, loc.y+12);
            aFocusedTweet = true;
            pFocusedTweet = this;
        }
        else r = PARTICLE_RADIUS;

        // Updates speed and location
        vel.add(acc);
        loc.add(vel);
    }

    void bounceOffWalls() {
        // Bounce off bottom
        if (loc.y > height - r*0.5) {
            vel.y = -abs(vel.y) * 0.9;
        }

        // Bounce off ceiling
        if (loc.y < r*0.5) {
            vel.y = abs(vel.y) * 0.9;
        }

        // Bounce off left border
        if (loc.x < r*0.5) {
            vel.x = abs(vel.x) * 0.9;
        }

        // Bounce off right border
        if (loc.x > width - r*0.5) {
            vel.x = -abs(vel.x) * 0.9;
        }
    }

    /**
    * Draws the particle on the canvas
    */
    void render() {
        ellipseMode(CENTER);
        stroke(255, 255, 255);
        fill(tweet.frgb[0], tweet.frgb[1], tweet.frgb[2]);
        ellipse(loc.x, loc.y, r, r);
    }

    /**
    * Checks if the coordinates specified are inside the particle
    */
    boolean isIn(int x, int y) {
    if (((x - loc.x)*(x - loc.x) + (y - loc.y)*(y - loc.y)) <= (r * r))
        return true;
    else return false;
  }
}

void bounce(Particle a, Particle b) {
    if (sqrt(pow(a.loc.x - b.loc.x, 2) + pow(a.loc.y - b.loc.y, 2)) < (a.r + b.r)*0.5) {
        if (sqrt(pow(a.loc.x - b.loc.x, 2) + pow(a.loc.y - b.loc.y, 2)) >
                sqrt(pow(a.loc.x + a.vel.x - b.loc.x - b.vel.x, 2) +
                pow(a.loc.y + a.vel.y - b.loc.y - b.vel.y, 2))) {

            float commonTangentAngle = atan2(b.loc.x - a.loc.x, b.loc.y
                    - a.loc.y)
                    + asin(1);

            float v1 = a.getVelocity();
            float v2 = b.getVelocity();
            float w1 = a.getMotionDirection();
            float w2 = b.getMotionDirection();

            a.vel.x = sin(commonTangentAngle) * v1 * cos(w1 - commonTangentAngle) + cos(commonTangentAngle) * v2 * sin(w2 - commonTangentAngle);
            a.vel.y = cos(commonTangentAngle) * v1 * cos(w1 - commonTangentAngle) - sin(commonTangentAngle) * v2 * sin(w2 - commonTangentAngle);
            b.vel.x = sin(commonTangentAngle) * v2 * cos(w2 - commonTangentAngle) + cos(commonTangentAngle) * v1 * sin(w1 - commonTangentAngle);
            b.vel.y = cos(commonTangentAngle) * v2 * cos(w2 - commonTangentAngle) - sin(commonTangentAngle) * v1 * sin(w1 - commonTangentAngle);

            a.vel.x *= (0.9);
            a.vel.y *= (0.9);
            b.vel.x *= (0.9);
            b.vel.y *= (0.9);

        }
    }
}
