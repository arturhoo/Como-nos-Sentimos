class State extends Attribute {
    String abbreviation;
    int[] srgb;

    State (String textString, String abbreviation, int[] srgb) {
        super(textString);
        this.abbreviation = abbreviation;
        this.srgb = srgb;
    }

    String getKeyAttribute() {
        return this.abbreviation;
    }

    /**
    * Writes the feeling text in the canvas. Used mainly in the Feeling
    * histogram view
    */
    void drawText() {
        textAlign(RIGHT);
        textFont(font, HISTOGRAM_FONT_SIZE);
        fill(255);
        text(abbreviation.toUpperCase() + ": " + occurrence, loc.x, loc.y);
        textAlign(LEFT);
    }
}
