class Tweet {
  String from_user;
  String name;
  String city;
  String state;
  String text_;
  int feeling;
  int[] frgb;
  boolean show = false;
  
  Tweet(String from_user, String text_, int feeling, String name, String city, String state) {
    this.from_user = from_user;
    this.text_ = text_;
    this.feeling = feeling;
    this.frgb = new int[3];
    this.name = name;
    this.city = city;
    this.state = state;
  }
  
  void setRgb(int[] frgb) {    
    this.frgb[0] = frgb[0];
    this.frgb[1] = frgb[1];
    this.frgb[2] = frgb[2];
  }
  
  void showFeeling(float x, float y) {
    textFont(font1, 10);
    fill(255,255);
    text((String) feelingsHash.get(this.feeling), x+10, y+10);
  }
  
  void showTweet() {
    int charLimit = 80;
    textFont(font1, 15);
    fill(255,255);
    // Check if it fits the screen
    if (this.text_.length() > charLimit) {
      int end = charLimit;
      char[] cText_ = this.text_.toCharArray();
      while(cText_[end] != ' ' && end < text_.length()-1) end++;
      if(end+1 < text_.length()) {
        String half1 = text_.substring(0, end);
        String half2 = text_.substring(end+1, text_.length());
        text(half1, 20, (height-pheight)*2/5);
        text(half2, 20, (height-pheight)*3/5);
      } else text(this.text_, 20, (height-pheight)*3/5);
    } else text(this.text_, 20, (height-pheight)*3/5);
    textFont(font1, 10);
    String by = "por " + this.from_user;
    if (this.name != null) by += "(" + this.name + ")";
    by += ", em";
    if (this.city != null && this.state != null) {
      char[] cCity = this.city.toCharArray();
      if (cCity[0] == ' ') by += this.city + ",";
      else by += " " + this.city + ",";
    }
    if (this.state != null) by += " " + this.state.toUpperCase();
    else by += " algum lugar";
    
    text(by, 20, (height-pheight)*4/5);
  }
}
