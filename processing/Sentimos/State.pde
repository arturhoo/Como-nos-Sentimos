class State extends Attribute {
    String abbreviation;

    State (String textString, String abbreviation) {
        super(textString);
        this.abbreviation = abbreviation;
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
        text(abbreviation + ": " + occurrence, loc.x, loc.y);
        textAlign(LEFT);
    }
}
