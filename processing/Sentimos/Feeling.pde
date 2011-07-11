class Feeling {
  int id;
  String feeling;
  int occurrence = 0;
  PVector loc;
  int escape = 0;
  
  Feeling (int id, String feeling) {
    this.id = id;
    this.feeling = feeling;
    this.loc = new PVector();
  }
}
