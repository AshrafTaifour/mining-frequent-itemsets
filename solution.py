
filepath = "retail.txt"
basketsContainer = []

with open(filepath, "r") as fp:
    line = fp.readline()
    while line:
        #removes new line at end
        line = line.strip('\n')
        #splits every number in the basket
        line = line.split()
        basketsContainer.append(line)
        line = fp.readline()




#print(basketsContainer)
#print(len(basketsContainer))

def firstPass(lst: list) -> dict:
    basketsTable = {}
    #select a basket
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


def findFrequentPairs(freqSingletons: list, originalData: dict, support: int) -> dict:
    freqPairs = {}
    for i in freqSingletons:
        for j in freqSingletons:
            pass
    return freqPairs


dct = firstPass(basketsContainer)
#print(dct)
#print(dct["1081"])

freqSingletons = findFrequentSingletons(dct, 880)
print(freqSingletons)


#the one below works! but it's inefficient
#for i in freqSingletons:
#    for j in freqSingletons:
#        print(i,j)