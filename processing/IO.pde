void readDB(MySQL db, MySQL db2) {
  db = new MySQL(this, host, database, user, pass);
  db2 = new MySQL(this, host, database, user, pass);
  //db = new SQLite(this, "twitter.db");
  //db2 = new SQLite(this, "twitter2.db");
  // After succesful connect
  if (db.connect() && db2.connect()) {  
    print("Conectou!\n");  
    // Get the feelings
    db.query("select * from feelings");
    feelingsHash = new HashMap();
    feelingsOccurrence = new HashMap();
    feelingsList = new ArrayList<Feeling>();
    feelingsRGB = new HashMap();
    while (db.next ()) {
      Feeling feeling = new Feeling(db.getInt("id"), db.getString("feeling"));
      feelingsHash.put(feeling.id, feeling.feeling);
      feelingsOccurrence.put(feeling.id, 0);
      feelingsList.add(feeling);
      StringTokenizer st = new StringTokenizer(db.getString("rgb"), ",");
      int[] frgb = new int[3];
      frgb[0] = Integer.parseInt(st.nextToken());
      frgb[1] = Integer.parseInt(st.nextToken());
      frgb[2] = Integer.parseInt(st.nextToken());
      feelingsRGB.put(feeling.id, frgb);
    }
    print("Pegou os feelings!\n");
    // Get the states
    db.query("select * from states");
    statesOccurrence = new HashMap();
    statesList = new ArrayList<State>();
    while (db.next ()) {
      StringTokenizer st = new StringTokenizer(db.getString("rgb"), ",");
      int[] frgb = new int[3];
      frgb[0] = Integer.parseInt(st.nextToken());
      frgb[1] = Integer.parseInt(st.nextToken());
      frgb[2] = Integer.parseInt(st.nextToken());
      color ccolor = color(frgb[0], frgb[1], frgb[2]);
      State state = new State(db.getString("state"), db.getString("state_long"), ccolor);
      statesOccurrence.put(state.st, 0);
      statesList.add(state);
    }
    print("Pegou os states!\n");
    // Get the X more recent tweets
    //db.query("select a.from_user, a.text, a.sentimento_id from tweets as a join users as b on a.from_user = b.screen_name where b.location_status = 1 order by a.id desc limit " + numParticles);
    db.query("select * from tweets order by id desc limit " + numParticles);
    int count = 0;    
    tweetsList = new ArrayList<Tweet>();
    while (db.next () && count < numParticles) {      
      String uquery = "select name, city, state from users where screen_name=\"" + db.getString("from_user") + "\"";
      db2.query(uquery);
      db2.next();
      Tweet tweet = new Tweet(db.getString("from_user"), db.getString("text"), db.getInt("sentimento_id"), db2.getString("name"), db2.getString("city"), db2.getString("state"));
      //int index = feelingList.indexOf(
      int occurrence = (Integer) feelingsOccurrence.get(tweet.feeling);
      feelingsOccurrence.put(tweet.feeling, occurrence+1);
      if (tweet.state != "" && tweet.state != null) {
        occurrence = (Integer) statesOccurrence.get(tweet.state);
        statesOccurrence.put(tweet.state, occurrence+1);
      }
      tweetsList.add(tweet);
      int[] frgb = (int[]) feelingsRGB.get(tweet.feeling);
      tweet.setRgb(frgb);
      ps.addParticle(tweet);
      count++;
      print(count + "-");
    }    
    print("\nPegou os tweets!\n");
  }
  db.close();
  db2.close();
}

void readDBFiltered() {
  db = new MySQL(this, host, database, user, pass);
  db2 = new MySQL(this, host, database, user, pass);
  //db = new SQLite(this, "twitter.db");
  //db2 = new SQLite(this, "twitter2.db");
  // After succesful connect
  if (db.connect() && db2.connect()) {
    String query = "sentimento_id = -99";
    for (int i=0; i<menu.buttonList.size(); i++) {
      if (menu.buttonList.get(i).active) {
        query += " or sentimento_id = " + menu.buttonList.get(i).feeling_id;
      }
    }
    print("Query: " + query + '\n');
    ps = new ParticleSystem(0, new PVector(width/2, height/2, 0));
    clearFeelingsOccurrence();
    clearStatesOccurrence();
    
    db.query("select * from tweets where " + query + " order by id desc limit " + numParticles);
    int count = 0;    
    tweetsList = new ArrayList<Tweet>();
    while (db.next () && count < numParticles) {      
      String uquery = "select name, city, state from users where screen_name=\"" + db.getString("from_user") + "\"";
      db2.query(uquery);
      db2.next();
      Tweet tweet = new Tweet(db.getString("from_user"), db.getString("text"), db.getInt("sentimento_id"), db2.getString("name"), db2.getString("city"), db2.getString("state"));
      //int index = feelingList.indexOf(
      int occurrence = (Integer) feelingsOccurrence.get(tweet.feeling);
      feelingsOccurrence.put(tweet.feeling, occurrence+1);
      if (tweet.state != "" && tweet.state != null) {
        occurrence = (Integer) statesOccurrence.get(tweet.state);
        statesOccurrence.put(tweet.state, occurrence+1);
      }
      tweetsList.add(tweet);
      int[] frgb = (int[]) feelingsRGB.get(tweet.feeling);
      tweet.setRgb(frgb);
      ps.addParticle(tweet);
      count++;
      print(count + "-");
    }    
    print("\nPegou os tweets!\n");
    
  }
  db.close();
  db2.close();
}

