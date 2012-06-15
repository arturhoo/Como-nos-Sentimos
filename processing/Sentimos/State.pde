class State extends Attribute {
    String abbreviation;

    State (String textString, String abbreviation) {
        super(textString);
        this.abbreviation = abbreviation;
    }

    String getKeyAttribute() {
        return this.abbreviation;
    }
}
