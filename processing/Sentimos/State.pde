class State extends Attribute {
    String abbreviation;
    color scolor;
    ArrayList mapCoordinates;
    int mapWidth;
    int mapHeight;

    State (String textString, String abbreviation, int[] srgb) {
        super(textString);
        this.abbreviation   = abbreviation;
        this.scolor         = color(srgb[0], srgb[1], srgb[2]);
        this.mapCoordinates = new ArrayList();
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

    void loadMapCoordinates(PImage img) {
        mapWidth  = img.width;
        mapHeight = img.height;
        for(int i=0; i<(img.width * img.height); i++) {
            if(img.pixels[i] == scolor)
                mapCoordinates.add(i);
        }
    }

    PVector getARandomMapCoordinate() {
        int pos = (int) (random(mapCoordinates.size()));
        return new PVector(mapCoordinates.get(pos)%mapWidth +
                           (width - mapWidth)/2,
                           mapCoordinates.get(pos)/mapWidth +
                           (height - mapHeight)/2);
    }
}
