class State {
    String textString;
    String abbreviation;
    int occurrence = 0;

    State (String textString, String abbreviation) {
        this.textString = textString;
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
