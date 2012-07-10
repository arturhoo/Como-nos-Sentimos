class Weather extends Attribute{
    String translation;

    Weather (String textString, String translation) {
        super(textString);
        this.translation = translation;
    }

    /**
    * Returns the object's attribute used as key in Map objects
    */
    String getKeyAttribute() {
        return this.translation;
    }

    /**
    * Writes the weather text in the canvas. Used mainly in the Weather
    * histogram view
    */
    void drawText() {
        textAlign(RIGHT);
        textFont(font, HISTOGRAM_FONT_SIZE);
        fill(255);
        if(!paginated) text(translation + ": " + occurrence, loc.x, loc.y);
        textAlign(LEFT);
    }
}
