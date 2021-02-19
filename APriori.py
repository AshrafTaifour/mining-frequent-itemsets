class aPriori:
    def parseFile(self, filepath: str) -> list:
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

    def firstPass(self, lst: list) -> dict:
        basketsTable = {}
        # select a basket
        for i in lst:
            for j in i:
                if j not in basketsTable:
                    basketsTable[j] = 1

                else:
                    basketsTable[j] += 1

        return basketsTable

    def findFrequentSingletons(self, singletonFreq: dict, support: int) -> list:
        lst = []
        for number in singletonFreq:
            if(singletonFreq[number] >= support):
                lst.append(number)

        return lst

    # given a list of frequent Singletons find all potential pairs
    def potentialPairs(self, freqSingletons: list) -> list:
        potentialPairs = []
        for i in range(0, len(freqSingletons)):
            for j in range(i+1, len(freqSingletons)):
                tupule = (freqSingletons[i], freqSingletons[j])
                potentialPairs.append(tupule)

        # list of candidate pairs
        return potentialPairs

    def countAllPairs(self, potentialPairs: list, originalData: list) -> dict:
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

    def findFrequentPairs(self, potentialPairs: dict, support: int) -> list:
        lst = []
        for pair in potentialPairs:
            if(potentialPairs[pair] >= support):
                lst.append(pair)

        return lst


if __name__ is "__main__":
    fp = "retail.txt"
    basketsContainer = aPriori.parseFile(0, fp)

    # print(basketsContainer)

    dct = aPriori.firstPass(0, basketsContainer)
    # print(dct)
    # print(dct["1081"])

    freqSingletons = aPriori.findFrequentSingletons(0, dct, 880)
    # print(freqSingletons)

    potPairs = aPriori.potentialPairs(0, freqSingletons)
    # print(potPairs)

    pairCount = aPriori.countAllPairs(0, potPairs, basketsContainer)
    freqPairs = aPriori.findFrequentPairs(0, pairCount, 880)

    print(freqPairs)
    # check count for every candidate pairs
