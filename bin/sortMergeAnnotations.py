def sortMergeAnnotations(inputList):
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
    # create output variable
    outputList = []

    # remove identical annotations
    tmpList = []
    [tmpList.append(item) for item in inputList if item not in tmpList]
    inputList = tmpList

    # sort the list by starting index
    inputList.sort(key=sortFunc)

    # merge the overlapped ones
    # first degrade the inputList into a dict {'AF':[23,45,43,75],...}
    typeList = [item['type'] for item in inputList]
    typeList = list(set(typeList))
    indexList = {}
    for typeItem in typeList:
        indexList[typeItem] = []
        [indexList[typeItem].extend([item['start'],item['end']]) for item in inputList if item['type']==typeItem]
        indexList[typeItem] = merge(indexList[typeItem])
    # now we should have a dict of nonoverlap index, e.g. {'AF':[23,75],...}
    # now rebuild the list

    for key in indexList.keys():
        for count,item in enumerate(indexList[key]):
            if (count+1)%2==0:
                start = indexList[key][count-1]
                end = indexList[key][count]
                outputList.append({'start':start,'end':end,'type':key})

    # sort the list by starting index
    outputList.sort(key=sortFunc)

    return outputList

def sortFunc(item):
    '''
    Just a small function to help with sorting.
    '''
    return item['start']

def merge(numList):
    '''
    A function merging the overlapped indexes.

    Parameters
    ----------
    numList : list of numbers
        e.g. [1,4,3,5]

    Returns
    -------
    resultList : list of numbers
        e.g. [1,5]

    '''
    resultList = numList.copy()
    for count,item in enumerate(numList):
        if (count+1)%2 == 0 and (count+1)>3: # every 2 items, starting from the 4th item
            if numList[count-2]>=numList[count-1]:
                resultList.remove(numList[count-2])
                resultList.remove(numList[count-1])

    return resultList
