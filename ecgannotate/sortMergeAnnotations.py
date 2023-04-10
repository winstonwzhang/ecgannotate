def processAnnotations(inputList):

    # Step 1: remove duplicate annotations
    uniqueList = []
    for annotation in inputList:
        if annotation not in uniqueList:
            uniqueList.append(annotation)
    
    # Step 2: sort annotations by type first, starting index second
    sortedList = sorted(uniqueList, key=lambda x: (x['type'], x['start']))

    # Step 3: merge overlapping annotations of the same type
    outputList = []
    i = 0
    while i < len(sortedList):
        j = i + 1
        while j < len(sortedList) and sortedList[j]['type'] == sortedList[i]['type'] and sortedList[j]['start'] <= sortedList[i]['end']:
            # merge overlapping annotations of the same type
            sortedList[i]['end'] = max(sortedList[i]['end'], sortedList[j]['end'])
            j += 1
        outputList.append(sortedList[i])
        i = j

    return outputList
