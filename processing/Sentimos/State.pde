class State {
    String text;
    String abbreviation;
    int occurrence = 0;

    State (String text, String abbreviation) {
        this.text = text;
        this.abbreviation = abbreviation;
    }

    String getKeyAttribute() {
        return this.abbreviation;
    }

    int getSortableAttribute() {
        return this.occurrence;
    }

    void setSortableAttribute(int value) {
        this.occurrence = value;
    }
}
