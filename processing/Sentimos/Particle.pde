class Particle{
    Tweet tweet;
    PVector loc, vel, acc;
    PVector feelingLoc = null;
    PVector stateLoc = null;
    PVector mapLoc = null;
    PVector weatherLoc = null;
    float r;

    Particle(PVector l) {
        this.acc = new PVector();
        this.vel = new PVector(random(-1, 1), random(-1, 1), 0);
        this.loc = l.get();
        this.r = PARTICLE_RADIUS;
    }

    void run() {
        update();
        render();
    }

    void update() {
        if(VIEW == MADNESS) this.madnessUpdate();
        else if(VIEW == FEELINGS) this.feelingsUpdate();
        else if(VIEW == STATES) this.statesUpdate();
        else if(VIEW == MAP) this.mapUpdate();
        else if(VIEW == 5) this.weatherUpdate();
    }

    void madnessUpdate() {
        // Sets the new, random acceleration
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
        if(abs(vel.x) > randomLimit*15 || abs(vel.y) > randomLimit*15)
            vel.mult(0.5);

        r = PARTICLE_RADIUS;
        // If mouse is over canvas
        if(!MOUSE_OUT) {
            // If mouse is close
            if(abs(mouseX - loc.x) < r*3 && abs(mouseY - loc.y) < r*3) {
                vel.mult(0.9);
                acc.add((mouseX - loc.x)*0.01, (mouseY - loc.y)*0.01, 0);
            }

            // If mouse is over
            if(this.isIn(mouseX, mouseY) && pFocusedTweet == null) {
                r = 14.0;
                pFocusedTweet = this;
            }
        }

        // Updates speed and location
        vel.add(acc);
        loc.add(vel);
    }

    void feelingsUpdate() {
        // If this feeling could fit the canvas
        if(feelingLoc.y != height) {
            this.goTo(feelingLoc);
        // If this feeling couldn't fit the canvas
        } else {
            r = PARTICLE_RADIUS;
            if(loc.y < feelingLoc.y-10) this.goTo(feelingLoc);
            else {
                vel.y = 0;
                loc.y = height-PARTICLE_RADIUS/2
            }
            this.bounceOffWalls();

            // Prevent the particle from going too fast
            if(abs(vel.x) > 10.0) vel.mult(0.5);

            float randomLimit = 1.32;
            float randomAcc1 = random(-randomLimit, randomLimit);
            acc.set(randomAcc1, 0, 0);

            // If mouse is close
            if(abs(mouseX - loc.x) < r*3 && abs(mouseY - loc.y) < r*3) {
                vel.mult(0.6);
                acc.add((mouseX - loc.x)*0.01, (mouseY - loc.y)*0.01, 0);
            }

            vel.add(acc);
            loc.add(vel);
        }
        // If mouse is in
        if(!MOUSE_OUT && pFocusedTweet == null && this.isIn(mouseX, mouseY)) {
            r = 14.0;
            pFocusedTweet = this;
        } else {
            r += random(-1.0, 1.0);
            if (r > 14.0) r -= 2;
            if (r < 6.0) r += 2;
        }
    }

    void statesUpdate() {
        if(stateLoc != null) {
            this.goTo(stateLoc);
            // If mouse is over
            if(this.isIn(mouseX, mouseY) && pFocusedTweet == null) {
                r = 14.0;
                pFocusedTweet = this;
            } else {
                r += random(-1.0, 1.0);
                if (r > 14.0) r -= 2;
                if (r < 6.0) r += 2;
            }
        }
    }

    void mapUpdate() {
        if(mapLoc != null) {
            this.goTo(mapLoc);
            // If mouse is over
            if(this.isIn(mouseX, mouseY) && pFocusedTweet == null) {
                r = 14.0;
                pFocusedTweet = this;
            } else {
                r += random(-1.0, 1.0);
                if (r > 11.0) r -= 1;
                if (r < 9.0) r += 1;
            }
        }
    }

    void weatherUpdate() {
        if(weatherLoc != null) {
            this.goTo(weatherLoc);
            // If mouse is over
            if(this.isIn(mouseX, mouseY) && pFocusedTweet == null) {
                r = 14.0;
                pFocusedTweet = this;
            } else {
                r += random(-1.0, 1.0);
                if (r > 14.0) r -= 2;
                if (r < 6.0) r += 2;
            }
        }
    }

    /**
    * Sets the PVector of this particle when the Feeling Histogram view
    * is displayed
    */
    void setFeelingLoc() {
        Feeling tempFeeling = null;
        Iterator<Feeling> itr = feelingList.iterator();
        while(itr.hasNext()) {
            tempFeeling = itr.next();
            if(tempFeeling.textString.equals(tweet.feelings[0]))
                break;
        }
        feelingLoc = new PVector();
        feelingLoc.set(tempFeeling.getAParticleLoc());
    }

    /**
    * Sets the PVector of this particle when the Feeling Histogram view
    * is displayed
    */
    void setStateLoc() {
        State tempState = this.getState();
        stateLoc = new PVector();
        if(tempState != null) {
            stateLoc.set(tempState.getAParticleLoc());
        } else {
            stateLoc.set(getRandomLocationFromQuestionMark());
        }
    }

    /**
    * Sets the PVector of this particle when the Map view is displayed
    */
    void setMapLoc() {
        State tempState = this.getState();
        mapLoc = new PVector();
        if(tempState != null) {
            mapLoc.set(tempState.getARandomMapCoordinate());
        } else {
            mapLoc.set(getRandomLocationFromQuestionMark());
        }
    }

    /**
    * Sets the PVector of this particle when the Feeling Histogram view
    * is displayed
    */
    void setWeatherLoc() {
        State tempWeather = this.getWeather();
        weatherLoc = new PVector();
        if(tempWeather != null) {
            weatherLoc.set(tempWeather.getAParticleLoc());
        } else {
            weatherLoc.set(getRandomLocationFromQuestionMark());
        }
    }

    /**
    * Draws the particle on the canvas
    */
    void render() {
        ellipseMode(CENTER);
        // stroke(255, 255, 255);
        // if(this.isIn(mouseX, mouseY) && !MOUSE_OUT && !aFocusedTweet) {
        if(pFocusedTweet == this) {
            strokeWeight(3);
            stroke(255, 196, 0, FILL_TRANSPARENCY);
            // Draw feeling
            textFont(font, 12);
            fill(255);
            if(loc.y > (height-PARTICLE_RADIUS*2)) {
                text(tweet.feelings[0], loc.x+12, loc.y-12);
            } else if (loc.x > (width-RIGHT_BORDER_OFFSET*2)) {
                textAlign(RIGHT);
                text(tweet.feelings[0], loc.x-12, loc.y+12);
                textAlign(LEFT);
            }else text(tweet.feelings[0], loc.x+12, loc.y+12);
        }
        else noStroke();
        fill(tweet.frgb[0], tweet.frgb[1], tweet.frgb[2], FILL_TRANSPARENCY);
        ellipse(loc.x, loc.y, r, r);
    }

    void goTo(PVector l) {
        acc.set(random(-0.08, 0.08), random(-0.08, 0.08), 0);
        acc.add((l.x - loc.x)*0.015, (l.y - loc.y)*0.015, 0);
        vel.add(acc);
        loc.add(vel);
        vel.mult(0.8);
      }

    void bounceOffWalls() {
        // Bounce off bottom
        if(loc.y > height - r*0.5) vel.y = -abs(vel.y) * 0.9;
        // Bounce off ceiling
        if(loc.y < r*0.5) vel.y = abs(vel.y) * 0.9;
        // Bounce off left border
        if(loc.x < r*0.5) vel.x = abs(vel.x) * 0.9;
        // Bounce off right border
        if(loc.x > width - r*0.5) vel.x = -abs(vel.x) * 0.9;
    }

    /**
    * Checks if the coordinates specified are within the particle
    */
    boolean isIn(int x, int y) {
        if (((x - loc.x)*(x - loc.x) + (y - loc.y)*(y - loc.y)) <= (r * r))
            return true;
        else return false;
    }

    float getVelocity() {
        return sqrt(vel.x * vel.x + vel.y * vel.y);
    }

    float getMotionDirection() {
        return atan2(vel.x, vel.y);
    }

    State getState() {
        State tempState = null;
        boolean foundState = false;
        Iterator<State> itr = stateList.iterator();
        while(itr.hasNext()) {
            tempState = itr.next();
            if(tweet.location != null) {
                String abbreviation = stateAbbreviation.get(tweet.location.state);
                if(tempState.abbreviation.equals(abbreviation)) {
                    foundState = true;
                    break;
                }
            }
        }
        if(foundState) {
            return tempState;
        } else {
            return null;
        }
    }

    Weather getWeather() {
        Weather tempWeather = null;
        boolean foundWeather = false;
        Iterator<Weather> itr = weatherList.iterator();
        while(itr.hasNext()) {
            tempWeather = itr.next();
            if(tweet.location != null && tweet.location.weather != null) {
                if(tempWeather.condition.equals(tweet.location.weather)) {
                    foundWeather = true;
                    break;
                }
            }
        }
        if(foundWeather) {
            return tempWeather;
        } else {
            return null;
        }
    }
}

void bounce(Particle a, Particle b) {
    if (sqrt(pow(a.loc.x - b.loc.x, 2) + pow(a.loc.y - b.loc.y, 2)) < (a.r + b.r)*0.5) {
        if (sqrt(pow(a.loc.x - b.loc.x, 2) + pow(a.loc.y - b.loc.y, 2)) >
                sqrt(pow(a.loc.x + a.vel.x - b.loc.x - b.vel.x, 2) +
                pow(a.loc.y + a.vel.y - b.loc.y - b.vel.y, 2))) {

            float commonTangentAngle = atan2(b.loc.x - a.loc.x, b.loc.y
                                        - a.loc.y) + asin(1);

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
