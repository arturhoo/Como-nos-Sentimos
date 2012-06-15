class Feeling {
    String textString;
    int[] frgb;
    int occurrence = 0;
    PVector loc;

    // Histogram Variables
    PVector particlesLoc;
    int numParticlesCurrentLine = 0;

    Feeling (String textString, int[] frgb) {
        this.textString = textString;
        this.frgb = frgb;
        this.loc = new PVector();
        this.particlesLoc = new PVector();
    }

    /**
    * Returns the object's attribute used as key in Map objects
    */
    String getKeyAttribute() {
        return this.textString;
    }

    /**
    * Returns the object's attribute used as value in Map objects
    */
    int getSortableAttribute() {
        return this.occurrence;
    }

    /**
    * Set the object's attribute used as value in Map objects
    */
    void setSortableAttribute(int value) {
        this.occurrence = value;
    }

    /**
    * Writes the feeling text in the canvas. Used mainly in the Feeling
    * histogram view
    */
    void drawText() {
        textAlign(RIGHT);
        textFont(font, HISTOGRAM_FONT_SIZE);
        fill(255);
        text(textString + ": " + occurrence, loc.x, loc.y);
        textAlign(LEFT);
    }

    /**
    * Gives a location for a particle that wants to be positioned in the
    * feeling histogram view
    */
    PVector getAParticleLoc() {
        PVector vectorToBeReturned = new PVector();
        vectorToBeReturned.set(particlesLoc);

        // Update the next PVector to be returned
        int numParticlesInOneLine = parseInt((PARTICLES_WIDTH + DIST_BTWN_PARTICLES)/(PARTICLE_RADIUS + DIST_BTWN_PARTICLES));
        // If reached limit of particles in one histogram line
        if(numParticlesCurrentLine + 1 > numParticlesInOneLine) {
            numParticlesCurrentLine = 0;
            particlesLoc.x = loc.x + DIST_BTWN_TEXT_AND_PARTICLES;
            particlesLoc.y += DIST_BTWN_HISTOGRAM_ENTRIES + HISTOGRAM_FONT_SIZE;
        } else {
            particlesLoc.x += PARTICLE_RADIUS + DIST_BTWN_PARTICLES;
            numParticlesCurrentLine++;
        }
        return vectorToBeReturned;
    }
}
