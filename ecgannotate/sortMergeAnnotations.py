def processAnnotations(inputList):
    '''
    Description
    -----------
    Functionality:
    1. sort the user-added annotations by starting index
    2. remove identical annotations (same start, end, and type)
    3. merge annotations that are the same type if they overlap with
       each other in the time domain.

    Parameters
    ----------
    inputList : list of dict
        e.g. [{'start': 23, 'end': 48, 'type': 'AF'},
              {'start': 23, 'end': 48, 'type': 'AF'},
              {'start': 45, 'end': 75, 'type': 'AF'}]

    Returns
    -------
    outputList : list of dict
        e.g. [{'start': 23, 'end': 75, 'type': 'AF'}]

    '''
    # Step 1: sort annotations by starting index
    inputList = sorted(inputList, key=lambda x: x['start'])

    # Step 2: remove duplicate annotations
    uniqueList = []
    for annotation in inputList:
        if annotation not in uniqueList:
            uniqueList.append(annotation)

    # Step 3: merge overlapping annotations of the same type
    outputList = []
    i = 0
    while i < len(uniqueList):
        j = i + 1
        while j < len(uniqueList) and uniqueList[j]['type'] == uniqueList[i]['type'] and uniqueList[j]['start'] <= uniqueList[i]['end']:
            # merge overlapping annotations of the same type
            uniqueList[i]['end'] = max(uniqueList[i]['end'], uniqueList[j]['end'])
            j += 1
        outputList.append(uniqueList[i])
        i = j

    return outputList