void sortFeelingList() {
    // Updating the occurrences
    for (int i=0; i<feelingList.size(); i++)
        feelingList.get(i).occurrence = (Integer) feelingOccurrence.get(feelingList.get(i).text);
    Feeling tempFeeling;
    int count1, count2;
    int largest;
    int size = feelingList.size();

    // Using selection sort
    for(count1=0; count1<size-1; count1++) {
        largest = 0;
        for(count2=largest+1; count2<size-count1; count2++) {
            if(feelingList.get(largest).occurrence > feelingList.get(count2).occurrence) {
                largest = count2;
            }
        }
        tempFeeling = feelingList.get(size-1-count1);
        feelingList.set(size-1-count1, feelingList.get(largest));
        feelingList.set(largest, tempFeeling);
    }
}