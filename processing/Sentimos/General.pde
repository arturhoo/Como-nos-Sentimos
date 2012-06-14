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
