void clearFeelingsOccurrence() {
  Iterator j = feelingsOccurrence.entrySet().iterator();
  while (j.hasNext ()) {
    Map.Entry me = (Map.Entry)j.next();
    feelingsOccurrence.put(me.getKey(), 0);
  }
}

void clearStatesOccurrence() {
  Iterator j = statesOccurrence.entrySet().iterator();
  int i= 0;
  while (j.hasNext ()) {
    Map.Entry me = (Map.Entry)j.next();
    statesOccurrence.put(me.getKey(), 0);
  }
}

void sortFeelingsList() {
  for (int i=0; i<feelingsList.size(); i++)
    feelingsList.get(i).occurrence = (Integer) feelingsOccurrence.get(feelingsList.get(i).id);
  // Sort feelingsList arrayList
  Collections.sort (feelingsList, new Comparator() {  
    public int compare(Object o1, Object o2) {
      Feeling f1 = (Feeling) o1;
      Feeling f2 = (Feeling) o2;
      return f1.occurrence > f2.occurrence ? -1 : (f1.occurrence < f2.occurrence ? +1 : 0);
    }
  }
  );
}

void sortStatesList() {
  for (int i=0; i<statesList.size(); i++)
    statesList.get(i).occurrence = (Integer) statesOccurrence.get(statesList.get(i).st);
  Collections.sort (statesList, new Comparator() {  
    public int compare(Object o1, Object o2) {
      State s1 = (State) o1;
      State s2 = (State) o2;
      return s1.occurrence > s2.occurrence ? -1 : (s1.occurrence < s2.occurrence ? +1 : 0);
    }
  }
  );  
}
