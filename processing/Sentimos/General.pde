/**
* Sort a list based on a given attribute that must be returned by the Object.
* Uses the simple selection sort algorithm to sort.
*/
void sortListThatHasTextAndOccurrenceFields(ArrayList list, HashMap map) {
    // Updating the occurrences on the elements of the list
    int size = list.size();
    for (int i=0; i<size; i++)
        list.get(i).setSortableAttribute((Integer) map.get(list.get(i).getKeyAttribute()));

    // Using selection sort
    Object temp;
    int count1, count2;
    int largest;
    for(count1=0; count1<size-1; count1++) {
        largest = 0;
        for(count2=largest+1; count2<size-count1; count2++) {
            if(list.get(largest).getSortableAttribute() > list.get(count2).getSortableAttribute()) {
                largest = count2;
            }
        }
        temp = list.get(size-1-count1);
        list.set(size-1-count1, list.get(largest));
        list.set(largest, temp);
    }
}

/**
* Drops duplicate items from the list, especially useful for the states list
* as there might be more than one entry in states.txt sharing the same state
* abbreviation
*/
void dropDuplicateItemsFromList(ArrayList list) {
    ArrayList indexesToBeRemoved = new ArrayList();
    String lastKey = "";
    for(int i=0; i<list.size(); i++) {
        keyAttribute = list.get(i).getKeyAttribute();
        if(keyAttribute.equals(lastKey)) {
            indexesToBeRemoved.add(i);
        }
        lastKey = keyAttribute;
    }
    for(int i=indexesToBeRemoved.size()-1; i>=0; i--) {
        list.remove(indexesToBeRemoved.get(i));
    }

}

/**
* Given a list of viewable elements, such as Feeling and State, the method
* provides sets the location of these objects, according to the size of the
* canvas and global constraints
*/
void setListElementsLocation(ArrayList list) {
    float textX = LEFT_BORDER_OFFSET + TEXT_WIDTH;
    int numParticlesInOneLine = parseInt((PARTICLES_WIDTH + DIST_BTWN_PARTICLES)/(PARTICLE_RADIUS + DIST_BTWN_PARTICLES));
    int y = parseInt(TOP_BORDER_OFFSET);
    int splittableY = -1; // unsplittable

    Iterator<Object> itr = list.iterator();
    while(itr.hasNext()) {
      Object temp = itr.next();
      if(temp.occurrence == 0) break;
      temp.loc.set(textX, y, 0);
      temp.particlesLoc.set(textX+DIST_BTWN_TEXT_AND_PARTICLES, y-PARTICLE_RADIUS/2, 0);

      // Defines the new Y for the next histogram entry
      int numHistogramLines = parseInt(temp.occurrence/numParticlesInOneLine) + 1;
      y += (DIST_BTWN_HISTOGRAM_ENTRIES + HISTOGRAM_FONT_SIZE)*numHistogramLines;

      // Identify if this histogram line spans less than half of the canvas
      tempX = textX + DIST_BTWN_TEXT_AND_PARTICLES;
      if((temp.occurrence*(PARTICLE_RADIUS + DIST_BTWN_PARTICLES) + tempX < width/2) &&
         splittableY == -1) {
        splittableY = y;
      }

      // Identify if Y has gone below the imposed limits
      if(y > (height - BOTTOM_BORDER_OFFSET)) {
        // If so, start using two columns
        textX = width/2 + LEFT_BORDER_OFFSET + TEXT_WIDTH;
        // Reset the Y
        y = splittableY;
      }
    }
}

/**
* This method executes everything that must be done after data of the
* visualization has been loaded, such as sorting lists
*/
void postTweetLoadingProcedures() {
    sortListThatHasTextAndOccurrenceFields(feelingList, feelingOccurrence);
    sortListThatHasTextAndOccurrenceFields(stateList, stateOccurrence);
    dropDuplicateItemsFromList(stateList);
    setListElementsLocation(feelingList);
    setListElementsLocation(stateList);

    for (int i=NUM_PARTICLES-1; i >= 0; i--) {
        particles[i].setFeelingLoc();
        particles[i].setStateLoc();
    }
}

void setFeelingsView() {
    VIEW = FEELINGS;
}

void setMadnessView() {
    VIEW = MADNESS;
}

void setStatesView() {
    VIEW = STATES;
}
