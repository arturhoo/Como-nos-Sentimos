class Feeling {
    String text;
    int[] frgb;
    int occurrence = 0;

    Feeling (String text, int[] frgb) {
        this.text = text;
        this.frgb = frgb;
    }

    String getKeyAttribute() {
        return this.text;
    }

    int getSortableAttribute() {
        return this.occurrence;
    }

    void setSortableAttribute(int value) {
        this.occurrence = value;
    }
}
