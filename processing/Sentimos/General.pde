void sortListThatHasTextAndOccurrenceFields(ArrayList list, HashMap map) {
    // Updating the occurrences on the elements of the list
    int size = list.size();
    for (int i=0; i<size; i++)
        list.get(i).setSortableAttribute((Integer) map.get(list.get(i).getKeyAttribute()));
    Object temp;
    int count1, count2;
    int largest;

    // Using selection sort
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

void setListElementsLocation(ArrayList list) {
    float leftBorderOffset = width*0.05;
    float rightBorderOffset = width*0.05;
    float topBorderOffset = height*0.10;
    float bottomBorderOffset = height*0.10;
    float distBtwnTextAndParticles = width*0.05;
    float distBtwnParticles = PARTICLE_RADIUS*0.80;
    float distBtwnHistogramEntries = PARTICLE_RADIUS*1.00;
    float textWidth = width*0.10;
    float textX = leftBorderOffset + textWidth;

    float particlesWidth = width - leftBorderOffset - rightBorderOffset - distBtwnTextAndParticles;
    int numParticlesInOneLine = parseInt((particlesWidth + distBtwnParticles)/(PARTICLE_RADIUS + distBtwnParticles));
    println("numParticlesInOneLine: " + numParticlesInOneLine);
    println("textWidth: " + textWidth);
    println("particlesWidth: " + particlesWidth);

    int y = parseInt(topBorderOffset);
    int splittableY = -1; // unsplittable
    Iterator<Feeling> itr = feelingList.iterator();
    while (itr.hasNext()) {
      Feeling tempFeeling = itr.next();
      if(tempFeeling.occurrence == 0) break;
      tempFeeling.loc.set(textX, y, 0);
      // Defines the new Y for the next histogram entry
      int numHistogramLines = parseInt(tempFeeling.occurrence/numParticlesInOneLine) + 1;
      y += (distBtwnHistogramEntries + HISTOGRAM_FONT_SIZE)*numHistogramLines;

      // Identify if this histogram line spans less than half of the canvas
      tempX = textX + distBtwnTextAndParticles;
      if((tempFeeling.occurrence*(PARTICLE_RADIUS + distBtwnParticles) + tempX < width/2) &&
         splittableY == -1) {
        splittableY = y;
      }

      // Identify if Y has gone below the imposed limits
      if(y > (height - bottomBorderOffset)) {
        // If so, start using two columns
        textX = width/2 + leftBorderOffset + textWidth;
        // Reset the Y
        y = parseInt(topBorderOffset);
      }
    }
}
