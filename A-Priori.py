
def parseFile(filepath: str) -> list:
    basketsContainer = []
    with open(filepath, "r") as fp:
        line = fp.readline()
        while line:
            # removes new line at end
            line = line.strip('\n')
            # splits every number in the basket
            line = line.split()
            basketsContainer.append(line)
            line = fp.readline()
        return basketsContainer


def firstPass(lst: list) -> dict:
    basketsTable = {}
    # select a basket
    for i in lst:
        for j in i:
            if j not in basketsTable:
                basketsTable[j] = 1

            else:
                basketsTable[j] += 1

    return basketsTable


def findFrequentSingletons(singletonFreq: dict, support: int) -> list:
    lst = []
    for number in singletonFreq:
        if(singletonFreq[number] >= support):
            lst.append(number)

    return lst


# given a list of frequent Singletons find all potential pairs
def potentialPairs(freqSingletons: list) -> list:
    potentialPairs = []
    for i in range(0, len(freqSingletons)):
        for j in range(i+1, len(freqSingletons)):
            tupule = (freqSingletons[i], freqSingletons[j])
            potentialPairs.append(tupule)

    # list of candidate pairs
    return potentialPairs


def countAllPairs(potentialPairs: list, originalData: list) -> dict:
    countAllPairs = {}
    for pair in potentialPairs:
        print(f"counting all occurances of pair {pair}...")
        for basket in originalData:
            # if both pair items are in the basket
            if pair[0] in basket and pair[1] in basket:
                #print(f"pair {pair} is in basket {basket}")
                # if pair not in dictionary, add them
                if pair not in countAllPairs:
                    countAllPairs[pair] = 1
                # pair already in hash table/dictionary
                else:
                    # increment count of pair
                    countAllPairs[pair] += 1
            # if pair aren't in basket
            else:
                pass

    return countAllPairs


def findFrequentPairs(potentialPairs: dict, support: int) -> list:
    lst = []
    for pair in potentialPairs:
        if(potentialPairs[pair] >= support):
            lst.append(pair)

    return lst


fp = "retail.txt"
basketsContainer = parseFile(fp)

# print(basketsContainer)

dct = firstPass(basketsContainer)
# print(dct)
# print(dct["1081"])

freqSingletons = findFrequentSingletons(dct, 880)
# print(freqSingletons)


potPairs = potentialPairs(freqSingletons)
# print(potPairs)

pairCount = countAllPairs(potPairs, basketsContainer)
freqPairs = findFrequentPairs(pairCount, 880)

print(freqPairs)
# check count for every candidate pairs
