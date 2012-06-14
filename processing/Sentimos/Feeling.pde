class Feeling {
    String textString;
    int[] frgb;
    int occurrence = 0;
    PVector loc;

    Feeling (String textString, int[] frgb) {
        this.textString = textString;
        this.frgb = frgb;
        this.loc = new PVector();
    }

    String getKeyAttribute() {
        return this.textString;
    }

    int getSortableAttribute() {
        return this.occurrence;
    }

    void setSortableAttribute(int value) {
        this.occurrence = value;
    }

    void drawText() {
        textAlign(RIGHT);
        textFont(font, HISTOGRAM_FONT_SIZE);
        fill(255);
        text(textString + ": " + occurrence, loc.x, loc.y);
        textAlign(LEFT);
    }
}
