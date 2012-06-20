class Feeling extends Attribute {
    int[] frgb;

    Feeling (String textString, int[] frgb) {
        super(textString);
        this.frgb = frgb;
    }

    /**
    * Returns the object's attribute used as key in Map objects
    */
    String getKeyAttribute() {
        return this.textString;
    }

    /**
    * Writes the feeling text in the canvas. Used mainly in the Feeling
    * histogram view
    */
    void drawText() {
        textAlign(RIGHT);
        textFont(font, HISTOGRAM_FONT_SIZE);
        fill(255);
        // text(textString + ": " + occurrence, loc.x, loc.y);
        if(!paginated) text(textString + ": " + occurrence, loc.x, loc.y);
        textAlign(LEFT);
    }
}
