import time
import math


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

    def countSingletons(self, lst: list, chunkSize: int) -> dict:
        basketsTable = {}

        # to avoid out of index errors
        if(chunkSize > len(lst)):
            chunkSize = len(lst)

        # select a basket
        for i in range(chunkSize):
            for j in lst[i]:
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
                print(f"Pair {pair} has {potentialPairs[pair]} count")
                lst.append(pair)

        return lst


if __name__ is "__main__":

    def runApriori(chnkSize: int, supp: int):
        start = time.perf_counter()
        fp = "retail.txt"
        basketsContainer = aPriori.parseFile(0, fp)

        # print(basketsContainer)
        ##################################### PASS 1 #####################################
        dct = aPriori.countSingletons(0, basketsContainer, chnkSize)
        # 88163
        # print(dct)

        freqSingletons = aPriori.findFrequentSingletons(0, dct, supp)
        del dct
        # print(freqSingletons)

        ##################################### PASS 2 #####################################
        potPairs = aPriori.potentialPairs(0, freqSingletons)
        # print(potPairs)
        del freqSingletons

        pairCount = aPriori.countAllPairs(0, potPairs, basketsContainer)
        del basketsContainer, potPairs
        freqPairs = aPriori.findFrequentPairs(0, pairCount, supp)
        del pairCount
        end = time.perf_counter()

        print(f"Apriori finished at {(end - start) * 1000:0.3f} ms")

    def runAprioriAtPercent(dataSetPercent: int, supportPercent: int):
        dataSetPercent = math.floor(88163 * (dataSetPercent/100))
        supportPercent = math.floor(dataSetPercent * (supportPercent / 100))
        runApriori(dataSetPercent, supportPercent)
        print(f"dataset size {dataSetPercent} support is {supportPercent}")

    runAprioriAtPercent(1, 10)
    # print(freqPairs)
    # print(len(dct))
    # check count for every candidate pairs
