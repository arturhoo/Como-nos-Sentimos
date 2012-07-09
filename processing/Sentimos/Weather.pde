class Weather extends Attribute{
    String condition;
    String translation;

    Weather (String condition, String translation) {
        super(condition);
        this.condition = condition;
        this.translation = translation;
    }

    /**
    * Returns the object's attribute used as key in Map objects
    */
    String getKeyAttribute() {
        return this.condition;
    }

    /**
    * Writes the weather text in the canvas. Used mainly in the Weather
    * histogram view
    */
    void drawText() {
        textAlign(RIGHT);
        textFont(font, HISTOGRAM_FONT_SIZE);
        fill(255);
        if(!paginated) text(condition + ": " + occurrence, loc.x, loc.y);
        textAlign(LEFT);
    }
}
